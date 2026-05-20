# Cyberdeck Workshop Series

A series of hands-on workshops for building a modular cyberdeck. Attend only the workshops covering the components in your chosen build.

**Radio is a core design principle of this deck, not an add-on.** Every deck built in Workshop 03 ships with a daughter-PCB carrying CC1101 / LoRa / SDR sockets and a CC1101 module pre-included. Workshop 04 is about *applying* that capability.

## Choose your build, choose your workshops

The battery and keyboard precursor workshops are **single-path**. If you want the easy off-the-shelf option, skip the workshop entirely:

| If you want... | Skip the workshop, just buy this |
|---|---|
| ⭐ **PiSugar 3** for power (1200 mAh, USB-C charging, snap-on) | Skip Workshop 01. Order [PiSugar 3 for Pi Zero](https://www.pisugar.com/) (~$35); snap onto the back of your Pi during Workshop 03. |
| ⭐ **External BT keyboard + trackpad** | Skip Workshop 02. Order a Rii i8+ (~$18); pair during Workshop 03. |

Attend the workshop only if you want the custom build:

| # | Workshop | Duration | Attend if... |
|---|---|---|---|
| 01 | [18650 Battery Pack](./01-battery-18650.md) | ~60 min | You want 2× swappable 18650 cells, ~3–5× the runtime of PiSugar 3 |
| 02 | [BB Q20 Clamshell Base](./02-bbq20-base.md) | ~75 min | You want an integrated BlackBerry Q20 keyboard in a clamshell form |
| 03 | [Main Deck Build](./03-main-build.md) | ~75 min | **Mandatory** — this is the deck. Bring whatever battery and keyboard you've chosen. |
| 04 | [Radio Applications Capstone](./04-radio-applications.md) | ~90 min | You want to use the radio that's built into your deck — LoRa mesh, SDR, GPS, sub-GHz |

Sequencing: complete 01 and/or 02 before attending 03. 04 is the last session, after the deck is built. Total commitment ranges from one workshop (~75 min, slab basic) to four (~5 hours, maxed).

## Cost ladder

The maxed mono build is held under **$125 in parts**. Color screen is a called-out premium tier above the cap.

| Configuration | Workshops attended | Per-deck total |
|---|---|---|
| Slab basic (PiSugar 3 + BT keyboard) | 03 | ~$123 |
| Light clamshell (PiSugar 3 + BBQ20) | 02 + 03 | ~$127 *(slightly over cap — PiSugar 3 is the expensive piece)* |
| Mid clamshell (18650 + BBQ20) | 01 + 02 + 03 | ~$114 |
| **Maxed mono** (above + radio capstone gear) | 01 + 02 + 03 + 04 | **~$123** |
| **Maxed + color screen** *(premium)* | as above + DSI panel + Pi 4/5 swap | **~$153** |

The 18650 pack ($22) is genuinely cheaper than PiSugar 3 ($35) — going maxed actually saves money over going "light." The color premium is real: 5" Waveshare DSI ($35–48) + a Pi 4/5 swap ($35–50) adds ~$30 over the mono baseline. Pitched as an explicitly-tiered upgrade rather than bundled in maxed.

## Shared design choices

These hold across every workshop in the series:

- **Shell:** 3D-printed PETG, ~120 × 85 × 22 mm slab body / clamshell lid. Heat-set M2.5 inserts. Standoffs for both Pi Zero W2 (58 × 23 mm) and full Pi 4/5 (58 × 49 mm) — upgrade path doesn't require a new case.
- **Screen mount:** e-paper sits as a 40-pin HAT directly on the GPIO header. HAT also fastens to shell standoffs.
- **Power:** PiSugar 3 (snap-on, easy) or 18650 pack (Workshop 01). Either way the Pi sees a clean 5 V supply.
- **Hinge (clamshell only):** print-in-place PETG hinge by default. Cigar box donor chassis is documented as a non-kit alternative.
- **Radio infra:** every Workshop-03-built deck ships with a daughter-PCB (CC1101 socket, spare-radio header, USB-A passthrough) and a CC1101 module. Shell has antenna cutouts. No version of this deck is shipped radio-less.
- **BBQ20 carrier (clamshell):** passive I²C carrier PCB (no MCU). Pi runs [`i2c_puppet`](https://github.com/solderparty/i2c_puppet) in software. Trades QMK-on-keyboard for $5/kit savings and keeps the Pi's USB-OTG free for radio dongles in Workshop 04.

## See also

- [`../INDEX.md`](../INDEX.md) — top-level component buyer's guides
- [`../04-power.md`](../04-power.md) — cell selection, BMS, charge controller deep-dive
- [`../03-input.md`](../03-input.md) — keyboard / pointing-device options
- [`../06-chassis-and-prebuilt.md`](../06-chassis-and-prebuilt.md) — filament, heat-set inserts, print settings
