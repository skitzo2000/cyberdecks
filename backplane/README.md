#  A7S Cyberdeck Backplane

A hand-solderable backplane **shield for the [Radxa Cubie A7S](https://radxa.com/products/cubie/a7s/)**
(Allwinner A733). It fans the A7S's 45 header pins out into a cyberdeck I/O board: dual swappable
radios, an input MCU, a touchscreen, and a Flipper-compatible expansion header.

> **Current board: [rev2](REV2.md)** — schematic/netlist complete and verified; PCB placed and **fully
> routed** (0 unconnected); fab package generated. **Not yet fab-verified** — see the rev2
> [Before you fabricate](REV2.md#before-you-fabricate) checklist before ordering.

---

## Revisions

The two revisions share a **byte-for-byte identical netlist / schematic / BOM** — only the physical layout
differs. All the electrical docs below apply to both; each rev doc covers just what's version-specific
(layout, fab files, renders, status).

| Rev | Status | What / why | Doc |
|---|---|---|---|
| **rev2** | **current** | A7S rotated 180° so USB-C/USB-A/RJ45 **ports face outward**; mount shifted 3 mm for edge clearance | **[REV2.md](REV2.md)** |
| rev1 | frozen / superseded | original layout — **ports face inward** into the radios (mistake); kept for reference only, **do not fab** | [REV1.md](REV1.md) |

**Shared (both revs):** [SCHEMATIC.md](SCHEMATIC.md) · [SCHEMATIC-DIAGRAM.md](SCHEMATIC-DIAGRAM.md) ·
[BACKPLANE-DESIGN.md](BACKPLANE-DESIGN.md) · [BOM-SHIELD.md](BOM-SHIELD.md) · [BOM-DECK.md](BOM-DECK.md)

---

## Features

| Block | Detail |
|---|---|
| **2× "8+1" radio sockets** | Shared SPI1. Drop-in for **nRF24L01+ / CC1101 / CC2500** (8-pin nRF24 pin order + an AUX pin 9 for ESP-01 / breadboard use). Both radios can run simultaneously. |
| **RP2040-Zero input MCU** | Human inputs **only** — 4 on-board buttons + 2 off-board, joystick, rotary encoder. It is *not* a radio bridge; every radio line maps straight to an A7S header pin. |
| **2.8" SPI TFT** | ILI9341 display with resistive (XPT2046) touch. |
| **Flipper GPIO header** | Real two-connector layout (1×8 + 1×10, 17.78 mm gap) as a **female socket**, on the front, so genuine Flipper-ecosystem add-ons mate. |
| **Power** | Taps **5 V and 3V3 from the A7S header** (an external battery powers the A7S over its own USB-C port). Radio rails are polyfused. |

## Design choices

- **All through-hole / hand-solder.** No SMD, no pick-and-place — it's a backplane you solder to.
- **2-layer**, designed to be routed on two sides.
- Schematic/netlist generated with **[SKiDL](https://github.com/devbisme/skidl)**; board built with the
  KiCad **pcbnew** Python API; autorouted headless with **[freerouting](https://github.com/freerouting/freerouting)**.
- A7S header geometry sits on **STEP-measured datums** (`refs/MECH-DATUMS.md`) so the shield mates correctly.

## Repository layout

```
README.md                this index
REV2.md                  rev2 board — current (layout, fab package, verification)
REV1.md                  rev1 board — frozen / superseded (the port-orientation mistake)
BACKPLANE-DESIGN.md      full design doc  (shared — netlist identical across revs)
SCHEMATIC.md             authoritative netlist / connectivity (source of truth)
SCHEMATIC-DIAGRAM.md     generated connectivity + bus diagrams
BOM-SHIELD.md            shield parts list (sourcing links, no prices)
BOM-DECK.md              full-deck system parts list (sourcing links, no prices)
a7s_backplane_skidl.py   netlist generator  ->  a7s_backplane.net
kicad/                   pcbnew boards, build_pcb.py, gerbers, fab_rev2/, renders
a7s.pretty/              custom footprints (TFT, RP2040-Zero, Flipper — see ATTRIBUTION.md)
refs/                    measured mechanical datums
tools/                   kpython wrapper (runs pcbnew against the nix KiCad libs)
```

## Build / regenerate

```sh
# 1. netlist (after editing the schematic) — shared by both revs
skidl-python a7s_backplane_skidl.py            # -> a7s_backplane.net

# 2. board from the netlist
tools/kpython kicad/build_pcb.py               # -> kicad/a7s_backplane.kicad_pcb

# 3. route (headless): export DSN -> freerouting -> import SES
tools/kpython -c "import pcbnew;b=pcbnew.LoadBoard('kicad/a7s_backplane.kicad_pcb');pcbnew.ExportSpecctraDSN(b,'kicad/a7s_backplane.dsn')"
freerouting -de kicad/a7s_backplane.dsn -do kicad/a7s_backplane.ses -mp 100 -mt 4
tools/kpython -c "import pcbnew;b=pcbnew.LoadBoard('kicad/a7s_backplane.kicad_pcb');pcbnew.ImportSpecctraSES(b,'kicad/a7s_backplane.ses');pcbnew.SaveBoard('kicad/a7s_backplane.kicad_pcb',b)"
```

> The current board (rev2) was built from the frozen rev1 layout with a one-shot rotate + shift, then
> re-routed — see [REV2.md § Regenerating](REV2.md#regenerating-rev2). Do **not** re-run `build_pcb.py`
> against a routed board (it emits a placed-but-unrouted board and loses all routing).

## Additional Notes

I think the radio headers belong in the left top corner so that any radio chips you plug in will be standing up vertically behind the deck & 90 degrees from the flipper headers becuase radio likes angles.

Yes its a lot of IO, I wanted to max out what was available in the friendliest way possible supporting cheap available modules that already exist in the market.

## Credits

Flipper GPIO footprints from **[kbembedded/flipper-gpio-eda](https://github.com/kbembedded/flipper-gpio-eda)**
(BSD-2-Clause) — see [`a7s.pretty/ATTRIBUTION.md`](./a7s.pretty/ATTRIBUTION.md). All other footprints are
original to this project.
