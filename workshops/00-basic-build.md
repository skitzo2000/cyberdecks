# Workshop 00 — Basic Cyberdeck Build

A ~2.5-hour workshop that produces a working DietPi cyberdeck. Pi Zero W2 + 4.2" e-paper HAT + PiSugar 3 + a paired Bluetooth keyboard with trackpad. Light soldering only. The shell footprint is identical for the optional 5.83" e-paper upgrade and accommodates either a Pi Zero W2 or a full-size Pi 4/5 — every later upgrade plugs into the same body.

## Design goals

- **~$108/kit** assuming organizer pre-prints shells, pre-flashes SD cards, and sources parts in bulk
- **Maxed-out path stays under $125** across the full workshop series (mono). Color screen is a called-out premium tier on top.
- **Light soldering only** — one set of GPIO header pins, that's it
- **All parts provided.** Workshop runs as kit-assembly, not parts-procurement
- **One enclosure design that survives every upgrade path**
- **Headless first-boot via WiFi hotspot** so participants SSH from their phones

## Build architecture

```
+---------------------------------+
| 4.2" or 5.83" e-paper HAT       |
| (SPI on GPIO 8/9/10/11)         |
+---------------------------------+
| Pi Zero 2 W (+ stacking header) |
|   micro-USB / micro-HDMI ports  |
+---------------------------------+
| PiSugar 2 (Plus) — spring pads  |
+---------------------------------+
| PETG shell, dual-Pi standoffs   |
+---------------------------------+

   [ External BT keyboard + trackpad combo, paired ]
```

## Bill of Materials (per kit, ~2026 prices)

