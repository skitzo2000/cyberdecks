# Workshop 04 — Radio Applications Capstone

The capstone. The radio infrastructure is already on your deck — daughter-PCB, CC1101 socket, spare radio header, USB-A passthrough, and a CC1101 module — all installed in Workshop 03. This session is about *using* it.

Prereq: [Workshop 03](./03-main-build.md) completed. Any battery + keyboard combination works.

## What you leave with

A deck that has done — live, in the room — at least three of these:

- Sub-GHz packet sniff on 433 MHz (with the CC1101 already plugged in)
- LoRa hello-world transmission to another deck on the spare radio header
- Meshtastic node join via a LILYGO T-Beam plugged into USB-A
- Live GPS fix via a USB-A GPS dongle
- *(Stretch, RF-law-permitting)* garage door capture-and-replay with `rpitx` — your own door only

## Bill of Materials (per kit, additive to Workshop 03)

| Part | Source | Qty | Cost |
|---|---|---|---|
| Ai-Thinker Ra-02 LoRa module (for the spare radio header) | AliExpress | 1 | $4 |
| **Optional:** RP-SMA bulkhead + pigtail for external antenna | AliExpress | 1 | $4 |
| **Optional:** Spring/whip antenna for 433 / 915 MHz | AliExpress | 1 | $1.50 |
| **Demo only** (instructor brings, not per-kit): LILYGO T-Beam with Meshtastic preloaded | LILYGO | 1 | ~$35 |
| **Demo only:** GlobalSat BU-353-S4 USB GPS | various | 1 | ~$30 |
| **Per-kit total (Ra-02 + antenna)** | | | **~$5.50–9.50** |

## SPI bus map reminder (from Workshop 03)

| Pi GPIO | Function | Wired to |
|---|---|---|
| GPIO 10 (MOSI) | SPI0 MOSI | e-paper, CC1101, spare |
| GPIO 9 (MISO) | SPI0 MISO | e-paper, CC1101, spare |
| GPIO 11 (SCLK) | SPI0 SCLK | e-paper, CC1101, spare |
| GPIO 8 (CE0) | e-paper CS | e-paper only |
| GPIO 7 (CE1) | CC1101 CS | CC1101 socket |
| GPIO 16 | spare radio CS | spare header |
| GPIO 25 | CC1101 GDO0 (IRQ) | CC1101 |
| GPIO 24 | CC1101 GDO2 (IRQ) | CC1101 |
| GPIO 22 | spare radio RESET | spare header |
| GPIO 23 | spare radio DIO0 | spare header |
| GPIO 27 | spare radio DIO1 | spare header |

## Spare radio header pinout

```
Pin   Label       Pi GPIO
 1    3V3         3V3
 2    GND         GND
 3    CS          GPIO 16
 4    RESET       GPIO 22
 5    DIO0/IRQ    GPIO 23
 6    DIO1/BUSY   GPIO 27
```

SPI MOSI/MISO/SCLK are shared from the CC1101 socket — bring 3 short jumper wires across.

Compatible modules for the spare header:

| Module | Chip | Band | Pin count |
|---|---|---|---|
| Ai-Thinker Ra-02 | SX1278 | 433 MHz | 16-pin |
| Ai-Thinker Ra-01H | SX1278 | 868 MHz | 16-pin |
| HopeRF RFM95W | SX1276 | 868 / 915 MHz | 8-pin SMD on breakout |
| Heltec SX1262 module | SX1262 | 868 / 915 MHz | 8-pin breakout (uses BUSY pin) |
| nRF24L01+ | nRF24L01+ | 2.4 GHz ISM | 8-pin |

## USB-A bus options

The daughter-PCB's USB-A port wires to the Pi's USB-OTG (Pi Zero 2 W) or one of the USB-A ports (Pi 4/5). Demo-ready candidates:

- **LILYGO T-Beam** — ESP32 + LoRa + GPS, runs Meshtastic. Excellent demo target.
- **Heltec WiFi LoRa V3** — same idea, smaller, no GPS
- **RTL-SDR Blog V4** — note: **EOL in 2026** (see [`../05-networking-radio.md`](../05-networking-radio.md))
- **BU-353-S4 USB GPS** — instant GPS, `gpsd` plug-and-play
- **Flipper Zero** — serial mode, the Pi reads `/dev/ttyACM0`

If you did Workshop 02 with the default passive-I²C BBQ20 carrier, the USB-OTG is free for any of these. If you used the future RP2040 USB-HID carrier variant, USB-OTG is busy — switch to the I²C path before this workshop.

## Software stack (already on your SD card from Workshop 03)

- [`rpi-rf`](https://pypi.org/project/rpi-rf/), [`rpitx`](https://github.com/F5OEO/rpitx)
- [`pySX127x`](https://github.com/mayeranalytics/pySX127x), [`pyLoRa`](https://github.com/rpsreal/pySX127x)
- [Meshtastic CLI](https://meshtastic.org/docs/software/python/cli/)
- Helper scripts: `~/cc1101-scan.py`, `~/lora-hello.py`, `~/meshtastic-quickstart.sh`

## Run-of-show (90 min)

| Time | Block |
|---|---|
| 0:00–0:10 | Intro: the radio landscape, what's already on your deck, what we'll do today |
| 0:10–0:30 | Re-run `~/cc1101-scan.py` from Workshop 03 as refresher. Discuss what you're seeing on the e-paper output. |
| 0:30–0:55 | Wire Ra-02 into the spare header with jumpers (~5 min if you've kept the bundle from Workshop 03). Run `~/lora-hello.py` — packet ping between paired decks across the room. |
| 0:55–1:15 | Plug a LILYGO T-Beam into USB-A. `meshtastic --info` shows the node. Join a 3-node mesh — write a message that travels through the relay. |
| 1:15–1:30 | Optional stretch demo (RF-law-permitting): garage door capture with CC1101, replay with `rpitx` — **instructor demo only**, on the instructor's own door, never a stranger's. |
| 1:30 | Photo, take-home stretch list, end of series. |

## Common failure modes

- **CC1101 detected but receives nothing.** Antenna not attached. A 17 cm wire on the ANT pad acts as a quarter-wave for 433 MHz testing.
- **LoRa TX times out.** Frequency mismatch between sender and receiver. Verify the Python frequency parameter on both ends.
- **`rpitx` reboots the Pi.** Undersized power supply. Switch to wall power (or 18650, if you built that) for the replay demo.
- **Meshtastic CLI: "No device found."** USB-A shared with a BBQ20-over-USB carrier variant. Switch the carrier to the default I²C path.

## Take-home stretch list

- Garage door replay on your *own* door using `rpitx` and a recorded sample
- LoRa mesh with 2× LILYGO T-Deck Plus and your deck as a third node
- APRS tracker with a BU-353-S4 USB GPS + `gpsd`
- External antenna with RP-SMA pigtail + Nagoya NA-771 for serious range
- Swap CC1101 → SX1262 in the spare header for long-range LoRaWAN

## References

- [`../05-networking-radio.md`](../05-networking-radio.md) — full radio buyer's guide, RTL-SDR EOL note, regulatory context
- [`SmartRC-CC1101-Driver-Lib`](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) · [`pySX127x`](https://github.com/mayeranalytics/pySX127x)
- [`rpitx`](https://github.com/F5OEO/rpitx) · [`rpi-rf`](https://pypi.org/project/rpi-rf/)
- [Meshtastic Python CLI](https://meshtastic.org/docs/software/python/cli/)

## End of series

You've built a fully-functional radio-capable cyberdeck across (at most) four workshop sessions. What you do with it from here — that's your problem.
