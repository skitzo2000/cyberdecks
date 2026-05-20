# Workshop Cyberdeck Build — Pi Zero 2 W + BlackBerry KB + e-Paper + Radio Expansion

A low-cost, light-soldering workshop build that produces a pocketable Linux cyberdeck with a real sub-GHz / LoRa radio socket. Designed for a 2–3 hour session where participants leave with a working device.

## Design Goals

- **~$100–130 per kit** in parts, assuming organizer pre-prints shells and pre-flashes SD cards.
- **Light soldering only** — header pins on the Pi and a few JST pigtails. No SMD work.
- **First-class radio expansion** — every deck ships with a labelled, well-documented socket for cheap SPI radio modules (CC1101, RFM95W, Ai-Thinker Ra-01/Ra-02, SX126x boards).
- **e-Paper primary display** — readable in sunlight, near-zero idle draw, fits the cyberdeck aesthetic.
- **All parts provided.** Workshop runs as kit-assembly, not parts-procurement.

## Build Architecture

```
+------------------------------+
| 4.2" e-Paper (SPI0 CE0)      |
+------------------------------+
| Pi Zero 2 W (+ stacking hdr) |
|   USB-A breakout for radios  |
|   BBQ20 over USB or I²C      |
|   LiPo SHIM + 1S 2000 mAh    |
+------------------------------+
|   BBQ20 keyboard module      |
|   (Solder Party or clone)    |
+------------------------------+
| Side: 8-pin CC1101 socket    |
|       + 6-pin "spare radio"  |
|       + USB-A port           |
+------------------------------+
```

## Bill of Materials (per kit, ~2026 prices)

