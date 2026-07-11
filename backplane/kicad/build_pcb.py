#!/usr/bin/env python3
"""
Headless KiCad board generator for the A7S backplane — modular + config-driven.

Run:  ../tools/kpython build_pcb.py [variant]      (variant defaults to "rev2")

DESIGN RULE: no positional literals in the build logic. Everything that has a place on the
board lives as *data* in a BoardConfig (see CONFIGS at the bottom). The logic below only
knows how to turn a config into a board.

- A single `Frame` maps the A7S STEP datums into KiCad coords.
- A single `Frame.move` offset relocates the ENTIRE board coherently — headers, mounting
  holes, outline AND curated parts all shift together, so the A7S mate geometry can never
  drift out of sync. "We moved the board for rev2" == change `move`, nothing else.
- Add a board variant  ==  add a BoardConfig, not edit the code.
"""
import os, re, math, sys
from dataclasses import dataclass, field
import pcbnew

HERE   = os.path.dirname(os.path.abspath(__file__))
FPROOT = os.environ["KICAD_FP"]                    # nix footprints (set by tools/kpython)
A7SLIB = os.path.join(HERE, "..", "a7s.pretty")    # project footprints

# --------------------------------- units ---------------------------------
def mm(v):     return pcbnew.FromMM(v)
def vec(x, y): return pcbnew.VECTOR2I(mm(x), mm(y))

# ------------------------------ coordinate frame ------------------------------
@dataclass
class Frame:
    """A7S STEP frame (X right, Y 'up' = less-negative) -> KiCad frame (Y down).

    `ox`      base X shift into positive KiCad space.
    `flip_y`  STEP Y grows upward, KiCad Y grows downward.
    `move`    (dx, dy) — relocate the WHOLE board. This is the one knob for a board move.
    """
    ox: float = 60.0
    flip_y: bool = True
    move: tuple = (0.0, 0.0)
    def step(self, sx, sy):                        # STEP-datum point -> KiCad
        return (sx + self.ox + self.move[0], (-sy if self.flip_y else sy) + self.move[1])
    def board(self, x, y):                         # curated board-frame point -> KiCad
        return (x + self.move[0], y + self.move[1])

# ------------------------------ placement specs ------------------------------
@dataclass
class Header:            # datum-locked connector that physically mates the A7S
    ref: str
    step: tuple          # (sx, sy) STEP-measured header center
    rot: float           # in-plane rotation
    back: bool = True    # sockets live on the shield's underside
    mirror_x: bool = False   # horizontal (east<->west) mirror of the back-side placement.
                             # The A7S reference was flipped horizontally; this corrects it.

@dataclass
class Anchor:            # curated placement for a "free" part (display, radios, buttons...)
    ref: str
    xy: tuple            # board-frame center (or origin if by_origin)
    rot: float = 0.0
    back: bool = False
    by_origin: bool = False   # place by footprint origin instead of bbox center

@dataclass
class Silk:              # a silkscreen label group for one footprint
    ref: str
    labels: dict         # pad-number/name -> text
    front: bool          # F.SilkS vs B.SilkS (mirrored)
    fixed: tuple = None  # (dx,dy) mm label offset; None -> auto perpendicular-to-row
    size: float = 0.6

@dataclass
class BoardConfig:
    name: str
    frame: Frame
    headers: list
    anchors: list
    silk: list
    outline_step: list          # polygon corners in STEP frame (the SHIELD edge)
    holes_step: list            # A7S mounting-hole centers in STEP frame
    pack_region: tuple          # (x_left, y_top, x_right) board-frame shelf for loose passives
    # a7s_move relocates ONLY the A7S cluster (J1, J2, and the 4 A7S mounting holes) as one
    # rigid unit, WITHOUT moving the shield outline or the curated parts. This is how the A7S
    # slides toward an edge (e.g. west = negative dx) independently of the board shape.
    a7s_move: tuple = (0.0, 0.0)
    pack_on_back: bool = True
    net: str = None
    out: str = None

# --------------------------------- netlist ---------------------------------
def load_netlist(path):
    txt = open(path).read()
    comps = {}
    for c in re.split(r'\n\s*\(comp\b', txt)[1:]:
        ref = re.search(r'\(ref "([^"]+)"\)', c)
        val = re.search(r'\(value "([^"]+)"\)', c)
        fp  = re.search(r'\(footprint "([^"]+)"\)', c)
        if ref and fp:
            comps[ref.group(1)] = (fp.group(1), val.group(1) if val else "")
    nets = {}
    for b in re.split(r'\n\s*\(net\b', txt)[1:]:
        nm = re.search(r'\(name "([^"]+)"\)', b)
        nodes = re.findall(r'\(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)', b)
        if nm and nodes:
            nets[nm.group(1)] = nodes
    return comps, nets

