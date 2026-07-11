#  A7S Cyberdeck Backplane

A hand-solderable backplane **shield for the [Radxa Cubie A7S](https://radxa.com/products/cubie/a7s/)**
(Allwinner A733). It fans the A7S's 45 header pins out into a cyberdeck I/O board: dual swappable
radios, an input MCU, a touchscreen, and a Flipper-compatible expansion header.

> **Current board: v2** — schematic/netlist complete; PCB placed and **fully routed** (0 unconnected);
> **DRC-clean**; fab package generated. It corrects the header-mirror short that made the earlier boards
> DOA (see [What v2 fixed](#what-v2-fixed)). **Not yet fab-verified** — order it and it should power on.

| | File |
|---|---|
| **Board (v2)** | [`kicad/a7s_backplane_routed.kicad_pcb`](kicad/a7s_backplane_routed.kicad_pcb) |
| **Fab package** | [`kicad/a7s_backplane_v2_fab.zip`](kicad/a7s_backplane_v2_fab.zip) — upload to JLCPCB/PCBWay |
| **Schematic (editable)** | [`a7s_backplane.kicad_sch`](a7s_backplane.kicad_sch) · [PDF](a7s_backplane_schematic_kicad.pdf) |
| **Renders** | [`kicad/renders/routed_top.png`](kicad/renders/routed_top.png) · [`routed_bottom.png`](kicad/renders/routed_bottom.png) |

---

## What v2 fixed

The earlier boards (archived in [`v1/`](v1/)) mated the A7S GPIO headers **mirrored** — the shield's
socket pin 1 landed where the A7S's pin 30 is. That put the A7S **+3V3 rail onto the shield's GND**, so
the SBC dead-shorted and went dark the instant the shield was seated. v2 corrects it:

- **30-pin (double) header → NORTH edge, 15-pin (single) → SOUTH edge, both mirrored east-west** so the
  socket now mates the A7S pin-for-pin (shield pad *P* → A7S pin *P*; grounds land on grounds).
- A7S cluster nudged **1.75 mm west** so the ethernet-port edge lines up with the PCB west edge (the
  board rests on/at the RJ45).
- Full silkscreen: every pin labeled tight to the pad, all grounds ringed.

The **electrical design (netlist / schematic / BOM) is unchanged** across all revs — only the layout and
this header-mate correction differ.

## Revisions

| Rev | Status | What | Where |
|---|---|---|---|
| **v2** | **current — routed, DRC-clean, fab-ready** | header-mirror fixed, A7S aligned to board edge, full silk | *this folder* |
| v1 | archived / **do not fab** | original rev1 (ports faced inward) + the rev2 respin — both still had the header-mirror short | [`v1/`](v1/) ([REV1](v1/REV1.md) · [REV2](v1/REV2.md)) |

**Shared electrical docs (apply to all revs):** [SCHEMATIC.md](SCHEMATIC.md) ·
[SCHEMATIC-DIAGRAM.md](SCHEMATIC-DIAGRAM.md) · [BACKPLANE-DESIGN.md](BACKPLANE-DESIGN.md) ·
[BOM-SHIELD.md](BOM-SHIELD.md) · [BOM-DECK.md](BOM-DECK.md)

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
- **2-layer**, routed on both sides.
- Schematic/netlist generated with **[SKiDL](https://github.com/devbisme/skidl)** (the source of truth);
  board built/edited with the KiCad **pcbnew** Python API; autorouted headless with
  **[freerouting](https://github.com/freerouting/freerouting)**.
- A7S header geometry sits on **STEP-measured datums** (`refs/MECH-DATUMS.md`) so the shield mates correctly.

## Repository layout

```
README.md                     this index (v2)
a7s_backplane_skidl.py        netlist generator (SOURCE OF TRUTH)  ->  a7s_backplane.net
a7s_backplane.kicad_sch       editable KiCad schematic (generated from the netlist, opens in Eeschema)
a7s_backplane_schematic_kicad.{pdf,png}   schematic exports (for people without KiCad)
a7s_backplane_schematic.{svg,pdf,png}     graphviz connectivity/bus diagram
BACKPLANE-DESIGN.md           full design doc + pin maps   (shared across revs)
SCHEMATIC.md                  authoritative connectivity    (shared)
BOM-SHIELD.md / BOM-DECK.md   parts lists (sourcing links)  (shared)
kicad/
  build_pcb.py                netlist -> initial placement (pcbnew); config-driven
  a7s_backplane_routed.kicad_pcb   THE v2 board (routed, labeled, outline closed)
  a7s_backplane_v2_fab.zip    gerbers + drills, ready to order
  fab_v2/                     unzipped fab outputs
  renders/                    3D top/bottom renders of v2
  pipeline/                   this session's working intermediates (placement/route steps)
  3d/                         STEP models (gitignored; large)
a7s.pretty/                   custom footprints (TFT, RP2040-Zero, Flipper — see ATTRIBUTION.md)
refs/                         measured mechanical datums
tools/                        kpython (runs pcbnew against nix KiCad libs) + gen_kicad_schematic.py
v1/                           ARCHIVE — old rev1 + rev2 boards/gerbers/fab/renders. Do not fab.
```

## Build / regenerate

> **Full step-by-step + the exact scripts:** [`kicad/pipeline/README.md`](kicad/pipeline/README.md).
> It documents precisely how v2 was made (header-mirror fix → hand-placement → re-net → freerouting →
> silk → schematic → fab) with the one-off scripts in `kicad/pipeline/scripts/` and every gotcha.

The electrical design lives in SKiDL; the **placement is hand-done in KiCad** (the autoplacer output is
only a rough starting point). Quick version:

```sh
# 1. netlist (after editing the schematic)  ->  a7s_backplane.net
docker run --rm -e HOME=/tmp -v "$PWD":/work -w /work a7s-skidl python3 a7s_backplane_skidl.py

# 2. editable KiCad schematic from the netlist (derived artifact)
#    (needs kiutils + KICAD_SYM; see tools/gen_kicad_schematic.py header)
python3 tools/gen_kicad_schematic.py            # -> a7s_backplane.kicad_sch

# 3. board: build_pcb.py gives a rough placement; the real layout is hand-edited in pcbnew.
#    Then route headless (freerouting must run FOREGROUND):
freerouting -de kicad/a7s_backplane_v2.dsn -do kicad/a7s_backplane_v2.ses -mp 15
#    ...and import the .ses back with pcbnew.ImportSpecctraSES.
#    NOTE: ImportSpecctraSES silently drops Edge.Cuts segments — re-verify the outline is closed.

# 4. fab package
kicad-cli pcb export gerbers -o kicad/fab_v2/ kicad/a7s_backplane_routed.kicad_pcb
kicad-cli pcb export drill   -o kicad/fab_v2/ kicad/a7s_backplane_routed.kicad_pcb
```

> Do **not** re-run `build_pcb.py` against a placed/routed board — it emits a rough placed-but-unrouted
> board and discards the hand-placement + routing.

## Additional Notes

I think the radio headers belong in the left top corner so that any radio chips you plug in will be standing up vertically behind the deck & 90 degrees from the flipper headers becuase radio likes angles.

Yes its a lot of IO, I wanted to max out what was available in the friendliest way possible supporting cheap available modules that already exist in the market.

## Credits

Flipper GPIO footprints from **[kbembedded/flipper-gpio-eda](https://github.com/kbembedded/flipper-gpio-eda)**
(BSD-2-Clause) — see [`a7s.pretty/ATTRIBUTION.md`](./a7s.pretty/ATTRIBUTION.md). All other footprints are
original to this project.
