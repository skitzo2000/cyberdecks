# Workshop 03 — Main Deck Build

A ~75-minute workshop where the deck comes together. Bring whatever battery and keyboard you've already built or bought; we'll integrate them with the Pi, e-paper, radio infrastructure, and shell.

**Mandatory for every builder.** This is the deck.

## What you leave with

A working DietPi cyberdeck booting to the e-paper, hotspotting a WiFi SSID for SSH, and running its first CC1101 sub-GHz scan. Specific configuration depends on what you brought:

| You brought | You'll build |
|---|---|
| PiSugar 3 + BT keyboard | Slab deck, PiSugar snapped to Pi back, BT keyboard paired |
| PiSugar 3 + BBQ20 base | Clamshell, PiSugar in lid under Pi, base connects via hinge |
| 18650 pack + BBQ20 base | Maxed clamshell, 18650 in base, hinge carries power + I²C to lid |
| 18650 pack + BT keyboard | Slab deck with 18650 in a thicker back-shell (uncommon but supported) |

## Bill of Materials (per kit, Workshop 03 only)

| Part | Source | Qty | Cost |
|---|---|---|---|
| Raspberry Pi Zero 2 W (pre-headered preferred) | Adafruit / bulk | 1 | $18 |
| microSD 16 GB Class 10 (pre-flashed, DietPi fits in 2 GB) | Bulk | 1 | $4 |
| Waveshare 4.2" e-Paper HAT V2 (400×300, SPI) | [Waveshare](https://www.waveshare.com/4.2inch-e-paper-module.htm) | 1 | $30 |
| **Alt size upgrade:** Waveshare 5.83" e-Paper HAT (648×480, SPI) | Waveshare | 1 | +$15 |
| Workshop daughter-PCB (CC1101 socket + spare radio header + USB-A breakout) | JLCPCB qty 10+ | 1 | $5 |
| CC1101 sub-GHz module (the "first radio," included) | AliExpress E07-M1101D-TH | 1 | $4 |
| 1×8 + 1×6 socket header set | Digi-Key | 1 | $1 |
| 2×20 stacking GPIO header (extra-tall, 14 mm) | Adafruit #2223 — bulk | 1 | $2 |
| Pre-printed PETG slab back / clamshell lid (dual-Pi standoffs, antenna cutout, CC1101 window) | Organizer | 1 | $3 filament |
| M2.5 brass heat-set inserts (8) + screws (8) | Ruthex — bulk | 1 set | $1 |
| Solder, flux, jumper wire, heat-shrink | Amortized | — | ~$2 |
| **Subtotal** | | | **~$70** |

Plus what you brought:

- **PiSugar 3** (~$35) — for snap-on power
- **18650 pack** from Workshop 01 (~$22) — for swappable runtime
- **Rii i8+ BT keyboard** (~$18) — for slab keyboard
- **BBQ20 clamshell base** from Workshop 02 (~$22) — for integrated keyboard

## Mechanical / shell

The Workshop 03 shell is the lid (clamshell builds) or full slab back (BT keyboard builds). Always includes:

- **Dual-Pi standoffs molded in** — Pi Zero W2 (58 × 23 mm) AND Pi 4/5 (58 × 49 mm). Use the pattern matching your Pi; unused bosses don't interfere.
- **Screen flush with the front face**, cutout sized to chosen e-paper (4.2" or 5.83" — pre-print the right variant)
- **HAT fastens to shell standoffs**, not only to the GPIO pins (two M2.5 holes through the HAT into shell bosses)
- **Daughter-PCB standoffs** between Pi and shell for the radio carrier
- **Antenna passthrough** on the rear edge for an external whip or RP-SMA pigtail
- **CC1101 window** in the back cover so the chip is visible and swappable
- **Hinge upper half** (clamshell builds) — print-in-place PETG, mates with the BBQ20 base from Workshop 02

Slab and clamshell-lid variants share most of the CAD; the difference is the back face (closed slab vs hinge half).

## Software stack (pre-flashed on every SD card)

Image: **DietPi** (32-bit) on Pi Zero 2 W.

Pre-installed and configured:

