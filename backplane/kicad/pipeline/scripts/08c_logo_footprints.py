"""Build silkscreen logo footprints from potrace GeoJSON traces (step 8c).

Recipes (potrace + imagemagick via `nix shell nixpkgs#potrace nixpkgs#imagemagick`):

Amnesia brain (~/Amnesia-Labs/b&W.png, black-on-white line art, ~18px strokes @1423px):
  magick 'b&W.png' -alpha off -colorspace Gray -threshold 50% -trim +repage logo_trim.png
  magick logo_trim.png logo_w20.pbm                              # 20mm: 0.25mm strokes
  magick logo_trim.png -morphology Erode Disk:3 logo_w12.pbm     # 12mm: thicken -> 0.20mm
  potrace -b geojson -t 50 -o logo_wNN.json logo_wNN.pbm

DEF CON 34 jack (1080px color-on-black jpeg, ~14px strokes / ~8px gaps @982px):
  magick dc34_hires.img -colorspace Gray -gaussian-blur 0x0.8 -threshold 12% -negate \
         -trim +repage dc34_mono.png
  magick dc34_mono.png dc34_w30.pbm                              # 30mm: raw
  magick dc34_mono.png -morphology Dilate Disk:1 dc34_w20.pbm    # 20mm: widen white gaps
  potrace -b geojson -t 30 -o dc34_wNN.json dc34_wNN.pbm
  # 20mm is the floor for this art (0.28mm strokes / 0.16mm gaps)

Run with tools/kpython (edit SP to where the .json traces live). Each variant
becomes a .kicad_mod in backplane/a7s.pretty: filled fp_poly art on F.SilkS,
centered on origin. Place with `A` in pcbnew; `F` flips to the back.
GOTCHAS: pcbnew Import Graphics CRASHES on complex SVGs -- use this offline
route. fp_poly persists ONE outline per shape: emit one PCB_SHAPE per
fractured outline or all but one disjoint island silently vanish on save.
IM morphology on black-art-on-white: Erode grows black, Dilate grows white.
"""
import json
import sys
import pcbnew

SP = '/tmp/claude-1000/-home-skitz0-Projects-a7s-cyberdeck/8a1df0af-f493-4eeb-9b2c-832eaff555d0/scratchpad'
LIB = '/home/skitz0/Projects/a7s-cyberdeck/backplane/a7s.pretty'

def chain_from_ring(ring, sx, sy, h_px, off_x, off_y):
    ch = pcbnew.SHAPE_LINE_CHAIN()
    pts = ring[:-1] if ring[0] == ring[-1] else ring
    for x, y in pts:
        # potrace geojson is y-up; KiCad is y-down
        mx = x * sx - off_x
        my = (h_px - y) * sy - off_y
        ch.Append(pcbnew.FromMM(mx), pcbnew.FromMM(my))
    ch.SetClosed(True)
    return ch

def build(json_path, name, width_mm):
    d = json.load(open(json_path))
    polys = []
    for f in d['features']:
        g = f['geometry']
        if g['type'] == 'Polygon':
            polys.append(g['coordinates'])
        else:
            polys.extend(g['coordinates'])
    xs = [c[0] for p in polys for r in p for c in r]
    ys = [c[1] for p in polys for r in p for c in r]
    w_px, h_px = max(xs) - min(xs), max(ys) - min(ys)
    s = width_mm / w_px
    off_x, off_y = w_px * s / 2, h_px * s / 2

    sps = pcbnew.SHAPE_POLY_SET()
    for rings in polys:
        idx = sps.AddOutline(chain_from_ring(rings[0], s, s, h_px, off_x, off_y))
        for hole in rings[1:]:
            sps.AddHole(chain_from_ring(hole, s, s, h_px, off_x, off_y), idx)
    try:
        sps.Fracture(pcbnew.SHAPE_POLY_SET.PM_FAST)
    except (AttributeError, TypeError):
        sps.Fracture()

    board = pcbnew.BOARD()
    fp = pcbnew.FOOTPRINT(board)
    fp.SetFPID(pcbnew.LIB_ID('', name))
    fp.SetAttributes(pcbnew.FP_EXCLUDE_FROM_BOM | pcbnew.FP_EXCLUDE_FROM_POS_FILES | pcbnew.FP_BOARD_ONLY)
    fp.SetLibDescription(f'Amnesia Labs brain logo, {width_mm} mm wide, silkscreen art')

    # one PCB_SHAPE per outline: fp_poly persists only a single outline each
    for i in range(sps.OutlineCount()):
        single = pcbnew.SHAPE_POLY_SET()
        single.AddOutline(sps.Outline(i))
        shape = pcbnew.PCB_SHAPE(fp, pcbnew.SHAPE_T_POLY)
        shape.SetPolyShape(single)
        shape.SetFilled(True)
        shape.SetWidth(0)
        shape.SetLayer(pcbnew.F_SilkS)
        fp.Add(shape)

    ht = h_px * s
    fp.Reference().SetText('G***')
    fp.Reference().SetLayer(pcbnew.F_Fab)
    fp.Reference().SetPosition(pcbnew.VECTOR2I(0, pcbnew.FromMM(-(ht / 2 + 1.5))))
    fp.Value().SetText(name)
    fp.Value().SetLayer(pcbnew.F_Fab)
    fp.Value().SetPosition(pcbnew.VECTOR2I(0, pcbnew.FromMM(ht / 2 + 1.5)))

    io = pcbnew.PCB_IO_KICAD_SEXPR()
    io.FootprintSave(LIB, fp)
    print(f'{name}: {width_mm} x {ht:.1f} mm, {sps.OutlineCount()} outlines after fracture -> {LIB}/{name}.kicad_mod')

build(f'{SP}/logo_w20.json', 'AMNESIA_BRAIN_W20', 20.0)
build(f'{SP}/logo_w12.json', 'AMNESIA_BRAIN_W12', 12.0)

build(f'{SP}/dc34_w20.json', 'DC34_JACK_W20', 20.0)
build(f'{SP}/dc34_w30.json', 'DC34_JACK_W30', 30.0)