# ----------------------------- footprint helpers -----------------------------
def fp_path(libid):
    lib, name = libid.split(":")
    d = A7SLIB if lib == "a7s" else os.path.join(FPROOT, lib + ".pretty")
    return d, name

def cbox(fp):
    """True footprint extent = union of pad + graphic bboxes (courtyard is unreliable here)."""
    boxes = [p.GetBoundingBox() for p in fp.Pads()]
    try:    boxes += [d.GetBoundingBox() for d in fp.GraphicalItems()]
    except Exception: pass
    L = min(b.GetLeft() for b in boxes);  R = max(b.GetRight() for b in boxes)
    T = min(b.GetTop()  for b in boxes);  B = max(b.GetBottom() for b in boxes)
    return (pcbnew.ToMM(L), pcbnew.ToMM(R), pcbnew.ToMM(T), pcbnew.ToMM(B))

def fp_wh(fp):
    l, r, t, b = cbox(fp); return r - l, b - t

def orient_at_center(fp, cx, cy, rot):
    """Place so the footprint's bbox center lands on (cx,cy) (SetPosition anchors pad1)."""
    fp.SetOrientationDegrees(rot); fp.SetPosition(vec(cx, cy))
    l, r, t, b = cbox(fp); dx = cx - (l + r) / 2.0; dy = cy - (t + b) / 2.0
    p = fp.GetPosition(); fp.SetPosition(pcbnew.VECTOR2I(p.x + mm(dx), p.y + mm(dy)))

def orient_at_origin(fp, x, y, rot):
    fp.SetOrientationDegrees(rot); fp.SetPosition(vec(x, y))

# ----------------------------- board assembly steps -----------------------------
def new_board(nets):
    board = pcbnew.BOARD()
    netobj = {}
    for nn in nets:
        ni = pcbnew.NETINFO_ITEM(board, nn); board.Add(ni); netobj[nn] = ni
    return board, netobj

def add_footprints(board, comps):
    missing = []
    for ref, (libid, val) in comps.items():
        d, name = fp_path(libid)
        fp = pcbnew.FootprintLoad(d, name)
        if fp is None:
            missing.append(f"{ref}:{libid}"); continue
        fp.SetReference(ref); fp.SetValue(val); board.Add(fp)
    return missing

def place_headers(board, cfg):
    for h in cfg.headers:
        fp = board.FindFootprintByReference(h.ref)
        if not fp: print("  header missing:", h.ref); continue
        cx, cy = cfg.frame.step(*h.step)
        cx += cfg.a7s_move[0]; cy += cfg.a7s_move[1]        # A7S cluster slides as one unit
        orient_at_center(fp, cx, cy, h.rot)
        if h.back: fp.Flip(vec(cx, cy), h.mirror_x)         # mirror_x=True -> east/west mirror

def place_anchors(board, cfg):
    for a in cfg.anchors:
        fp = board.FindFootprintByReference(a.ref)
        if not fp: print("  anchor missing:", a.ref); continue
        x, y = cfg.frame.board(*a.xy)
        (orient_at_origin if a.by_origin else orient_at_center)(fp, x, y, a.rot)
        if a.back: fp.Flip(vec(x, y), False)

def pack_free(board, cfg, comps):
    """Shelf-pack whatever the config did NOT explicitly place (loose passives)."""
    named = {h.ref for h in cfg.headers} | {a.ref for a in cfg.anchors}
    free = [fp for r in comps if r not in named
            for fp in [board.FindFootprintByReference(r)] if fp]
    xL, yT = cfg.frame.board(cfg.pack_region[0], cfg.pack_region[1])
    xR, _  = cfg.frame.board(cfg.pack_region[2], cfg.pack_region[1])
    M = 1.6
    for fp in free:
        fp.SetOrientationDegrees(0)
        if cfg.pack_on_back: fp.Flip(fp.GetPosition(), False)
    free.sort(key=lambda fp: fp_wh(fp)[1], reverse=True)
    cx, cy, rowh = xL, yT, 0.0
    for fp in free:
        w, h = fp_wh(fp)
        if cx + w > xR: cx = xL; cy += rowh + M; rowh = 0.0
        orient_at_center(fp, cx + w / 2.0, cy + h / 2.0, 0)
        cx += w + M; rowh = max(rowh, h)
    return len(free)

def assign_nets(board, nets, netobj):
    unmatched = 0
    for nn, nodes in nets.items():
        ni = netobj[nn]
        for r, p in nodes:
            fp = board.FindFootprintByReference(r)
            if not fp: continue
            pad = fp.FindPadByNumber(p)
            if pad: pad.SetNet(ni)
            else:   unmatched += 1
    return unmatched

