# Cyberdeck Component Research — 2026

A six-part buyer's guide to the major component categories that make up a modern cyberdeck. Each guide is a self-contained shopping reference with current 2026 street prices, specs tables, "how to choose" sections, and inline source links.

## Contents

1. **[Compute](./01-compute.md)** — ARM SBCs (Pi 5/CM5, RK3588 family), RISC-V SBCs, x86 mini-mainboards (LattePanda, ODROID-H4, Framework), mini PCs as deck cores, handheld x86 donors (Steam Deck OLED, GPD), compute modules (CM5, Jetson Orin), and cyberdeck-native products (uConsole, DevTerm, MNT Reform).
2. **[Displays](./02-displays.md)** — 5"–10" primary LCDs, widescreen 320×1480/1920×480 bars, eInk panels (DASUNG, Boox, PineNote), OLED, secondary/status displays (HyperPixel, VFD, Nixie), donor LCD harvesting with driver boards, and HDMI/DSI/MIPI bridges.
3. **[Input](./03-input.md)** — Compact mechanical keyboards (40%/60%/65%), ortho kits (Planck/Preonic), splits (Corne/Glove80), handheld (BBQ20KBD, Cardputer), pointing devices (Ploopy, TrackPoint salvage, Cirque), switches/MCUs, niche (Topre, CharaChorder), touchscreen alternatives.
4. **[Power](./04-power.md)** — Pi UPS HATs (PiSugar, Waveshare, Geekworm), 18650/21700 cell selection (30Q, P42A, M50LT), BMS boards (DALY/JBD smart), DC-DC regulators, USB-C PD trigger ICs, solar input, repurposed power banks, fuel gauges, connectors, **FAA/ICAO 2026 battery rules**, runtime math.
5. **[Networking & Radio](./05-networking-radio.md)** — WiFi monitor-mode adapters (Alfa/Panda), internal M.2 cards (AX210 caveats, MT7922), SDR (RTL-SDR V4 EOL, HackRF, KrakenSDR), GPS/GNSS, LoRa/Meshtastic (T-Deck, Heltec), cellular modems, ham radio + Digirig, BT/RFID/NFC, antennas and pigtails.
6. **[Chassis & Pre-built Decks](./06-chassis-and-prebuilt.md)** — Community 3D-printable designs (Penkesu, Decktility, Cyberboy, Pip-Boy), Pelican/Apache/Nanuk donor cases, surplus mil enclosures, kit chassis (HackberryPi, Pi Slate), complete pre-builts (uConsole, DevTerm, MNT Pocket Reform, Mecha Comet, Beepy), CNC fab services, filament selection, mounting hardware.

## Workshop Series

A separate workshop track teaches builders how to assemble a working cyberdeck from these components. See [`workshops/`](./workshops/) — basic build, battery upgrade, clamshell+BBQ20 upgrade, and radio expansion capstone, each as a standalone session.

## How to Use This Set

Build-vs-buy is the first fork:

- **Buy:** ClockworkPi uConsole CM4 Lite ($249) is the highest-ROI complete deck in 2026. MNT Pocket Reform (€1,399) for open-hardware enthusiasts. Mecha Comet ($189–269) for modular handheld. Beepy ($79 kit) for pager-class hacking. See §5 of [chassis](./06-chassis-and-prebuilt.md).
- **Build:** decide form factor first (slab/clamshell/handheld/wearable/briefcase) and chassis material — that locks down most other choices. Pi 5 + Pelican 1200 + Waveshare 11.9" + RK61 + Geekworm X1202 is the canonical $300 starter build.

Power-budget your build before buying displays or x86 silicon — see the runtime math in [power](./04-power.md). A Pi 5 deck lands ~12 W active; a Framework mainboard lands ~30–55 W. The battery you can legally fly with (≤100 Wh per FAA/ICAO 2026) caps how aggressive your CPU can be.

Plan antenna pass-throughs on day one if your chassis is metal — see the "chassis material and RF" section in [networking](./05-networking-radio.md). This is the #1 retroactive regret in finished decks.

## Notable 2026 Status Changes

- **RTL-SDR Blog V4 is EOL** — final batch shipping; "V4L Lite" successor under development.
- **ClockworkPi DevTerm A06/A04/R-01** are all out of stock; uConsole CM4 Lite is the only ClockworkPi currently shipping.
- **Sixfab's flagship Pi 5 5G kit (RM502Q-AE)** is EOL; replaced by new 5G Dev Kit (~$650).
- **MNT Reform Next** ships June 5, 2026 — relevant for purchase timing.
- **Shapeways** reborn as Manuevo BV; marketplace did not return. PCBWay and SendCutSend are the practical CNC defaults.
- **JLCPCB CNC pricing jumped in 2025** to PCBWay parity — old "JLCPCB is cheapest" advice is stale.
- **ICAO effective March 27, 2026:** max 2 power banks per passenger, no in-flight USB charging from seat, batteries must stay accessible (not overhead).
- **HackberryPi**: Tindie store on break; Elecrow is the active retail channel.
- **Intel AX210**: 6 GHz monitor-mode blocked by Intel regulatory firmware lockout — MediaTek MT7922 is the 2026 recommendation for WiFi 6E auditing.
