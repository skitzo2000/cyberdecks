# How the v2 board was made (reproducible pipeline)

This documents **exactly** how `kicad/a7s_backplane_routed.kicad_pcb` (the current v2 board) was produced,
so it can be reproduced or audited. The one-off scripts for each step are in [`scripts/`](scripts/).

**Key fact:** v2 was **not** built fresh from `build_pcb.py`. Its auto-placement is a rough netlist dump
(parts off-board, everything overlapping). The usable placement was always **hand-done in KiCad**. So v2
started from the previous *routed* board (`v1/kicad/a7s_backplane_render.kicad_pcb`) and was corrected +
re-placed + re-routed. `build_pcb.py` was only used for the header-orientation fix logic and stays the
netlist→initial-placement generator.

## Toolchain

| Tool | How it's run | For |
|---|---|---|
| **pcbnew** (KiCad 10 Python) | `tools/kpython <script>` (sets `PYTHONPATH`/`KICAD_FP`/`KICAD_SYM` from the nix store) | all board edits |
| **kicad-cli** | on `$PATH` | DRC, gerbers, drill, renders, sch export |
| **freerouting 2.2.4** | `freerouting` on `$PATH` | autorouting |
| **SKiDL 2.2.3** | `docker run --rm -e HOME=/tmp -v "$PWD":/work -w /work a7s-skidl python3 …` | netlist |
| **kiutils** (pip) | in a venv, with `KICAD_SYM` set | generating the `.kicad_sch` |

## The pipeline (in order)

Run each `scripts/NN_*.py` with `tools/kpython` unless noted. Filenames are hardcoded in the scripts — read
the top of each before running.

**0. Netlist (only if connectivity changed).** `docker run … a7s-skidl python3 a7s_backplane_skidl.py` → `a7s_backplane.net`. The netlist is the connectivity source of truth for every step below.

**1. Fix the header mate + make a clean placement canvas** — `scripts/01_fix_headers_zero_net.py`
Loads the render board; re-orients **J1 → north / J2 → south, centered between their mounting holes, mirrored E-W** (the DOA-shorting bug fix); strips all tracks and zeroes all pad nets so you can place freely without a ratsnest. Verifies J1-pin1 aligns E-W with J2-pin15 and that the headers clear the mounting holes.

**2. Group logical assemblies** — `scripts/02a_group_assemblies.py` then `scripts/02b_group_singles.py`
Puts each logical unit in a KiCad `PCB_GROUP` (A7S = J1+J2+H1–H4, RP2040, TFT, BUTTONS, RADIO1/2, JOY, ENC, BTN, each cap/fuse/TP) so a click drags the whole part. **Do NOT lock footprints instead** — locked footprints become click-through (you select the pad, not the part).

**3. Overlay the A7S body + ports as a placement reference** — `scripts/03_overlay_a7s_ref.py`
Draws the A7S PCB outline + ETH/USB ports on `Dwgs.User`, mapped through the 4 mounting holes, and prints the ethernet-edge vs PCB-edge gap. Used to align the A7S **1.75 mm west** so the RJ45 edge meets the board edge. (Overlay is removed before fab.)

**4. Hand-place in pcbnew.** Open the board, drag the groups where they go (arrow keys / `M` / Ctrl-M "Move Exactly" for precise nudges), save.

**5. Re-apply the nets** — `scripts/04_reapply_nets.py`
Copies connectivity from the render board back onto the placed board **by (ref, pin)** — position-independent, so it doesn't matter where parts moved. Writes `a7s_backplane_v2.kicad_pcb`.

**6. Export DSN → route → import SES.**
```sh
tools/kpython -c "import pcbnew;b=pcbnew.LoadBoard('kicad/a7s_backplane_v2.kicad_pcb');pcbnew.ExportSpecctraDSN(b,'kicad/a7s_backplane_v2.dsn')"
freerouting -de kicad/a7s_backplane_v2.dsn -do kicad/a7s_backplane_v2.ses -mp 15    # MUST be foreground
tools/kpython -c "import pcbnew;b=pcbnew.LoadBoard('kicad/a7s_backplane_v2.kicad_pcb');pcbnew.ImportSpecctraSES(b,'kicad/a7s_backplane_v2.ses');pcbnew.SaveBoard('kicad/a7s_backplane_routed.kicad_pcb',b)"
```

**7. Restore the board outline** — `scripts/07_restore_edge_cuts.py`
`ImportSpecctraSES` silently drops Edge.Cuts segments; this re-adds the south + west edges to close the rectangle. Always re-verify the outline after a route round-trip.

**8. Silkscreen labels** — `scripts/08_silk_labels.py`
Adds a net/function label tight to every pin (Flipper-header style: ~1.5 mm off the pad, 0.8 mm font), grounds ringed. Back-side parts on `B.SilkS` (mirrored), TFT on `F.SilkS`. Single-column connectors label to the interior side; button rows label above.

**9. Schematic (.kicad_sch)** — `scripts/09_gen_schematic.py` (a copy of `tools/gen_kicad_schematic.py`)
Generates the editable `a7s_backplane.kicad_sch` from the netlist with kiutils: every component as its stock symbol (RP2040 as a custom box), a global net-label on a wire stub off each pin. Needs the kiutils venv + `KICAD_SYM`.

**10. DRC + fab + renders.**
```sh
kicad-cli pcb drc --format json --severity-error --severity-warning -o drc.json kicad/a7s_backplane_routed.kicad_pcb
kicad-cli pcb export gerbers -o kicad/fab_v2/ kicad/a7s_backplane_routed.kicad_pcb
kicad-cli pcb export drill --format excellon --excellon-separate-th -o kicad/fab_v2/ kicad/a7s_backplane_routed.kicad_pcb
kicad-cli pcb render --side top    --quality high -o kicad/renders/routed_top.png    kicad/a7s_backplane_routed.kicad_pcb
kicad-cli pcb render --side bottom --quality high -o kicad/renders/routed_bottom.png kicad/a7s_backplane_routed.kicad_pcb
```

## Gotchas (each cost real time)

- **freerouting only routes when launched FOREGROUND.** `nohup`/background dies silently. It went 96 → 0 unrouted in ~30 s foreground.
- **`ImportSpecctraSES` silently drops Edge.Cuts** — re-run step 7 and check the outline is closed.
- **Never lock footprints for hand-placement** — locked = click-through (grabs the pad, not the part). Use `PCB_GROUP`s (step 2).
- **`pcbnew`'s process name is the full nix path**, so `pgrep -x pcbnew` false-negatives — match `bin/pcbnew`. Launch with `nohup pcbnew <file> &`.
- **DRC courtyard "errors" are benign** — the TFT (J3) footprint courtyard is the whole floating display, so every part beneath it flags `pth_inside_courtyard`. Not collisions.
- **kiutils quirks** (schematic gen): `Font(height=,width=)` — the 1st positional arg is `face`; unit sub-symbols must be `Part` (kiutils appends `_unitId_styleId`), no lib prefix on units. SKiDL's own `generate_schematic()` is broken.
- **Do not re-run `build_pcb.py` on a placed/routed board** — it emits a rough placed-but-unrouted board and discards the hand-placement + routing.
