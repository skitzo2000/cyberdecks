# Workshop 03 — Radio Expansion Capstone

The "everyone shows up regardless of build" capstone. Adds a CC1101 sub-GHz socket, a spare radio header for LoRa / SX126x / nRF24, and a USB-A port for SDR / Meshtastic / GPS dongles. Closes out the series with practical demos: 433 MHz packet sniffing, LoRa hello-world between two decks, and a stretch garage-door replay.

Prereq: [Workshop 00](./00-basic-build.md) at minimum. Compatible with any combination of Workshops 01 (battery) and 02 (clamshell).

## What you're adding

```
+----------------------------+
| Side: 8-pin CC1101 socket  |
|       + 6-pin "spare radio"|
|       + USB-A port         |
+----------------------------+
        │
   [shared SPI0 bus, dedicated CS per device]
        │
   [Pi GPIO header in lid]
```

## Bill of Materials (per kit)

| Part | Source | Qty | Cost |
|---|---|---|---|
| Workshop daughter-PCB (radio + sockets, designed for this workshop) | JLCPCB qty 10+ | 1 | ~$5 |
| **Radio socket:** 1×8 female header 2.54 mm, low-profile | Digi-Key 952-2261-ND | 1 | $0.40 |
| 1×6 female header (spare radio) | Digi-Key | 1 | $0.30 |
| CC1101 module (included as the "first radio") | AliExpress E07-M1101D-TH or 8-pin red-PCB | 1 | $4 |
| USB-A panel-mount breakout | AliExpress / Adafruit | 1 | $2 |
| JST-PH pigtails | Adafruit #1131 | 1 | $1 |
| Solder, jumper wire, heat-shrink | Amortized | — | ~$2 |
| **Per-kit total** | | | **~$15** |

Optional add-ons (per-kit cost if included):
- RP-SMA bulkhead + pigtail for external antenna — $4
- Spring/whip antenna for CC1101 (433 MHz or 915 MHz) — $1.50
- Ai-Thinker Ra-02 LoRa module for the spare header — $4
- LILYGO T-Beam (USB-A demo target with Meshtastic preloaded) — $35 (one per workshop, not per kit)

## Why a daughter-PCB

You *can* hand-wire this with dupont jumpers (Option A below) and it'll work, but every joint is a future failure. The daughter-PCB carries:

- 2×20 GPIO socket mating with the Pi
- 1×8 CC1101 socket
- 1×6 spare radio header
- USB-A breakout pads
- 4-pin JST-SH for BBQ20 I²C (if the builder has Workshop 02 done)
- M2.5 mounting holes matching the lid shell

~$5/board in qty 10, designed once, reused across every cohort. The PCB design is in [TBD repo].

## SPI bus map (Pi Zero 2 W and Pi 4/5 — same pins)

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
| GPIO 17 | e-Paper DC | e-Paper (from Workshop 00) |
| GPIO 5  | e-Paper RST | e-Paper |
| GPIO 6  | e-Paper BUSY | e-Paper |

## Socket 1 — CC1101 (1×8, dedicated, pre-wired)

Standardize on **one specific CC1101 module** for the workshop and silk-screen the matching pin order on the daughter-PCB:

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

**⚠️ Verify the pinout on the exact module you bulk-buy.** There are at least three "8-pin CC1101" variants with different pad orders in circulation. Buy 5 spares from the same listing, label one as the workshop reference, and silkscreen the socket to match.

## Socket 2 — "Spare Radio" (1×6, jumper-wire to anything)

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

## Socket 3 — USB-A host port

Panel-mounted USB-A port wired to the Pi's USB OTG (Pi Zero 2 W) or one of the USB-A ports (Pi 4/5). Lets participants plug in:

- RTL-SDR Blog V4 dongle ($40, while stocks last — note: this is **EOL** in 2026, see `../05-networking-radio.md`)
- LILYGO T-Beam / Heltec WiFi LoRa V3 (full ESP32+LoRa boards via USB)
- Flipper Zero in serial mode
- USB GPS dongle (BU-353-S4 et al)
- USB WiFi adapter

**Pi Zero 2 W only has one USB-OTG line**, so this **shares** the bus if Workshop 02 (BBQ20 over USB) is installed. Two paths:

- BBQ20 over **I²C** (the i2c_puppet route): leaves USB-A free for radios. Recommended.
- BBQ20 over **USB**: needs a tiny USB hub IC (FE1.1S, ~$2) on the daughter-PCB to share with USB-A.

A full-size Pi 4/5 has multiple USB-A ports natively and sidesteps this entirely.

## Routing options

**Option A — Hand-wired (cheapest, slowest).** Pi GPIO header → 2×20 stacking → dupont/breadboard wires to two through-hole female headers epoxied into the shell. Cheap, no PCB, but every joint is failure-prone. ~30 min of wiring per kit. Use this if you skipped ordering the daughter-PCB.

**Option B — Workshop daughter-PCB (recommended).** Snap-in carrier with all sockets pre-wired. Solder the 2×20 stacking header to the carrier (~10 joints, ~10 min). Build time per builder: ~45 min.

