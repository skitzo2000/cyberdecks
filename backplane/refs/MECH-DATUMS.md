# A7S Mechanical Datums — measured from STEP v1.10

Source: `radxa_cubie_a7s_3d_stp_v1.10.stp` via FreeCAD (`/tmp/measure_headers.py`, `/tmp/find_30pin.py`).
All in the **STEP coordinate frame**, mm. Validated by mounting holes = 43.8 mm square.

## Board
- Outline: **X ∈ [−23.31, +27.49], Y ∈ [−29.68, −80.48]** → 50.8 × 50.8 mm.
- Center: (2.09, −55.08).
- Edges: **TOP** Y≈−29.68, **BOTTOM** Y≈−80.48, **LEFT** X≈−23.31, **RIGHT** X≈+27.49.

## Mounting holes — Ø2.7 (4.5 pad), 43.8 × 43.8 square
| # | X | Y |
|---|---|---|
| TL | −19.81 | −33.18 |
| TR | +23.99 | −33.18 |
| BL | −19.81 | −76.98 |
| BR | +23.99 | −76.98 |

## GPIO headers (the shield mates these) — both X-centered ≈ board center
| Header | Part label | Center | Pin field (approx) | Body bbox |
|---|---|---|---|---|
| **30-pin (2×15)** | `1555298` | **(2.11, −33.02)** | X −15.7…+19.9 (15 cols @2.54), rows Y ≈ −31.75 / −34.29 | X[−16.7, 21.0] Y[−36.4, −29.7], Z −9.7..0 (TH) |
| **15-pin (1×15)** | `HDR-TH_15P-P2_54-V-M` | **(2.08, −78.71)** | X −15.7…+19.9 (15 @2.54), row Y ≈ −78.7 | X[−17.0, 21.1] Y[−80.0, −77.5], Z −8..3.5 (TH) |

- Both span the **same X window** (~−16 … +21) → vertically aligned columns top & bottom.
- **TODO (pin-1):** confirm which end/row is pin-1 + exact pitch origin by extracting individual pin
  solids (or from schematic v1.10) before locking the shield footprint mirror.

## Ports (all RIGHT edge — protrude to X≈+31.5) → overhang LEFT
| Port | Center | Notes |
|---|---|---|
| USB-C #1 | (24.51, −39.61) | `BUSF242B3N11735-USB3_TYPE_C` |
| USB-C #2 | (24.51, −46.11) | second Type-C |
| USB-A | (24.69, −53.83) | TH |
| RJ45 (Ethernet) | (20.86, −66.55) | `LPJG0926HENL` MagJack |
| Camera FPC (31P) | (−20.46, −51.28) | LEFT edge |
| u.FL (RF_SM3) | (−19.71, −58.42) | LEFT side |

## Shield placement implications
- Shield female sockets: 2×15 at (2.11, −33.02), 1×15 at (2.08, −78.71) — **in the shield's frame these
  are MIRRORED about the mating axis** (shield flips onto the A7S); apply the mirror at KiCad placement.
- Right edge of the shield must clear ports out to **X ≈ +31.5** (don't extend the PCB over them).
- Overhang LEFT (past X=−23.31) for the TFT; top + bottom control strips past Y=−29.68 / −80.48.
- Stack height: headers are TH; top-side tallest nearby part heights TBD per-region if needed.
