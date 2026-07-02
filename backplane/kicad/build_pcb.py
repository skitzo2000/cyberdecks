#!/usr/bin/env python3
"""
Headless KiCad board generator for the A7S backplane (run via ../tools/kpython).
- parses ../a7s_backplane.net  (components + footprints + nets)
- loads each footprint from the nix KiCad libs (+ project a7s.pretty)
- assigns nets to pads from the netlist
- places J1/J2 (A7S GPIO headers) on the STEP-measured datums; draws Edge.Cuts
  outline (overhang-left + top/bottom strips), 4 mounting holes; rough-clusters the rest
- saves a7s_backplane.kicad_pcb
Routing is NOT done (no headless autorouter) — output is placed + full ratsnest.
"""
import os, re, sys, glob
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
NET  = os.path.join(HERE, "..", "a7s_backplane.net")
OUT  = os.path.join(HERE, "a7s_backplane.kicad_pcb")
FPROOT = os.environ["KICAD_FP"]                      # nix footprints dir (set by kpython)
A7SLIB = os.path.join(HERE, "..", "a7s.pretty")      # project footprints

def mm(v): return pcbnew.FromMM(v)
def VEC(x, y): return pcbnew.VECTOR2I(mm(x), mm(y))

# ---- coordinate transform: STEP frame -> KiCad frame ----
# STEP: X right, Y "up" is less-negative; board X[-23.31,27.49] Y[-29.68,-80.48].
# KiCad: Y increases downward. Use kx = sx + XOFF, ky = -sy  (so 30-pin top has smaller Y).
XOFF = 60.0
def T(sx, sy): return (sx + XOFF, -sy)

# ---- parse netlist ----
txt = open(NET).read()
comps = {}   # ref -> (libid, value)
for c in re.split(r'\n\s*\(comp\b', txt)[1:]:
    ref = re.search(r'\(ref "([^"]+)"\)', c)
    val = re.search(r'\(value "([^"]+)"\)', c)
    fp  = re.search(r'\(footprint "([^"]+)"\)', c)
    if ref and fp:
        comps[ref.group(1)] = (fp.group(1), val.group(1) if val else "")
nets = {}    # netname -> [(ref,pin)]
for b in re.split(r'\n\s*\(net\b', txt)[1:]:
    nm = re.search(r'\(name "([^"]+)"\)', b)
    nodes = re.findall(r'\(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)', b)
    if nm and nodes:
        nets[nm.group(1)] = nodes
print(f"parsed: {len(comps)} comps, {len(nets)} nets")

# ---- board ----
board = pcbnew.BOARD()
# net objects
netobj = {}
for nn in nets:
    ni = pcbnew.NETINFO_ITEM(board, nn)
    board.Add(ni)
    netobj[nn] = ni

def fp_path(libid):
    lib, name = libid.split(":")
    d = A7SLIB if lib == "a7s" else os.path.join(FPROOT, lib + ".pretty")
    return d, name