def _row_perp(pts):
    """Unit vector perpendicular to the principal (row) axis of a pad cloud."""
    n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
    sxx = sum((p[0]-mx)**2 for p in pts); syy = sum((p[1]-my)**2 for p in pts)
    sxy = sum((p[0]-mx)*(p[1]-my) for p in pts)
    th = 0.5 * math.atan2(2*sxy, (sxx - syy) if abs(sxx - syy) > 1 else 1e-9)
    row = (math.cos(th), math.sin(th))
    return (mx, my), (-row[1], row[0])

def add_silk(board, cfg):
    for s in cfg.silk:
        fp = board.FindFootprintByReference(s.ref)
        if not fp: print("  silk: no", s.ref); continue
        pos = {p.GetNumber(): (p.GetPosition().x, p.GetPosition().y) for p in fp.Pads()}
        (mx, my), perp = _row_perp(list(pos.values()))
        layer = pcbnew.F_SilkS if s.front else pcbnew.B_SilkS
        off = mm(1.9); n = 0
        for key, text in s.labels.items():
            if key not in pos: print(f"  silk {s.ref}: pad {key} missing"); continue
            px, py = pos[key]
            if s.fixed is not None:
                lx, ly = int(px + mm(s.fixed[0])), int(py + mm(s.fixed[1]))
            else:
                along = (px-mx)*perp[0] + (py-my)*perp[1]
                side = 1.0 if (abs(along) < mm(0.6) or along >= 0) else -1.0
                lx, ly = int(px + off*perp[0]*side), int(py + off*perp[1]*side)
            t = pcbnew.PCB_TEXT(board); t.SetText(text); t.SetLayer(layer)
            t.SetPosition(pcbnew.VECTOR2I(lx, ly))
            t.SetTextSize(pcbnew.VECTOR2I(mm(s.size), mm(s.size))); t.SetTextThickness(mm(0.12))
            if not s.front: t.SetMirrored(True)
            board.Add(t); n += 1
        print(f"  silk {s.ref}: {n}/{len(s.labels)} on {'F' if s.front else 'B'}.SilkS")

def draw_outline(board, cfg):
    pts = [cfg.frame.step(sx, sy) for sx, sy in cfg.outline_step]
    n = len(pts)
    for i in range(n):
        seg = pcbnew.PCB_SHAPE(board); seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(vec(*pts[i])); seg.SetEnd(vec(*pts[(i+1) % n]))
        seg.SetLayer(pcbnew.Edge_Cuts); seg.SetWidth(mm(0.15)); board.Add(seg)

def add_holes(board, cfg):
    mh_dir = os.path.join(FPROOT, "MountingHole.pretty")
    mh_name = next((c for c in ["MountingHole_2.7mm_M2.5", "MountingHole_2.7mm_M2.5_Pad", "MountingHole_2.7mm"]
                    if os.path.exists(os.path.join(mh_dir, c + ".kicad_mod"))), None)
    for i, (sx, sy) in enumerate(cfg.holes_step, 1):
        x, y = cfg.frame.step(sx, sy)
        x += cfg.a7s_move[0]; y += cfg.a7s_move[1]          # A7S holes move with the cluster
        if mh_name:
            h = pcbnew.FootprintLoad(mh_dir, mh_name); h.SetReference(f"H{i}")
            board.Add(h); h.SetPosition(vec(x, y))
        else:
            c = pcbnew.PCB_SHAPE(board); c.SetShape(pcbnew.SHAPE_T_CIRCLE)
            c.SetCenter(vec(x, y)); c.SetEnd(vec(x + 1.35, y)); c.SetLayer(pcbnew.Edge_Cuts)
            c.SetWidth(mm(0.15)); board.Add(c)
    return mh_name

def build(cfg):
    print(f"[{cfg.name}] frame ox={cfg.frame.ox} move={cfg.frame.move}")
    comps, nets = load_netlist(cfg.net)
    print(f"  parsed {len(comps)} comps, {len(nets)} nets")
    board, netobj = new_board(nets)
    missing = add_footprints(board, comps)
    if missing: print("  MISSING footprints:", missing)
    place_headers(board, cfg)
    place_anchors(board, cfg)
    nfree = pack_free(board, cfg, comps)
    print(f"  placed {len(comps) - len(missing)} footprints; packed {nfree} free")
    print("  unmatched pads:", assign_nets(board, nets, netobj))
    add_silk(board, cfg)
    draw_outline(board, cfg)
    print("  mounting holes:", add_holes(board, cfg) or "edge-circles")
    pcbnew.SaveBoard(cfg.out, board)
    print("  saved", cfg.out)
    return board