| Part | Source | Qty | Cost |
|---|---|---|---|
| Raspberry Pi Zero 2 W (pre-soldered header preferred) | Adafruit / PiShop / Pimoroni — bulk | 1 | $18 |
| microSD 16 GB Class 10 (pre-flashed by organizer; DietPi fits in 2 GB) | Bulk | 1 | $4 |
| Waveshare 4.2" e-Paper HAT V2 (400×300, SPI) | [Waveshare](https://www.waveshare.com/4.2inch-e-paper-module.htm) | 1 | $30 |
| **Alt size upgrade:** Waveshare 5.83" e-Paper HAT (648×480, SPI) | Waveshare | 1 | +$15 |
| PiSugar 3 for Pi Zero (USB-C, I²C battery status) | [PiSugar](https://www.pisugar.com/) | 1 | $35 |
| Rii i8+ Mini Wireless Keyboard + Touchpad (BT version) | Amazon / AliExpress | 1 | $18 |
| 2×20 stacking GPIO header (extra-tall, 14 mm) | Adafruit #2223 — bulk | 1 | $2 |
| Pre-printed PETG shell + cover (dual-Pi standoffs) | Organizer (Bambu/Prusa) | 1 set | $3 filament |
| M2.5 brass heat-set inserts (8) + M2.5×6 screws (8) | Ruthex — bulk | 1 set | $1 |
| Solder, flux pen, jumper wire, heat-shrink | Amortized | — | ~$2 |
| **Per-kit total** | | | **~$113** |

Note on the BT keyboard: Rii i8+ is the cheap-and-cheerful workshop default. Logitech K400 Plus ($30) is the upgrade if you want a full-size companion. Both pair with a stock BlueZ stack — no custom driver work.

Note on PiSugar: PiSugar 3 (USB-C) supersedes PiSugar 2 in 2026; same form factor, same price point, much better connector. PiSugar 3 Plus (+$5) buys ~30% more capacity if budget allows.

## Mechanical / shell

3D-printed two-piece PETG shell, ~120 × 85 × 22 mm. Heat-set inserts pressed by organizer the night before.

Design must-haves:

- **Dual-Pi standoff bosses molded in.** Pi Zero W2 mounts on the 58 × 23 mm pattern; Pi 4/5 mounts on the 58 × 49 mm pattern. The shared edge means two standoffs are common; the other two of each set are size-specific. Costs nothing at print time; unused bosses don't interfere.
- **Screen sits flush with the front face.** Cutout sized to the chosen e-paper module (4.2" or 5.83" — print two shell variants if you offer both screen sizes in the same workshop; everything else is identical).
- **HAT fastens to shell standoffs**, not only to the GPIO pins. Two M2.5 holes through the HAT into shell bosses keep the screen from levering on the header pins.
- **PiSugar 3 contact pad** — no cutout needed, it lives between the Pi and the shell back, secured by the same standoffs.
- **Cutouts:** Pi micro-USB (charging), microSD slot, micro-HDMI (debug only — not used during normal operation).
- **No keyboard cutout in the basic shell.** The keyboard is external.

## Software stack (pre-flashed on every SD card)

Image: **DietPi** (32-bit) on a Pi Zero 2 W. Lower RAM overhead and faster first-boot than Pi OS Lite on the Zero 2.

Pre-installed and configured:

- e-paper SPI driver: upstream [`waveshare/e-Paper`](https://github.com/waveshare/e-Paper) Python lib for the chosen panel
- `bluez`, `bluez-tools` with the Rii i8+ pre-paired (MAC baked into `/etc/bluetooth/main.conf`) and auto-reconnect on boot
- WiFi hotspot "DECK-XX" auto-up on boot (hostapd + dnsmasq) — instructor shows DHCP table on projector for SSH access
- `python3-rpi.gpio`, `spidev`, `python3-pip`
- tmux, vim, w3m, btop, neofetch, htop
- Custom MOTD: ASCII cyberpunk banner + "what's on this thing" cheat sheet
- Optional, off by default: pwnagotchi face renderer on e-paper

## Wiring

There is essentially no wiring. The build is:

1. Solder the 2×20 stacking header onto the Pi Zero 2 W (~10 minutes per builder, ~10 joints)
2. Snap the PiSugar 3 onto the back of the Pi — spring contacts touch the back of the GPIO pads, no solder
3. Plug the e-paper HAT onto the top of the stacking header
4. Drop the assembly into the shell, screw 4× M2.5 into the Pi-Zero standoff pattern
5. Screw the HAT down to the shell standoffs (4× M2.5)
6. Close the back cover

No flying wires. No daughterboards. No JST pigtails. This is the appeal of the basic build.

## Pre-workshop prep checklist (organizer)

Two weeks out:
- [ ] Source 1.2× headcount for every part (failure rate is real)
- [ ] Print all shells (~1.5 hr each in PETG on a Bambu A1 mini; budget 2–3 print farm days)
- [ ] Bulk-pair Rii i8+ keyboards to a test Pi to capture MAC addresses for the pre-flash

One week out:
- [ ] Flash all SD cards. Boot each one once to expand FS and verify it reaches a prompt.
- [ ] Press heat-set inserts into every shell while watching TV.
- [ ] Solder the 2×20 stacking header onto every Pi Zero 2 W (~5 min each).

Day before:
- [ ] Pack kits in labelled bags. Each bag: Pi (in static bag), SD, PiSugar 3, e-paper HAT, BT keyboard, stacking header (if not pre-soldered), shell, screws/inserts ziplock.
- [ ] Print pinout / cheat-sheet cards (color, 4×6") — one per builder.
- [ ] Print the "first boot" instruction sheet.

## Workshop run-of-show (2 hr 30 min)

| Time | Block |
|---|---|
| 0:00–0:15 | Intro: what is a cyberdeck, why e-paper, the upgrade ladder ahead (Workshops 01/02/03). Show finished example. |
| 0:15–0:30 | Soldering primer at the bench: tin tip, flow heat, joint inspection. Each builder solders a practice joint. |
| 0:30–0:50 | Solder 2×20 stacking header onto Pi. Inspect with magnifier. |
| 0:50–1:20 | Mechanical: insert Pi onto standoffs, snap PiSugar 3 to the back, attach e-paper HAT, screw HAT to shell, close cover. |
| 1:20–1:50 | First boot. Deck powers up, PiSugar 3 LED indicates charge. WiFi hotspot DECK-XX appears. SSH from phone. Run `~/eink-hello.py` — "hello, world" renders on the panel. |
| 1:50–2:15 | Bluetooth keyboard pairing demo. Verify the keyboard reconnects after a power cycle. |
| 2:15–2:30 | Customize MOTD, take a photo, hand out stickers, talk about the next workshop in the series. |

## Common failure modes and fixes

- **e-paper shows nothing.** Almost always a missing GND or wrong SPI overlay. Re-check the pinout card; verify `dtoverlay=spi0-0cs` in `/boot/config.txt` and that the cable seats flat.
- **PiSugar 3 won't power on.** Sliding power switch on the PiSugar side is OFF. Or the battery shipped flat — needs 30+ minutes on a charger before first use.
- **PiSugar 3 LED flashes red rapidly.** Spring contacts not aligned with the back of the GPIO pads. Reseat with even pressure.
- **BT keyboard pairs once then disconnects after sleep.** Add `Class = 0x000540` and `FastConnectable = true` to `/etc/bluetooth/main.conf` and restart `bluetooth.service`. The pre-flashed image already has this — only an issue if a participant reflashed.
- **WiFi hotspot never appears.** SSID/password typo in `/etc/hostapd/hostapd.conf`. Pre-flash with verified config.
- **Pi 4/5 standoff doesn't line up.** You're using the Pi Zero boss pattern with a full Pi (or vice versa). The unused bosses are intentional — use the correct set for the Pi in front of you.

## Footnote: Pi + screen size combinations supported by this shell

| Pi | 4.2" e-paper | 5.83" e-paper | 5" color DSI |
|---|---|---|---|
| Pi Zero W2 | ✓ default | ✓ swap-in | ✗ (no DSI on Zero W2) |
| Pi 4 / Pi 5 | ✓ | ✓ | ✓ (requires Pi swap; uses DSI ribbon to the panel) |

The 5" color DSI option is sold as a **premium tier** (~$25–30 over the mono cap) because it requires both a screen swap and a Pi 4/5 swap. It's pitched at the end of the workshop, not built during the session.

## Where to go next

- **Want more battery life?** → [Workshop 01: 18650 Battery Pack](./01-battery-18650.md)
- **Want integrated thumb-typing without an external keyboard?** → [Workshop 02: BB Q20 + Clamshell](./02-bbq20-clamshell.md)
- **Want radio capabilities (sub-GHz, LoRa, SDR, GPS)?** → [Workshop 03: Radio Expansion Capstone](./03-radio-capstone.md)