# ---- curated placement (KiCad mm). board X[1.5,87.5] Y[17.7,92.5];
#      A7S region X[36.7,87.5] Y[29.7,80.5]; bottom strip Y[82,92]; left overhang X[1.5,36.7].
j1x, j1y = T(2.11, -33.02)     # 30-pin top  -> (62.11, 33.02)
j2x, j2y = T(2.08, -78.71)     # 15-pin bottom -> (62.08, 78.71)
# Landscape 2.8" TFT direct-soldered (no socket): J3 = vertical 1x14 at LEFT, display body
# extends RIGHT covering the top ~2/3. Buttons + radios + input segments in the bottom strip.
# Joystick (J8) and Encoder (J10) on OPPOSITE edges -> 180deg deck flip swaps handedness.
# REAL display = full-width landscape 86x50 (J3 body-centered, header on its left edge).
# Top strip (tight) = Flipper header above the screen. Bottom strip = controls below the display.
# EFFICIENT placement: each movable header sits next to where its signals SOURCE (measured).
# Sources cluster center-right (SPI/radio/I2C x60-77 on J1+J2). Display header -> RIGHT edge.
# MODEL: display floats over the board (bezel). The whole SCREEN REGION on the BACK is packed
# with the connector headers + RP2040 + passives (modules hang in the gap/overhang -> thin device).
# Buttons live on the FRONT below the display's bottom edge. J1/J2 stay in-model on front (datums).
# PRINCIPLE: internals that need NO access (RP2040, passives) go CENTER / under the screen (back).
# Everything you plug into or touch goes to an EDGE: radios=TOP, Flipper=BOTTOM, joy+btn=LEFT, enc=RIGHT.
anchors = {
    "J1": (j1x, j1y, 90), "J2": (j2x, j2y, 90),   # A7S header datums (mate on back; in-model front)
    "J3": (44.5, 42.0, 0),                          # TFT header LEFT edge; body y17-67, right edge @ USB-C
    # --- UNDER SCREEN (back): internals, no access needed ---
    "A1": (44.0, 42.0, 90),                          # RP2040-Zero (back), dead-center under the display
    # --- EDGES (front): access-needers ---
    "J5": (16.0, 10.0, 90), "J5b": (24.0, 10.0, 0),   # Radio1 -> TOP-left edge, antenna up
    "J6": (70.0, 10.0, 90), "J6b": (62.0, 10.0, 0),   # Radio2 -> TOP-right edge, antenna up
    "J12": (44.0, 88.0, 90),                          # Flipper 18-pin -> BOTTOM edge, center
    "SW1": (16.0, 73.0, 0), "SW2": (27.0, 73.0, 0),   # buttons -> bottom, LEFT-grouped
    "SW3": (38.0, 73.0, 0), "SW4": (49.0, 73.0, 0),
    "J8":  (6.0, 84.0, 90),                          # JOY 1x5  -> LEFT edge
    "J11": (6.0, 90.0, 90),                          # BTN5/6   -> LEFT (with joystick)
    "J10": (82.0, 84.0, 90),                          # ENC 1x4  -> RIGHT edge (USB-C side)
    "TP1": (74.0, 73.0, 0), "TP2": (78.0, 73.0, 0),  # console pads
}
# passives packed on the BACK, under the screen, beside the RP2040 (internal, no access)
PACK_REGION  = (6.0, 24.0, 36.0)   # x_left, y_top, x_right (back, under display, left of A1)
PACK_ON_BACK = True
BACK_REFS    = {"A1","J1","J2","J5","J5b","J6","J6b","J8","J10","J11"}  # connector headers + RP2040 on the BACK; screen/Flipper/buttons stay front
ORIGIN_REFS  = {"J3"}             # custom fp, origin=body center -> place by origin (full-width body)

# ---- placement helpers (SetPosition sets ORIGIN=pad1, so we correct to bbox CENTER) ----
def cbox(fp):
    # True footprint extent = union of pad bboxes + graphical-item (silk/fab body outline) bboxes.
    # (GetCourtyard is unreliable for hand-written .kicad_mod; this is robust.)
    boxes = [p.GetBoundingBox() for p in fp.Pads()]
    try:
        boxes += [d.GetBoundingBox() for d in fp.GraphicalItems()]
    except Exception:
        pass
    L = min(b.GetLeft() for b in boxes);  R = max(b.GetRight() for b in boxes)
    T = min(b.GetTop()  for b in boxes);  B = max(b.GetBottom() for b in boxes)
    return (pcbnew.ToMM(L), pcbnew.ToMM(R), pcbnew.ToMM(T), pcbnew.ToMM(B))
def place_center(fp, cx, cy, rot=0):
    fp.SetOrientationDegrees(rot); fp.SetPosition(VEC(cx, cy))
    l,r,t,b = cbox(fp); dx = cx-(l+r)/2.0; dy = cy-(t+b)/2.0
    p = fp.GetPosition(); fp.SetPosition(pcbnew.VECTOR2I(p.x+mm(dx), p.y+mm(dy)))
def fp_wh(fp):
    l,r,t,b = cbox(fp); return r-l, b-t