# ================================== CONFIGS ==================================
# A7S GPIO header STEP datums (from refs/MECH-DATUMS.md): 30-pin center (2.11,-33.02),
# 15-pin center (2.08,-78.71). These are physical A7S positions and must not be edited to
# "move the board" — use frame.move for that so the mate stays correct.

def rev2():
    return BoardConfig(
        name="rev2",
        net=os.path.join(HERE, "..", "a7s_backplane.net"),
        out=os.path.join(HERE, "a7s_backplane.kicad_pcb"),
        # ---- relocate the whole board here (headers+holes+outline+parts move together) ----
        frame=Frame(ox=60.0, flip_y=True, move=(0.0, 0.0)),
        # ---- A7S headers: rot=270 (NOT 90). rev1 used 90 and mated pin1<->pin30 (180deg
        #      diagonal flip) -> A7S 3V3 shorted to shield GND, killing the SBC on contact.
        #      The 2x15/1x15 grids are 180deg-symmetric about their datum-pinned center, so
        #      +180deg keeps every hole fixed and only relabels pad->hole (pad P mates pin P).
        headers=[
            # J1 (30-pin double) = NORTH datum, J2 (15-pin single) = SOUTH datum.
            # mirror_x corrects the horizontally-flipped A7S reference. rot/mirror confirmed
            # visually in KiCad (human-in-the-loop) against the real A7S pinout.
            Header("J1", (2.11, -33.02), 270, mirror_x=True),
            Header("J2", (2.08, -78.71), 270, mirror_x=True),
        ],
        # ---- curated free-part placement (board frame) ----
        anchors=[
            Anchor("J3",  (44.5, 42.0), 0,  by_origin=True),          # TFT header, LEFT edge (front)
            Anchor("A1",  (44.0, 42.0), 90, back=True),               # RP2040-Zero, center-back
            Anchor("J5",  (16.0, 10.0), 90, back=True),               # Radio1  -> TOP-left
            Anchor("J5b", (24.0, 10.0), 0,  back=True),
            Anchor("J6",  (70.0, 10.0), 90, back=True),               # Radio2  -> TOP-right
            Anchor("J6b", (62.0, 10.0), 0,  back=True),
            Anchor("J12", (44.0, 88.0), 90),                          # Flipper -> BOTTOM (front)
            Anchor("SW1", (16.0, 73.0), 0), Anchor("SW2", (27.0, 73.0), 0),   # buttons (front)
            Anchor("SW3", (38.0, 73.0), 0), Anchor("SW4", (49.0, 73.0), 0),
            Anchor("J8",  (6.0, 84.0), 90, back=True),                # JOY   -> LEFT
            Anchor("J11", (6.0, 90.0), 90, back=True),                # BTN5/6 -> LEFT
            Anchor("J10", (82.0, 84.0), 90, back=True),               # ENC   -> RIGHT
            Anchor("TP1", (74.0, 73.0), 0), Anchor("TP2", (78.0, 73.0), 0),   # console pads (front)
        ],
        # ---- silkscreen labels (rev1 had NONE -> header mis-mate + unlabeled TFT VCC/GND) ----
        silk=[
            Silk("J1", {"1": "1|3V3", "2": "5V", "4": "5V", "6": "GND", "17": "3V3", "30": "30|GND"}, front=False),
            Silk("J2", {"1": "1|PB3", "4": "GND", "9": "GND", "15": "15|PG5"}, front=False, fixed=(0, 2.0)),
            Silk("J3", {"1": "1 VCC", "2": "GND", "3": "CS", "4": "RST", "5": "DC", "6": "SDI", "7": "SCK",
                        "8": "LED", "9": "SDO", "10": "TCLK", "11": "TCS", "12": "TDIN", "13": "TDO", "14": "TIRQ"},
                 front=True, fixed=(-2.2, 0), size=0.5),
            Silk("A1", {"5V": "5V", "GND": "GND", "3V3": "3V3", "GP0": "TX0", "GP1": "RX1",
                        "GP2": "BTN1", "GP3": "BTN2", "GP4": "BTN3", "GP5": "BTN4"}, front=False),
        ],
        outline_step=[(-58.5, -4.0), (27.5, -4.0), (27.5, -94.0), (-58.5, -94.0)],
        holes_step=[(-19.81, -33.18), (23.99, -33.18), (-19.81, -76.98), (23.99, -76.98)],
        pack_region=(6.0, 24.0, 36.0),
        pack_on_back=True,
    )

CONFIGS = {"rev2": rev2}

if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "rev2"
    if variant not in CONFIGS:
        sys.exit(f"unknown variant {variant!r}; known: {list(CONFIGS)}")
    build(CONFIGS[variant]())