| Part | Source | Qty | Cost |
|---|---|---|---|
| Raspberry Pi Zero 2 W (with pre-soldered header preferred) | Adafruit / PiShop / Pimoroni | 1 | $20 |
| microSD 32 GB Class 10 (pre-flashed by organizer) | Bulk | 1 | $7 |
| Solder Party BBQ20KBD (USB+I²C+PMOD) | [Tindie](https://www.tindie.com/products/arturo182/bb-q20-keyboard-with-trackpad-usbi2cpmod/) | 1 | $50 |
| **Alt:** AliExpress BB Q10/Q20 clone keyboard module | AliExpress | 1 | $20–25 |
| Waveshare 4.2" e-Paper Module + driver HAT | [Waveshare 4.2" V2](https://www.waveshare.com/4.2inch-e-paper-module.htm) | 1 | $30 |
| **Alt smaller/cheaper:** Waveshare 2.9" e-Paper HAT (296×128) | Waveshare | 1 | $20 |
| Pimoroni LiPo SHIM for Pi Zero (or Adafruit PowerBoost 1000C) | [Pimoroni](https://shop.pimoroni.com/products/lipo-shim) | 1 | $13 |
| 1S 2000 mAh LiPo pouch, JST-PH | PKCell / Adafruit #2011 | 1 | $10 |
| **Radio socket:** 1×8 female header 2.54 mm, low-profile | Digi-Key 952-2261-ND | 1 | $0.40 |
| 1×6 female header (spare radio) | Digi-Key | 1 | $0.30 |
| 2×20 stacking GPIO header | Adafruit #2223 | 1 | $3 |
| Pre-printed PETG shell + cover | Organizer (Bambu/Prusa) | 1 set | $3 filament |
| M2.5 brass heat-set inserts (8) + M2.5×6 screws (8) | Ruthex | 1 set | $1.50 |
| JST-PH 2.0 pigtail pair, 100 mm | Adafruit #1131 | 1 | $1 |
| **CC1101 module (included as the "first radio")** | AliExpress E07-M1101D-TH or red-PCB 8-pin | 1 | $4 |
| Solder, flux pen, jumper wire spool, heat-shrink | Amortized | — | ~$3 |
| **Per-kit total** | | | **~$115–125** with Solder Party KB, **~$90** with clone |

Optional add-ons (per-kit cost if included):
- USB-A breakout (panel mount) — $2
- RP-SMA bulkhead + pigtail for external antenna — $4
- Spring/whip antenna for CC1101 (433 MHz or 915 MHz) — $1.50

## Radio Expansion — The Important Bit

The deck ships with one CC1101 socket pre-wired and a second "spare radio" header that participants can use for LoRa or future modules. SPI bus is shared; chip-select pins differentiate.

### SPI bus map (Pi Zero 2 W)

| Pi GPIO | Function | Wired to |
|---|---|---|
| GPIO 10 (MOSI) | SPI0 MOSI | e-Paper, CC1101, spare |
| GPIO 9 (MISO) | SPI0 MISO | e-Paper, CC1101, spare |
| GPIO 11 (SCLK) | SPI0 SCLK | e-Paper, CC1101, spare |
| GPIO 8 (CE0) | e-Paper CS | e-Paper only |
| GPIO 7 (CE1) | CC1101 CS | CC1101 socket |
| GPIO 16 | spare radio CS | spare header |
| GPIO 25 | CC1101 GDO0 (IRQ) | CC1101 |
| GPIO 24 | CC1101 GDO2 (IRQ) | CC1101 |
| GPIO 22 | spare radio RESET | spare header |
| GPIO 23 | spare radio DIO0 | spare header |
| GPIO 27 | spare radio DIO1 | spare header |
| GPIO 17 | e-Paper DC | e-Paper |
| GPIO 5  | e-Paper RST | e-Paper |
| GPIO 6  | e-Paper BUSY | e-Paper |

### Socket 1 — CC1101 (1×8, dedicated, pre-wired)

Most cheap CC1101 modules (E07-M1101D-TH, red square PCB) use this pinout. Standardize on **one specific module** for the workshop and silk-screen the matching order:

```
Pin   Module pad   Pi GPIO        Notes
 1    GND          GND
 2    MOSI         GPIO 10
 3    GDO2         GPIO 24        IRQ
 4    SCK          GPIO 11
 5    MISO         GPIO 9
 6    GDO0         GPIO 25        IRQ
 7    CSN          GPIO 7  (CE1)
 8    VCC          3V3            NEVER 5V — CC1101 is 3.3 V only
```

**⚠️ Verify the pinout on the exact module you bulk-buy** — there are at least three "8-pin CC1101" variants with different pad orders. Buy 5 spares from the same listing, label one as the workshop reference, and silkscreen the socket to match.

### Socket 2 — "Spare Radio" (1×6, jumper-wire to anything)

A second 6-pin labelled header for participants to wire LoRa modules with dupont jumpers:

```
Pin   Label       Pi GPIO
 1    3V3         3V3
 2    GND         GND
 3    CS          GPIO 16
 4    RESET       GPIO 22
 5    DIO0/IRQ    GPIO 23
 6    DIO1/BUSY   GPIO 27
```

SPI MOSI/MISO/SCLK are shared from the CC1101 socket — bring 3 short jumper wires across. Compatible with:

| Module | Chip | Band | Pin count | Wiring notes |
|---|---|---|---|---|
| Ai-Thinker Ra-02 | SX1278 | 433 MHz | 16-pin | Wire VCC/GND/MOSI/MISO/SCLK/NSS/RESET/DIO0; ignore DIO1–5 |
| Ai-Thinker Ra-01H | SX1278 | 868 MHz | 16-pin | Same |
| HopeRF RFM95W | SX1276 | 868/915 MHz | 8-pin SMD on breakout | Same wiring as Ra-02; smaller footprint |
| Heltec SX1262 module | SX1262 | 868/915 MHz | 8-pin breakout | Uses BUSY pin (DIO1 on our header) |
| nRF24L01+ (2.4 GHz) | nRF24L01+ | 2.4 GHz ISM | 8-pin | Different chemistry but same SPI pattern; works with the spare header |

### Socket 3 — USB-A host port

Panel-mounted USB-A port wired to the Pi Zero's USB OTG. Lets participants plug in:
- RTL-SDR Blog V4 dongle ($40, while stocks last)
- LILYGO T-Beam / Heltec WiFi LoRa V3 (full ESP32+LoRa boards via USB)
- Flipper Zero in serial mode
- Any USB WiFi adapter

A Pi Zero 2 W only has one USB-OTG line, so this **shares** with the BBQ20 keyboard if the keyboard is wired over USB instead of I²C. Decide during prep: if BBQ20 over USB → use a tiny USB hub IC (FE1.1S, ~$2) on the workshop PCB, or wire BBQ20 over I²C and keep USB-A for radios.

### Routing options for the workshop

**Option A — Hand-wired (cheapest, slower).** Pi GPIO header → 2×20 stacking → dupont/breadboard wires to two through-hole female headers epoxied into the shell. Cheap, no PCB, but every joint is failure-prone. ~30 min of wiring per kit.

**Option B — Workshop daughter-PCB (recommended).** Design a single 60×40 mm "radio + power" PCB at JLCPCB/PCBWay (~$5/board in qty 10). Carries:
  - 2×20 GPIO socket that mates with the Pi
  - 1×8 CC1101 socket
  - 1×6 spare radio header
  - LiPo SHIM footprint (Pimoroni reference layout)
  - JST-PH for battery
  - USB-A breakout pads
  - 4-pin JST-SH for BBQ20 I²C
  - Mount holes M2.5 matching the shell

Participants snap in their Pi, solder the stacking header (~10 joints, ~10 min), drop in radio, screw to shell. Build time drops to ~45 min.

**Option C — Off-the-shelf HAT.** Pimoroni Breakout Garden + a [PCB Pi Hut "Sub-1 GHz CC1101" HAT](https://thepihut.com/) or use the Sparkfun LoRaWAN Pi HAT. Easiest if you can find one in stock at workshop scale; weakest cyberdeck aesthetic.

**Recommended for first workshop run:** Option A for prototyping with 2–3 builders, then move to Option B for any session of >5 builders.

## Mechanical / Chassis

3D-printed two-piece PETG shell, ~150 × 90 × 22 mm. Heat-set inserts pressed in by the organizer the night before. STL design considerations:

- Cutouts: USB-C (Pi power), micro-HDMI (optional debug), microSD slot, USB-A radio port, antenna passthrough (RP-SMA hole), 8-pin CC1101 window so the chip is visible/replaceable through the back cover.
- Recess for the BBQ20KBD flush with the front face.
- e-Paper sits behind a 0.5 mm clear PETG window or open cutout (open is better for screen quality).
- 4× M2.5 standoffs molded into the shell for the Pi/daughterboard sandwich.
- Antenna grommet at top-back so the CC1101 whip clears.

If you have no printer farm: use an **Apache 2800 Harbor Freight case** ($30) with foam cutouts. Less cyberdeck-aesthetic, far less prep.

## Software Stack (pre-flashed on every SD card)

Image: **DietPi** (32-bit) on a Pi Zero 2 W. DietPi is faster to first boot than Pi OS Lite on the Zero 2 and has lower RAM overhead.

Pre-installed and configured:
- `fbcp-ili9341` framebuffer driver pointed at the e-paper (or `IT8951` driver for partial-refresh panels)
- BBQ20KBD HID driver — Solder Party's official [I2C driver](https://github.com/solderparty/i2c_puppet) or the kernel HID-USB driver if you wired it as USB
- `python3-rpi.gpio`, `spidev`, `python3-pip`
- `rpi-rf` and `rpitx` for sub-GHz experimentation
- [pySX127x](https://github.com/mayeranalytics/pySX127x) and [pyLoRa](https://github.com/rpsreal/pySX127x) for LoRa modules on the spare socket
- [SmartRC-CC1101-Driver-Lib](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) — Arduino-style but works with `wiringpi`
- [Meshtastic CLI](https://meshtastic.org/docs/software/python/cli/) (no daemon — for talking to a USB-attached Heltec via the USB-A port)
- tmux, vim, w3m, btop, neofetch, htop
- Custom MOTD: ASCII cyberpunk banner + WiFi join instructions
- Pre-built hotspot SSID "DECK-XX" so participants can SSH in from a phone during the workshop

Optional: bundle [twtxt](https://twtxt.dev/) or [aerc](https://aerc-mail.org/) for a "this thing is a real computer" demo at the end.

## Pre-Workshop Prep Checklist (organizer)

Two weeks out:
- [ ] Source 1.2× the head-count for every part (failure rate is real)
- [ ] Verify the bulk CC1101 modules with one test wiring before sending out the order
- [ ] Order workshop PCBs (Option B) at JLCPCB with a 1-week buffer
- [ ] Print all shells (~2 hours each on a Bambu A1 mini in PETG; budget 2–3 print farm days)

One week out:
- [ ] Flash all SD cards. Boot each one once to expand FS and verify it gets to a prompt.
- [ ] Press heat-set inserts into every shell while watching TV.
- [ ] Solder the 2×20 stacking header to every Pi Zero 2 W. (~5 min each.)

Day before:
- [ ] Pack kits in labelled bags. Each bag: Pi (in static bag), SD, BBQ20, e-paper, LiPo SHIM, battery, daughterboard, shell, screws/inserts in a tiny ziplock, radio module, JST pigtail, jumper-wire bundle.
- [ ] Print pinout cards (color, 4×6") — one per builder.
- [ ] Print the "what to type" cheat-sheet for first boot.

## Workshop Run-of-Show (2 hr 30 min)

| Time | Block |
|---|---|
| 0:00–0:15 | Intro: what is a cyberdeck, what you're about to build, why e-paper, why CC1101. Show finished example. |
| 0:15–0:30 | Soldering primer at the bench: tin tip, flow heat, joint inspection. Each builder solders a practice joint. |
| 0:30–1:00 | Solder Pi to daughterboard (stacking header). Inspect with magnifier. Continuity-test one CS and one ground. |
| 1:00–1:30 | Mechanical: heat-set inserts already in shell. Mount Pi sandwich. Route LiPo. Press BBQ20 into front face. Drop in e-paper. Screw down. |
| 1:30–1:50 | First boot. Flash light pattern (boot ok). Pi auto-connects to workshop SSID; instructor shows DHCP table on projector. SSH from phone optional. |
| 1:50–2:10 | Plug in the CC1101. Run `python3 ~/cc1101-scan.py` — pre-installed script that scans 433 MHz and shows any RF packets nearby. Most likely catches your car-key remote. |
| 2:10–2:25 | Show how to plug an Ra-02 into the spare header with jumper wires. Send a "hello, world" LoRa packet between two decks. |
| 2:25–2:30 | Customize MOTD, take a photo, hand out stickers, talk about take-home next steps. |

## Common Failure Modes and Fixes

- **e-paper shows nothing.** Almost always a missing GND or wrong driver overlay. Re-check pinout card, verify `dtoverlay=` line in `/boot/config.txt`.
- **CC1101 returns 0xFF on every register read.** Reversed VCC/GND or 5V on VCC — chip is dead. Replace, do not retry.
- **BBQ20 not detected.** Driver not loaded — `lsmod | grep hid_i2c_puppet`. Reseat the JST cable; some clones have the polarity flipped, hence the cheaper price.
- **LiPo SHIM brown-out under load.** Old battery or cold solder on the SHIM. Swap battery first.
- **Wi-Fi never connects.** SSID typo in `/boot/dietpi-wifi.txt`. Pre-flash *with the workshop SSID baked in*.

## Stretch Goals (post-workshop take-home material)

- **CC1101 replay attack on your own garage door** with `rpitx` and a CC1101 + recorded sample.
- **LoRa mesh** — buy two LILYGO T-Deck Plus and join the workshop deck to a Meshtastic mesh via the USB-A port.
- **GPS** — plug a [GlobalSat BU-353-S4](https://www.globalsat.com.tw/en/product-167321/USB-GPS-Receiver-with-SiRF-Star-IV-chipset-BU-353S4.html) into USB-A, run `gpsd`, deck becomes a portable APRS tracker.
- **External antenna** — replace the spring whip with an RP-SMA pigtail and a Nagoya NA-771 for serious range.
- **Swap to SX126x LoRa** — pop the CC1101, jumper an SX1262 board into the spare header, jump to long-range LoRaWAN.

## Sources

### Core Components
- [Solder Party BBQ20KBD (Tindie)](https://www.tindie.com/products/arturo182/bb-q20-keyboard-with-trackpad-usbi2cpmod/) · [i2c_puppet firmware/driver (GitHub)](https://github.com/solderparty/i2c_puppet)
- [Waveshare 4.2" e-Paper Module V2](https://www.waveshare.com/4.2inch-e-paper-module.htm) · [Waveshare 2.9" e-Paper HAT](https://www.waveshare.com/2.9inch-e-paper-module.htm)
- [Pimoroni LiPo SHIM for Pi Zero](https://shop.pimoroni.com/products/lipo-shim) · [Adafruit PowerBoost 1000C](https://www.adafruit.com/product/2465)
- [DietPi for Raspberry Pi](https://dietpi.com/)

### Radio Modules and Libraries
- [Ai-Thinker Ra-02 SX1278 module](https://docs.ai-thinker.com/en/lora) · [HopeRF RFM95W datasheet](https://www.hoperf.com/modules/lora/RFM95.html)
- [SmartRC-CC1101-Driver-Lib (GitHub)](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) · [pySX127x (GitHub)](https://github.com/mayeranalytics/pySX127x)
- [rpitx — Raspberry Pi RF transmitter (GitHub)](https://github.com/F5OEO/rpitx) · [rpi-rf (PyPI)](https://pypi.org/project/rpi-rf/)
- [Meshtastic Python CLI](https://meshtastic.org/docs/software/python/cli/)

### Fab and Hardware
- [JLCPCB PCB ordering](https://jlcpcb.com/) · [PCBWay PCB ordering](https://www.pcbway.com/)
- [Ruthex heat-set inserts](https://www.ruthex.de/) · [Adafruit JST cable assortment (#1131)](https://www.adafruit.com/product/1131)
