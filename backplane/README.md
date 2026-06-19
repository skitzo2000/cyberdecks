# A7S Cyberdeck Backplane

A hand-solderable backplane "shield" for the **Radxa Cubie A7S** (Allwinner A733).
It turns the A7S's 45 header pins into a cyberdeck I/O board.

## What's on it

- **2× "8+1" radio sockets** on shared SPI1 — drop-in for **nRF24L01+ / CC1101 / CC2500**
  (the 8-pin nRF24 order + an AUX pin 9 for ESP-01/breadboard use). Two radios can run at once.
- **RP2040-Zero input MCU** — handles the human inputs only (4 on-board buttons + 2 off-board,
  joystick, rotary encoder). It is *not* a radio bridge; all radio lines map straight to A7S pins.
- **2.8" SPI TFT** (ILI9341) with resistive (XPT2046) touch.
- **Flipper-Zero-compatible header** (real two-connector 1×8 + 1×10 GPIO) for Flipper-ecosystem add-ons.
- Taps **5V and 3V3 from the A7S header** (external battery powers the A7S over its USB-C port);
  polyfused radio rails.

## Design choices

- **All through-hole / hand-solder** — no SMD, no pick-and-place. It's a backplane you solder to.
- **2-layer.** Schematic/netlist generated with **SKiDL**; board with the KiCad **pcbnew** Python API;
  autorouting with **freerouting** (headless). See `tools/` and `*_skidl.py`.
- A7S header geometry is on **STEP-measured datums** so the shield mates correctly (`refs/MECH-DATUMS.md`).

## Status

Schematic/netlist **complete and verified** (`SCHEMATIC.md`, 0 ERC errors).
The PCB is **placed and fully routed** (`kicad/a7s_backplane.kicad_pcb`) but the floorplan is a
**working starting point** — placement/routing still want a human optimization pass in the KiCad GUI
before fab. Verify the RP2040-Zero footprint row spacing and header pin-1 orientation before ordering.

## Files

- `BACKPLANE-DESIGN.md` — full design doc + BOM
- `SCHEMATIC.md` — authoritative netlist / connectivity
- `a7s_backplane_skidl.py` → `a7s_backplane.net` — netlist generator
- `kicad/` — pcbnew board, build script, render
- `a7s.pretty/` — custom footprints (TFT, RP2040-Zero, Flipper — see `ATTRIBUTION.md`)

## Credits

Flipper GPIO footprints from [kbembedded/flipper-gpio-eda](https://github.com/kbembedded/flipper-gpio-eda)
(BSD-2-Clause) — see `a7s.pretty/ATTRIBUTION.md`.