placed = 0; missing = []; free = []
for ref,(libid,val) in comps.items():
    d, name = fp_path(libid)
    fp = pcbnew.FootprintLoad(d, name)
    if fp is None:
        missing.append(f"{ref}:{libid}"); continue
    fp.SetReference(ref); fp.SetValue(val); board.Add(fp)
    if ref in anchors:
        x,y,rot = anchors[ref]
        if ref in ORIGIN_REFS:                          # custom fp, origin=body center -> place origin
            fp.SetOrientationDegrees(rot); fp.SetPosition(VEC(x, y))
        else:
            place_center(fp, x, y, rot)
        if ref in BACK_REFS:
            fp.Flip(VEC(x, y), False)                   # flip about the ANCHOR (bbox center) -> position preserved
    else:
        free.append((ref, fp))
    placed += 1
print(f"placed {placed} footprints; missing: {missing}; free-to-pack: {len(free)}")

# ---- shelf-pack the free parts (passives) onto the BACK, under the display, no overlap ----
xL, yT, xR = PACK_REGION; M = 1.6
for _,fp in free:
    fp.SetOrientationDegrees(0)
    if PACK_ON_BACK: fp.Flip(fp.GetPosition(), False)   # move to B.Cu (underside)
free.sort(key=lambda t: fp_wh(t[1])[1], reverse=True)
cx, cy, rowh = xL, yT, 0.0
for ref, fp in free:
    w, h = fp_wh(fp)
    if cx + w > xR:                      # wrap to next shelf
        cx = xL; cy += rowh + M; rowh = 0.0
    place_center(fp, cx + w/2.0, cy + h/2.0, 0)
    cx += w + M; rowh = max(rowh, h)
print(f"packed {len(free)} parts on {'BACK' if PACK_ON_BACK else 'FRONT'}; bottom shelf y={cy:.1f}")

# ---- assign nets to pads ----
unmatched = 0
for nn, nodes in nets.items():
    ni = netobj[nn]
    for r,p in nodes:
        fp = board.FindFootprintByReference(r)
        if not fp: continue
        pad = fp.FindPadByNumber(p)
        if pad: pad.SetNet(ni)
        else: unmatched += 1
print("unmatched pads:", unmatched)

# ---- Edge.Cuts outline (STEP coords -> T) ----
# left overhang to ~-58.5; right at A7S edge +27.5; strips past top -29.68 and bottom -80.48
L,Rr = -58.5, 27.5
Tp,Bt = -4.0, -94.0      # top above radios, bottom below flipper; display floats center
corners_step = [(L,Tp),(Rr,Tp),(Rr,Bt),(L,Bt)]
pts = [T(sx,sy) for sx,sy in corners_step]
for i in range(4):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetStart(VEC(*pts[i])); seg.SetEnd(VEC(*pts[(i+1)%4]))
    seg.SetLayer(pcbnew.Edge_Cuts); seg.SetWidth(mm(0.15))
    board.Add(seg)

# ---- mounting holes ----
holes_step = [(-19.81,-33.18),(23.99,-33.18),(-19.81,-76.98),(23.99,-76.98)]
mh_dir = os.path.join(FPROOT, "MountingHole.pretty")
mh_name = None
for cand in ["MountingHole_2.7mm_M2.5","MountingHole_2.7mm_M2.5_Pad","MountingHole_2.7mm"]:
    if os.path.exists(os.path.join(mh_dir, cand+".kicad_mod")): mh_name = cand; break
for i,(sx,sy) in enumerate(holes_step,1):
    x,y = T(sx,sy)
    if mh_name:
        h = pcbnew.FootprintLoad(mh_dir, mh_name); h.SetReference(f"H{i}")
        board.Add(h); h.SetPosition(VEC(x,y))
    else:
        c = pcbnew.PCB_SHAPE(board); c.SetShape(pcbnew.SHAPE_T_CIRCLE)
        c.SetCenter(VEC(x,y)); c.SetEnd(VEC(x+1.35,y)); c.SetLayer(pcbnew.Edge_Cuts)
        c.SetWidth(mm(0.15)); board.Add(c)
print("mounting holes:", "fp="+mh_name if mh_name else "edge-circles")

pcbnew.SaveBoard(OUT, board)
print("saved", OUT)