**Option C — Off-the-shelf HAT.** Pimoroni Breakout Garden + a [Pi Hut "Sub-1 GHz CC1101" HAT](https://thepihut.com/) or the Sparkfun LoRaWAN Pi HAT. Easiest if you can find one in stock at workshop scale; weakest cyberdeck aesthetic.

**Recommended for the first workshop run:** Option A for prototyping with 2–3 builders, then move to Option B for any session of >5 builders.

## Software additions (on top of the Workshop 00 image)

DietPi already has Python, SPI, and GPIO from Workshop 00. The capstone image adds:

- [`rpi-rf`](https://pypi.org/project/rpi-rf/) and [`rpitx`](https://github.com/F5OEO/rpitx) for sub-GHz experimentation
- [`SmartRC-CC1101-Driver-Lib`](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) — Arduino-style but works under `wiringpi`
- [`pySX127x`](https://github.com/mayeranalytics/pySX127x) and [`pyLoRa`](https://github.com/rpsreal/pySX127x) for LoRa modules on the spare socket
- [Meshtastic CLI](https://meshtastic.org/docs/software/python/cli/) — talks to a USB-attached Heltec / T-Beam through the USB-A port
- Pre-installed helper scripts: `~/cc1101-scan.py`, `~/lora-hello.py`, `~/meshtastic-quickstart.sh`

## Pre-workshop prep (organizer)

Two weeks out:
- [ ] Order daughter-PCBs from JLCPCB (qty 1.5× headcount)
- [ ] Verify the bulk CC1101 modules with one test wiring before the order goes wider
- [ ] Charge & label one demo LILYGO T-Beam with workshop SSID + Meshtastic enabled

One week out:
- [ ] Re-flash SD cards from Workshop 00 builders' images, layering on the capstone software bundle (or distribute a "capstone overlay" script that builders run on arrival)
- [ ] Print pinout cards (color, 4×6") — one per builder

Day before:
- [ ] Pack kits. Each: daughter-PCB, CC1101 module, jumper-wire bundle, USB-A breakout, JST pigtail, fresh sticker sheet.

## Workshop run-of-show (2 hr 30 min)

| Time | Block |
|---|---|
| 0:00–0:15 | Intro: the radio landscape, why SPI sharing works, what each socket is for. Show a finished example deck scanning a doorbell. |
| 0:15–0:35 | Solder 2×20 stacking header to daughter-PCB; mount onto Pi in the lid. |
| 0:35–0:55 | Plug in CC1101. Run `python3 ~/cc1101-scan.py` — passively listens on 433 MHz. Most rooms catch a car-key remote, a doorbell, or a tire-pressure sensor within 5 minutes. |
| 0:55–1:25 | Wire Ra-02 into the spare header with jumpers. Send a "hello, world" LoRa packet between two decks (instructor demos with a paired deck). |
| 1:25–1:50 | Plug the LILYGO T-Beam into USB-A. `meshtastic --info` shows the node. Pair the deck into a 3-node mesh. |
| 1:50–2:15 | Stretch demo (optional, RF-law-permitting): record a button press from your own garage door with the CC1101, replay it with `rpitx`. |
| 2:15–2:30 | Photo, stickers, take-home stretch goals (below), feedback form. |

## Common failure modes and fixes

- **CC1101 returns 0xFF on every register read.** Reversed VCC/GND or 5V on VCC — the chip is dead. Replace, do not retry.
- **CC1101 detected but receives nothing.** Antenna not attached, or the module shipped without one. A 17 cm wire on the ANT pad acts as a basic 433 MHz quarter-wave for testing.
- **LoRa Tx fails with timeout.** Frequency mismatch between the two decks (433 vs 868 vs 915 MHz). Re-check the Python frequency parameter on both sides.
- **`rpitx` causes random Pi reboots.** It's pushing serious power through GPIO 4 — undersized power supply or weak boost. Fall back to PiSugar2 / wall power for the replay demo.
- **Meshtastic CLI says "No device found."** USB-A port is shared with BBQ20-over-USB (Workshop 02 USB path) and the hub isn't enumerating. Reseat the USB-C cable to the T-Beam, or move BBQ20 to the I²C path.

## Stretch goals (take-home material)

- **CC1101 replay attack on your own garage door** with `rpitx` and a recorded sample
- **LoRa mesh** — buy two LILYGO T-Deck Plus and join the deck to a Meshtastic mesh via USB-A
- **GPS** — plug a [GlobalSat BU-353-S4](https://www.globalsat.com.tw/en/product-167321/USB-GPS-Receiver-with-SiRF-Star-IV-chipset-BU-353S4.html) into USB-A, run `gpsd`, the deck becomes a portable APRS tracker
- **External antenna** — replace the spring whip with an RP-SMA pigtail and a Nagoya NA-771 for serious range
- **Swap to SX126x LoRa** — pop the CC1101, jumper an SX1262 board into the spare header, jump to long-range LoRaWAN

## References

- [`../05-networking-radio.md`](../05-networking-radio.md) — RTL-SDR EOL note, full radio buyer's guide, regulatory context
- [Ai-Thinker Ra-02 docs](https://docs.ai-thinker.com/en/lora) · [HopeRF RFM95W datasheet](https://www.hoperf.com/modules/lora/RFM95.html)
- [`SmartRC-CC1101-Driver-Lib`](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) · [`pySX127x`](https://github.com/mayeranalytics/pySX127x)
- [`rpitx`](https://github.com/F5OEO/rpitx) · [`rpi-rf`](https://pypi.org/project/rpi-rf/)
- [Meshtastic Python CLI](https://meshtastic.org/docs/software/python/cli/)

## End of series

This was the last scheduled workshop. After this, builders own a fully-loaded cyberdeck that can:

- Show a status screen on e-paper (Workshop 00)
- Run all day on swappable cells (Workshop 01)
- Thumb-type natively in a clamshell form (Workshop 02)
- Sniff and transmit sub-GHz / LoRa / GPS (Workshop 03)

What they do with it next — that's their problem.