- e-paper SPI driver — [`waveshare/e-Paper`](https://github.com/waveshare/e-Paper) Python lib for the chosen panel
- CC1101 driver — [`SmartRC-CC1101-Driver-Lib`](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) + `~/cc1101-scan.py` ready to run
- For BBQ20 builds: [`i2c_puppet`](https://github.com/solderparty/i2c_puppet) kernel module + interrupt GPIO wired
- For BT keyboard builds: `bluez` configured with auto-reconnect; instructor pairs Rii i8+ during the workshop
- WiFi hotspot "DECK-XX" auto-up at boot for SSH access from a phone or laptop
- `python3-rpi.gpio`, `spidev`, `python3-pip`, tmux, vim, btop, neofetch
- Custom MOTD with WiFi join instructions and the `cc1101-scan` invocation

## Wiring

Core build is largely no-wire:

1. Solder 2×20 stacking header onto Pi (~10 min)
2. Mount daughter-PCB onto Pi GPIO via the stacking header
3. Plug e-paper HAT onto the top of the stacking header
4. Plug CC1101 into the daughter-PCB's 1×8 socket
5. Drop assembly into shell, screw HAT to shell standoffs

Then integrate your specific configuration:

- **PiSugar 3:** snap onto back of Pi before mounting (spring contacts on GPIO pad backs)
- **18650 pack (slab variant):** route JST-PH from the pack (mounted in slab back cover) to the daughter-PCB's 5 V/GND pads
- **BBQ20 clamshell base:** mate the lid's hinge half with the base's hinge half (slide print-in-place pin through both barrels), route I²C JST-SH and power JST-PH through the hinge channel up to the daughter-PCB and Pi
- **BT keyboard:** instructor pairs Rii i8+ during the workshop; no internal wiring

## Run-of-show (75 min)

| Time | Block |
|---|---|
| 0:00–0:10 | Intro: what's on the daughter-PCB, why radio is core, what you'll see when CC1101 lights up |
| 0:10–0:25 | Solder 2×20 stacking header to Pi. Inspect joints. |
| 0:25–0:40 | Mount Pi on shell standoffs; stack daughter-PCB; plug in e-paper HAT; plug in CC1101 module. |
| 0:40–0:55 | Integrate your battery + keyboard. **Slab:** snap PiSugar 3 to back or mount 18650 pack in back-shell. **Clamshell:** join hinge halves, route cables through, screw shut. |
| 0:55–1:05 | First boot. WiFi hotspot DECK-XX appears. SSH from phone. E-paper shows "hello." |
| 1:05–1:15 | Run `~/cc1101-scan.py` — passively listens on 433 MHz. Most rooms catch a car key / doorbell / tire-pressure sensor within minutes. Photo, sticker, see you in Workshop 04. |

## Common failure modes

- **e-paper shows nothing.** Wrong SPI overlay or missing GND. Verify `dtoverlay=spi0-0cs` in `/boot/config.txt`.
- **CC1101 returns 0xFF on every register read.** Reversed VCC/GND or 5 V on VCC — the chip is dead, replace.
- **PiSugar 3 won't power on.** Sliding switch is OFF, or battery shipped flat — needs 30+ min on a charger first.
- **18650 pack: Pi reboots randomly under load.** MT3608 boost trimmer drifted from 5.10 V — re-check from Workshop 01.
- **BBQ20: characters echo wrong / nothing at all.** I²C address mismatch or `i2c_puppet` not loaded. `dmesg | grep i2c_puppet`.
- **Hinge won't close flush.** Cable too thick in the channel. Switch to thinner JST-SH variant or file the channel.
- **Pi 4/5 standoff doesn't line up.** You're using the Pi Zero boss pattern with a full Pi (or vice versa) — use the correct set.

## Footnote: color screen variant (premium tier)

A premium SKU swaps the e-paper HAT for a **Waveshare 5" DSI LCD (B)** (~$35–48), which requires upgrading to a **Pi 4 or Pi 5** (~$35–50, has the DSI port the Pi Zero W2 lacks). Pulls maxed cost to ~$153. Not a workshop variant — pitched as a take-home upgrade with the swap documented in the kit handout.

## Where to go next

- **Use the radio you just built in.** → [Workshop 04: Radio Applications Capstone](./04-radio-applications.md) — LoRa mesh, SDR via USB-A, GPS, sub-GHz replay.
