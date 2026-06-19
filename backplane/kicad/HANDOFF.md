# Placement handoff — finish in the GUI

**Open:** `a7s_backplane.kicad_pcb` (the **placed, un-routed** board — full ratsnest, drag parts freely).
Do NOT use `a7s_backplane_routed.kicad_pcb` for placement — that's an old auto-route; we re-route after you place.

## What's already correct (don't need to touch unless you want to)
- **All nets/connections** are right (verified against `../SCHEMATIC.md`). The thin white airwires are the ratsnest — they follow parts as you drag.
- **J1 / J2** (A7S 30-pin / 15-pin sockets) are on the **STEP-measured datums** — leave these put; they mate the A7S. H1–H4 are the M2.5 mounting holes.
- Footprints are real: `a7s:TFT_2p8` (86×50 body, header on its left edge), `a7s:RP2040_Zero`.

## The layout principle (what I was aiming at — adjust to taste)
- **Under the screen / center → internals, no access:** RP2040 (A1) + passives (C1/C2/F1/F2). These are on the **back** (B.Cu). Keep them under the display footprint.
- **Edges → things you plug into or touch:** radios (J5/J6 + AUX J5b/J6b), Flipper (J12), buttons (SW1-4), joystick (J8), encoder (J10), BTN5/6 (J11).
- Your stated intent: **radios top, Flipper bottom, joystick+buttons left, encoder right (USB-C side)**, TFT right edge at the USB-C edge, TFT header pins on the left.

## How to move parts
- `M` = move, `R` = rotate, `F` = flip to other side (front/back). `E` = edit footprint props.
- Toggle **F.Cu / B.Cu** in the Layers panel (or **Alt+3** for the 3D view) to see front vs back.
- The display floats over the center on a bezel — its body courtyard overlapping the back parts is expected (ignore those `pth_inside_courtyard` DRC items).

## When you're done placing
Either:
- **Ping me** — I'll re-run freerouting + DRC headlessly and hand back the routed board, **or**
- Route it yourself, then `Inspect → DRC`.

Re-route command (what I'll run):
```
tools/kpython -c "import pcbnew;b=pcbnew.LoadBoard('kicad/a7s_backplane.kicad_pcb');pcbnew.ExportSpecctraDSN(b,'kicad/a7s_backplane.dsn')"
freerouting -de kicad/a7s_backplane.dsn -do kicad/a7s_backplane.ses -mp 100 -mt 4
tools/kpython -c "import pcbnew;b=pcbnew.LoadBoard('kicad/a7s_backplane.kicad_pcb');pcbnew.ImportSpecctraSES(b,'kicad/a7s_backplane.ses');pcbnew.SaveBoard('kicad/a7s_backplane_routed.kicad_pcb',b)"
```

## Notes / open items
- Board outline (Edge.Cuts) is a rectangle; resize/reshape it in the GUI as you settle the parts (Edge.Cuts layer).
- If you move J5/J6/J12 etc. to new spots, the ratsnest just follows — connectivity stays correct.
- Verify the RP2040-Zero footprint row-spacing vs the real module before fab (currently 15.24 mm assumed).
