# Cyberdeck Workshop Series

A series of hands-on workshops for building a modular cyberdeck. Attend only the workshops covering the components in your chosen build — every workshop after the basic one is an additive upgrade that snaps onto the same shell.

## Which workshops should I attend?

| Your build | Attend |
|---|---|
| Basic: Pi Zero W2 + e-paper + PiSugar2 + BT keyboard/trackpad | 00 |
| + 18650 battery pack (replaces PiSugar2) | 00 → 01 |
| + Integrated BB Q20 in a clamshell (replaces external KB) | 00 → 02 |
| + Radio expansion (CC1101 / LoRa / SDR / GPS) | 00 → 03 |
| Maxed: all upgrades | 00 → 01 → 02 → 03 |

Recommended sequence: 00 first, then your upgrades in any order, then 03 last as the capstone.

## Workshops

| # | Workshop | Duration | Prereqs |
|---|---|---|---|
| [00](./00-basic-build.md) | Basic Cyberdeck Build | ~2.5 hr | none — start here |
| [01](./01-battery-18650.md) | 18650 Battery Pack Upgrade | ~1.5 hr | 00 |
| [02](./02-bbq20-clamshell.md) | BB Q20 Keyboard + Clamshell | ~2 hr | 00 |
| [03](./03-radio-capstone.md) | Radio Expansion Capstone | ~2.5 hr | 00 |

## What you get from Workshop 00

A working DietPi handheld with:

- Raspberry Pi Zero 2 W, headless on a 4.2" (or 5.83") e-paper HAT
- PiSugar2 battery, ~6 hr runtime under light load
- Bluetooth keyboard+trackpad combo pre-paired and persistent across reboots
- WiFi hotspot for SSH access from a phone
- Single 3D-printed shell that also accommodates a future Pi 4/5 swap (dual standoff pattern) and any of the upgrades above

## Cost ladder

The maxed mono build is held under **$125 in parts**. Color screen is a called-out premium tier above the cap.

| Configuration | Workshops attended | Per-deck total |
|---|---|---|
| Basic mono | 00 | ~$108 |
| Basic + 18650 pack | 00 → 01 | ~$120 |
| Basic + clamshell w/ BBQ20 | 00 → 02 | ~$118 |
| **Maxed mono** (all upgrades) | 00 → 01 → 02 → 03 | **~$121** |
| **Maxed + color screen** *(premium)* | as above + DSI color + Pi 4/5 swap | **~$150** |

The color premium is real: 5" Waveshare DSI ($35–48) + a Pi 4/5 swap ($35–50) overruns the mono baseline by ~$25–30. It's offered as an explicitly-pitched higher tier rather than bundled into "maxed."

## Shared design choices

These hold across every workshop in the series:

- **Shell:** 3D-printed PETG, ~120 × 85 × 22 mm for the basic body. Heat-set M2.5 inserts. Standoffs for both Pi Zero W2 (58 × 23 mm) and full Pi 4/5 (58 × 49 mm) — the upgrade path doesn't require a new case.
- **Screen mount:** e-paper sits as a 40-pin HAT directly on the GPIO header. The HAT also fastens to shell standoffs so it doesn't rely on the GPIO pins alone.
- **Power:** PiSugar 3 in basic (USB-C charging, I²C SoC); swap to a custom 18650 pack (Workshop 01) for the runtime upgrade. Either way, the Pi sees a clean 5 V supply.
- **Hinge (clamshell only):** print-in-place PETG hinge as the default — no metalwork, no parts to source, robust enough in PETG. A cigar box donor chassis is documented as a non-kit aesthetic alternative for builders who want wood.
- **Upgrade path is non-destructive.** Every upgrade is reversible — you can fall back to the basic config by reinstalling the original parts.

## Upgrade dependencies

- **Color screen (5" Waveshare DSI) requires a Pi 4 or Pi 5** — the Pi Zero W2 has no DSI port. This is the one upgrade that pulls a Pi upgrade along with it. Covered as a footnote in Workshop 00 rather than a dedicated session.
- **Clamshell + integrated BBQ20 (Workshop 02)** is most cleanly built with the 18650 pack (Workshop 01) since the pack lives in the clamshell base. Doing 01 before 02 saves rework.

## See also

- [`../INDEX.md`](../INDEX.md) — top-level component buyer's guides this series draws from
- [`../04-power.md`](../04-power.md) — cell selection, BMS, charge controller deep-dive for Workshop 01
- [`../03-input.md`](../03-input.md) — keyboard/pointing-device options behind Workshops 00 and 02
- [`../06-chassis-and-prebuilt.md`](../06-chassis-and-prebuilt.md) — filament, heat-set inserts, print settings
