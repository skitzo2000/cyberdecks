# A7S Backplane — **rev2** (current)

**Status:** placed, **fully routed (0 unconnected)**, fab package generated. **Not yet fab-verified** —
review the [Before you fabricate](#before-you-fabricate) checklist before ordering.

rev2 is a **mechanical-only respin of [rev1](REV1.md)** that fixes a port-orientation mistake. The
**electrical design is byte-for-byte identical** to rev1 — same schematic, same netlist, same BOM (verified:
the 160-pad → net map and the 26-component set match rev1 exactly). Only footprint *placement* changed. For
the connectivity, pin maps, buses, power tree, and parts, see the shared docs:

- [SCHEMATIC.md](SCHEMATIC.md) — authoritative netlist / connectivity (source of truth)
- [SCHEMATIC-DIAGRAM.md](SCHEMATIC-DIAGRAM.md) — generated connectivity + bus diagrams
- [BACKPLANE-DESIGN.md](BACKPLANE-DESIGN.md) — full design doc + pin maps
- [BOM-SHIELD.md](BOM-SHIELD.md) / [BOM-DECK.md](BOM-DECK.md) — parts

---

## What changed from rev1

**The mistake (rev1):** the A7S was mounted so its **USB-C / USB-A / RJ45 ports faced *inward*** — toward
the radio sockets in the middle of the deck — instead of outward off a board edge. The ports were unusable.

**The fix (rev2):** **rotate the A7S 180°** so the ports face **outward** and overhang the board edge. This
is a **layout change, not a schematic change** — the A7S host sockets (J1/J2) rotate *together with* the A7S,
so pad-*N* still mates A7S-pin-*N* and the netlist is unchanged.

| Change | rev1 | rev2 | Detail |
|---|---|---|---|
| **A7S mount rotation** | J1/J2 @ ≈−90° | J1/J2 @ +90° | J1 (2×15) + J2 (1×15) **rotated 180°** about the mounting-hole-pattern center |
| **A7S mount + holes shift** | — | **−3.0 mm X** | J1, J2 **and** mounting holes H1–H4 shifted 3 mm **left** together, so the rotated ports sit **~1.3 mm proud** of the left board edge (clear, not fouling) |
| **Encoder J10 shift** | Y 87.0 | Y 90.0 | moved **+3.0 mm south** to clear the H2 mounting hole |
| Everything else | — | unchanged | TFT (J3), radios (J5/J6), joystick (J8), Flipper (J12), buttons (SW1–4), RP2040 (A1), power (F1/F2, C1/C2), test points — all in the **same place** |
| Board outline | 86.35 × 74.25 mm | 86.35 × 74.25 mm | **unchanged rectangle** (origin 1.32, 19.93); the A7S mount moved *within* it |

> The mounting holes sit on a symmetric 43.8 mm square, so the A7S still bolts to the same 4 holes after the
> 180° rotation — the holes just shift 3 mm with the mount. The rotation swaps the two header Y-bands.

---

## Preview (rev2 renders)

**Top / deck face** — A7S host sockets (J1 top 2×15, J2 bottom 1×15), the 4 face buttons SW1–4 along the
bottom, TFT footprint centered, test points TP1/TP2:

![rev2 top](../3dfiles/rev2_top.png)

**Iso** — shield + see-through TFT stacked over the A7S ghost outline:

![rev2 iso](../3dfiles/rev2_iso.png)

Bottom face: [`../3dfiles/rev2_bottom.png`](../3dfiles/rev2_bottom.png).

---

## Handedness (as built)

The board is a **single fixed layout with one control strip** (buttons SW1–4, one J-IN/J-BRK field). The
other hand is obtained by **physically rotating the whole deck 180°** and flipping the display in firmware —
**not** by a mirrored board variant. A true left/right **mirror was rejected for wiring reasons** (it
complicates the off-board control harness and the routing). This is a deliberate compromise over the earlier
dual-strip "ambidextrous" idea; see [BACKPLANE-DESIGN.md § Handedness](BACKPLANE-DESIGN.md#handedness--as-built-single-strip--180-deck-rotation-a-compromise).

---

## Verification (this rev)

Checked against the frozen rev1 board and the fab output:

| Check | Result |
|---|---|
| Unconnected pads | **0** |
| Routing | **486 track segments + 21 vias** (507 tracks) |
| Pad → net connectivity vs rev1 | **identical** (160/160 pads, 0 diff) |
| Component set vs rev1 | **identical** (26 refs) |
| A7S rotation | J1/J2 **exactly 180°** (−90° → +90°), mount/holes −3.0 mm X |
| DRC | 101 violations, **all cosmetic**: courtyard overlaps (screen body floats over back-side parts) + THT-in-courtyard — **no electrical / clearance errors**. Same profile as rev1. |

---

## Fab package

Everything an assembler needs is under **[`kicad/fab_rev2/`](kicad/fab_rev2/)**:

| File(s) | What |
|---|---|
| `a7s_backplane_rev2-*.g{tl,bl,ts,bs,to,bo,tp,bp}`, `-Edge_Cuts.gm1`, `-job.gbrjob` | Gerbers (2-layer) |
| `a7s_backplane_rev2.drl`, `-drl_map.gbr` | Excellon drill + drill map |
| `a7s_backplane_rev2-pos.csv` | Component positions (place file) |
| `a7s_backplane_rev2.d356` | IPC-D-356 netlist (bare-board test) |
| `a7s_backplane_rev2-fab.pdf` | Fab drawing |
| `a7s_backplane_rev2-bom.csv` | BOM (14 line items) |
| `a7s_backplane_rev2.step` / `.glb` | 3D models |
| `a7s_backplane_rev2-schematic.{svg,pdf,png}` | Schematic diagram |

**Bundles:** [`kicad/a7s_backplane_rev2-FULL.zip`](kicad/a7s_backplane_rev2-FULL.zip) (full package) and
`kicad/fab_rev2/a7s_backplane_rev2-gerbers.zip` (gerbers + drill only, for the board house). Loose gerbers
also in [`kicad/gerbers_rev2/`](kicad/gerbers_rev2/).

**Board / project:** [`kicad/a7s_backplane_rev2.kicad_pcb`](kicad/a7s_backplane_rev2.kicad_pcb) (+ `.kicad_pro`).
**Populated 3D** (for enclosure design): `../3dfiles/backplane_rev2_populated.step` / `.stl` (~290k tris).

---

## Regenerating rev2

rev2 was built **fresh from the frozen rev1 board** (do not edit in place — see the gotcha below), applying
the rotate + shift once, then re-routing headless:

```sh
# 1. copy frozen rev1 as the rev2 base, apply rotate(180° about mount center) + shift(-3mm X mount, +3mm Y J10)
#    (one-shot placement edit via pcbnew python; see session notes)

# 2. route headless: strip tracks -> export DSN -> freerouting -> import SES
tools/kpython -c "import pcbnew;b=pcbnew.LoadBoard('kicad/a7s_backplane_rev2.kicad_pcb');pcbnew.ExportSpecctraDSN(b,'kicad/a7s_backplane_rev2.dsn')"
freerouting -de kicad/a7s_backplane_rev2.dsn -do kicad/a7s_backplane_rev2.ses -mp 200 -oit 50
tools/kpython -c "import pcbnew;b=pcbnew.LoadBoard('kicad/a7s_backplane_rev2.kicad_pcb');pcbnew.ImportSpecctraSES(b,'kicad/a7s_backplane_rev2.ses');pcbnew.SaveBoard('kicad/a7s_backplane_rev2.kicad_pcb',b)"

# 3. fab outputs via kicad-cli (gerbers, drill, pos, ipc-d356, pdf, step, glb) -> kicad/fab_rev2/
```

> **Gotchas (learned the hard way):**
> - **Repeated in-place `pcbnew` edits corrupt the board** — symptom: freerouting returns an *identical*
>   score no matter what geometry you change. Fix: rebuild rev2 fresh from frozen rev1, apply changes **once**,
>   then route. Clear stray `*.rules` / `*.ses` between runs.
> - `kicad-cli` 10 dropped Specctra from the CLI — export/import DSN/SES via the `pcbnew` Python API (above).
> - The netlist is **not** regenerated for rev2. Do **not** re-run `kicad/build_pcb.py` (it emits a
>   placed-but-*unrouted* board and would lose all routing).

---

## Before you fabricate

rev2 has **not** been fab-verified. Check these first:

1. **Port clearance** — the whole point of rev2. Confirm on the real A7S STEP that the rotated USB-C/USB-A/RJ45
   **ports clear the board edge** (they should sit ~1.3 mm proud of the left edge) and that nothing on the
   shield fouls the port bodies.
2. **Header pin-1 orientation** vs the A7S — datum *centers* are exact; verify pin-1 end/row so the shield
   mates the right way round (`refs/MECH-DATUMS.md`).
3. **RP2040-Zero footprint row spacing** assumed **15.24 mm** — confirm against your module.
4. **Radio headers (J5/J6)** — two 2×4 "8+1" sockets, oriented 90° to each other; confirm module clearance.
5. **Flipper header (J12)** — 1×8 + 1×10 female, fixed 17.78 mm gap; keep spacing exact.
6. **DRC courtyard items are expected/cosmetic** — the TFT body courtyard floats over the back-side parts.
   Distinguish those from any real clearance error.
7. Give the routed board a **GUI review pass** in KiCad before ordering.

---

## Relationship to rev1

[rev1](REV1.md) is **frozen** (`kicad/a7s_backplane_render.*`, `kicad/gerbers/`) and kept for reference /
diff only — it should **not** be fabricated (ports face inward). rev2 supersedes it. Because the two share an
identical netlist, all electrical docs apply equally to both.
