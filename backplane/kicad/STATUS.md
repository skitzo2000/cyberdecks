# KiCad board — status

Headless-generated from `../a7s_backplane.net` via `build_pcb.py` (KiCad 10 `pcbnew` API,
run with `../tools/kpython`). Open `a7s_backplane.kicad_pcb` in KiCad 10 pcbnew.

## Regenerate
```
cd ..                              # backplane/
skidl-python a7s_backplane_skidl.py        # -> a7s_backplane.net  (if schematic changed)
tools/kpython kicad/build_pcb.py           # -> kicad/a7s_backplane.kicad_pcb
kicad-cli pcb render --side top -o kicad/render_top.png kicad/a7s_backplane.kicad_pcb
kicad-cli pcb drc --format json -o kicad/drc.json kicad/a7s_backplane.kicad_pcb
```

## DONE (this milestone: placed + full ratsnest)
- 36 components + 4 mounting holes instantiated; **0 missing footprints, 0 unmatched pads**.
- All 50 nets assigned to pads (ratsnest complete) — connectivity matches SCHEMATIC.md.
- **Anchored on STEP-measured datums:** J1 (30-pin) @ (2.11,−33.02), J2 (15-pin) @ (2.08,−78.71);
  4× M2.5 mounting holes at the 43.8 mm square; Edge.Cuts outline 86.2 × 75.0 mm
  (overhang-left + top/bottom strips, right edge at the A7S edge so ports stay clear).
- Coordinate transform STEP→KiCad: `kx = sx + 60`, `ky = −sy`.
- Rough-clustered the rest (power/passives left-overhang, RP2040 center, 4 buttons + radios bottom strip).

## Placement refined (center-based + shelf-packer)
- Footprints placed by COURTYARD CENTER (SetPosition sets origin=pad1, so we correct to center).
- Anchors fixed: J1/J2 on datums (verified centers 62.11,33.02 / 62.08,78.71), J3 TFT, A1 RP2040,
  SW1-4 bottom-center, J5/J6(+AUX) flanking, J8 left-edge field. Rest shelf-packed in the left
  overhang using real courtyard sizes (no overlap).
- **DRC: 6 violations total** — 4 courtyards_overlap = INHERENT (mounting holes H1-H4 sit ~0.7mm from
  the J1/J2 header ends, real A7S geometry; datums can't move) + 2 silk_over_copper (trivial).
  121 unconnected = the ratsnest (routing is the next phase). Down from 317.


## ROUTED (freerouting batch) — milestone
- Flow: `pcbnew.ExportSpecctraDSN` -> `freerouting -de in.dsn -do out.ses -mp 100 -mt 4` -> `pcbnew.ImportSpecctraSES` -> save `a7s_backplane_routed.kicad_pcb`.
- **kicad-cli pcb export specctra is GONE in KiCad 10** -> use the pcbnew Python API for DSN/SES.
- freerouting 2.2.4: `--help` launches the GUI (hangs); BATCH mode = `-de`/`-do`/`-mp`/`-mt` runs headless+exits. `-dr` expects a RULES FILE arg (don't pass bare).
- Result: 0 unrouted (5 passes, 13.8s, score 992.67); **661 tracks, 32 vias**.
- DRC on routed board: **0 unconnected**, 6 violations = the same 4 inherent hole<->header courtyards + 2 silk (cosmetic). Render kicad/render_routed.png.
- Files: a7s_backplane_routed.kicad_pcb (+ .kicad_pro), a7s_backplane.dsn, a7s_backplane.ses.

## TODO (next phases)
1. **Manual placement refinement** in pcbnew — spread parts (kill courtyard/silk/short overlaps),
   finalize the bottom-strip ergonomics, place decoupling next to its IC.
2. **Route** (no headless autorouter): hand-route, or export DSN → freerouting → import SES.
3. **Real symbols/footprints** (currently provisional, name-stable):
   - `a7s:RP2040_Zero` is a 2×12 socket stand-in — replace geometry with the true Waveshare
     RP2040-Zero castellation order; reconcile A1 pin map (currently sequential index).
   - U2 load switch: footprint is a real SOT-23-6, but confirm the TPS22918 pin order (1=VIN 2=GND
     3=ON 6=VOUT assumed) and add a proper symbol if regenerating the schematic.
4. **Verify header pin-1** end/row vs the A7S (extract pin solids / schematic v1.10) before fab — the
   datum centers are exact but pin-1 orientation must match so the shield mates.
5. **Ambidextrous duplicate strip** — add the second (DNP) control-strip footprints on the top overhang
   (same nets) per design §9.
6. ERC/BOM/Gerbers via `kicad-cli` once routed.
```
