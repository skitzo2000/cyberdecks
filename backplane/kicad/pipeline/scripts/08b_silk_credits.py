"""Add v2 credits + easter-egg silkscreen text to the routed backplane.

Back side gets the title/designer block (right of the RP2040), the
special-thanks block (left of the RP2040), the Flipper-footprint credit
behind J12, and the rev1 memorial -- all mirrored so they read correctly
viewed from the bottom. Front gets a brand/rev line + HACK THE PLANET along
the bottom edge (the only front strip not hidden by the TFT: the strip under
the J12 pin labels is occupied -- those labels are rotated vertical).
"""
import pcbnew

BOARD = '/home/skitz0/Projects/a7s-cyberdeck/backplane/kicad/a7s_backplane_routed.kicad_pcb'
b = pcbnew.LoadBoard(BOARD)
F = b.GetLayerID('F.Silkscreen')
B = b.GetLayerID('B.Silkscreen')

def add(text, x, y, layer, size=0.9, thick=0.15):
    t = pcbnew.PCB_TEXT(b)
    t.SetText(text)
    t.SetLayer(layer)
    t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
    t.SetTextThickness(pcbnew.FromMM(thick))
    t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
    t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
    if layer == B:
        t.SetMirrored(True)
    b.Add(t)
    return t

# --- BACK: title / designer block, right of the RP2040 (zone x52.5..74.5, y48.5..64) ---
TX = 63.5
add('A7S CYBERDECK',      TX, 50.0, B, size=1.4, thick=0.25)
add('BACKPLANE  REV 2',   TX, 52.8, B, size=1.2, thick=0.20)
add('DESIGNED BY SKITZ0', TX, 55.6, B, size=0.9)
add('AMNESIA-LABS.COM',   TX, 57.8, B, size=0.9)

# --- BACK: special-thanks block, left of the RP2040 (zone x7.5..28, y48.5..64) ---
KX = 17.5
add('SPECIAL THANKS TO',   KX, 50.0, B, size=0.9)
add('ART, TWON, CYRUS,',   KX, 52.2, B, size=0.9)
add('XCHAOS & THE ENTIRE', KX, 54.4, B, size=0.9)
add('HACKERS GUILD PGH',   KX, 56.6, B, size=0.9)
add('CREW!',               KX, 58.8, B, size=0.9)

# --- BACK: Flipper footprint credit, behind the J12 header ---
add('FLIPPER GPIO: KBEMBEDDED/FLIPPER-GPIO-EDA', 36.05, 28.8, B, size=0.8)

# --- FRONT: brand + rev line along the bottom edge (visible control face) ---
add('A7S CYBERDECK BACKPLANE REV 2 - AMNESIA-LABS.COM', 40.5, 92.95, F, size=0.8)

# --- FRONT: easter egg, right segment of the bottom edge ---
add('HACK THE PLANET', 67.0, 92.95, F, size=0.8)

# --- BACK: rev1 memorial easter egg, strip between the fuses and J2 ---
add('RIP REV 1: MIRRORED & SHORTED', 30.0, 75.6, B, size=0.8)

pcbnew.SaveBoard(BOARD, b)
print('saved', BOARD)

# report bboxes of what we added for a clearance sanity check
mm = pcbnew.ToMM
for d in b.GetDrawings():
    if isinstance(d, pcbnew.PCB_TEXT) and d.GetText().startswith(('A7S', 'BACKPLANE', 'DESIGNED', 'AMNESIA', 'SPECIAL', 'ART,', 'XCHAOS', 'HACKERS', 'CREW', 'FLIPPER GPIO:', 'RIP', 'HACK')):
        bb = d.GetBoundingBox()
        print(f"{d.GetLayerName():14s} x {mm(bb.GetLeft()):6.2f}..{mm(bb.GetRight()):6.2f}  y {mm(bb.GetTop()):6.2f}..{mm(bb.GetBottom()):6.2f}  '{d.GetText()}'")
