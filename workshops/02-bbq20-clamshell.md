# Workshop 02 — BB Q20 Keyboard + Clamshell

A ~2-hour workshop that upgrades your basic build into an integrated clamshell with a BlackBerry Q20 physical QWERTY keyboard on a custom QMK carrier PCB. Replaces the external BT keyboard with a thumb-typing experience native to the device. Prereq: [Workshop 00](./00-basic-build.md) completed. Strongly recommended: [Workshop 01](./01-battery-18650.md) first, since the 18650 pack lives in the clamshell base.

This upgrade adds **~$25 net** in parts (using the AliExpress BBQ20 module + custom carrier path) and brings the maxed deck (00 + 01 + 02 + 03) in at **~$121** — under the $125 cap.

## Clamshell architecture

The existing basic build becomes the **LID** (screen + Pi only — no battery in the lid). A new **BASE** is built below the hinge containing the BBQ20 keyboard, its carrier PCB, the 18650 pack (or PiSugar2 carried over), and an external power switch.

```
       LID (= basic build minus battery)
       ┌─────────────────────────────┐
       │  4.2" / 5.83" e-paper       │
       │  Pi Zero 2 W (or full Pi)   │
       │  Lid shell                  │
       └──────────────┬──────────────┘
                  [hinge]
       ┌──────────────┴──────────────┐
       │  BB Q20 keyboard (clicky)   │
       │  Custom QMK carrier PCB     │
       │  18650 pack (or PiSugar2)   │
       │  External slide switch ▶    │
       │  Base shell                 │
       └─────────────────────────────┘
```

## Status: PCB design pending

**The custom QMK carrier PCB is the gating deliverable for this workshop.** Specs, BOM, and Gerbers belong in a separate hardware repo (TBD). This workshop doc captures the *functional* spec so the PCB design can be driven from it. Workshop cannot run until the PCB has been ordered and verified in qty.

## Bill of Materials (per kit)

| Part | Source | Qty | Cost |
|---|---|---|---|
| BlackBerry Q20 keyboard module (salvaged, bulk-buy) | AliExpress | 1 | $12 |
| **Alt drop-in:** Solder Party BBQ20KBD (includes carrier + trackpad) | [Tindie](https://www.tindie.com/products/arturo182/bb-q20-keyboard-with-trackpad-usbi2cpmod/) | 1 | $44–55 |
| Custom QMK carrier PCB w/ JLCPCB-assembled RP2040 + USB-C | JLCPCB qty 10+ | 1 | $8 |
| **Hinge: print-in-place PETG** (built into shell STL — no purchased hinge) | Organizer print | — | $0 |
| Lid + base PETG shells (with print-in-place hinge) | Organizer | 1 set | $5 filament |
| SPDT slide power switch, panel mount | Digi-Key — bulk | 1 | $1 |
| M2.5 brass heat-set inserts (12) + M2.5×6 screws (12) | Ruthex — bulk | 1 set | $1.50 |
| JST-SH 4-pin pigtail (carrier to Pi I²C/USB in lid, through hinge channel) | Adafruit — bulk | 1 | $1 |
| **Per-kit total (custom PCB path)** | | | **~$28.50** |
| **Per-kit total (Solder Party drop-in path)** | | | **~$60** |

The Solder Party drop-in path blows the $125 cap on a maxed build. It's listed for reference but the workshop runs on the custom-carrier path.

### Hinge: alternative chassis (non-kit)

The workshop default is a **print-in-place PETG hinge** integrated into the shell STL — no hardware to source, prints with the shell in a single run, robust enough in PETG for 5,000+ open/close cycles when the pin is sized at 3 mm and printed in PETG-CF or annealed PETG.

For builders who want a totally different aesthetic, a **cigar box donor chassis** works beautifully — it already has a hinge, the wood looks great with exposed PCBs, and the boxes are free-to-$5 from most cigar shops. We don't carry this in the kit because the boxes vary in size and require per-box dremel work, but a take-home guide ships with the workshop covering how to fit the same internals into a box of your choosing.

## The carrier PCB — functional spec

The PCB lives in the base under the BBQ20, replaces both the i2c_puppet board and the trackpad daughter on a Solder Party-style design. Designed in-house so workshop bulk pricing stays under $10/board.

**Required connectors / interfaces:**

- **BBQ20 keyboard FFC connector** matching the BB Q20 module's flex cable (24-pin, 0.5 mm pitch — confirm against the keyboard module on hand before laying out)
- **USB-C** — host link to the Pi (USB-HID by default), also used for flashing QMK firmware to the on-board RP2040
- **JST-SH 4-pin alternate host link** — I²C + interrupt, for builders who configure the Pi for [i2c_puppet](https://github.com/solderparty/i2c_puppet) instead of USB-HID
- **No on-board trackpad in v1.** Cirque GlidePoint pad expansion via SPI/I²C breakout is a v2 stretch. v1 builders use the cursor keys / arrow cluster on the BBQ20.

**Firmware:**

- QMK on the RP2040, presents as USB HID Keyboard by default. Pre-flashed by the organizer.
- VIA-compatible keymap so participants can remap without re-compiling.
- Configurable Fn-layer for the BBQ20's `sym` and `mic` keys (which have no obvious modern equivalent).

**Form factor:**

- ~60 × 45 mm, matches the BBQ20 footprint so the assembly stacks neatly
- M2.5 mounting holes on a 50 × 35 mm grid matching base shell standoffs

**Open design questions** (to resolve before tape-out):
- 5V or 3V3 logic level for keyboard? BBQ20 module is 3V3-only — carrier must regulate. RP2040 native 3V3, USB-C provides 5V VBUS, on-board LDO required.
- Pull-ups for the keyboard FFC matrix? Yes, on RP2040 GPIOs internally.
- Backlight? BBQ20 has white LED backlight via separate pins. Carrier should route them to a single PWM GPIO with a current-limit resistor sized for the workshop's chosen brightness.

**TODO:** schematic, BOM cross-ref against LCSC stock, Gerbers, fab order with 1-week buffer.

## Clamshell mechanical

- **LID shell** = Workshop 00 shell with a hinge boss added to the bottom-rear corner. Battery cavity removed (no PiSugar2 in the lid — the basic build's PiSugar2 moves down to the base, OR the build pulls power from the 18650 pack via Workshop 01).
- **BASE shell** = new design, same outer footprint as the lid so the clamshell closes flush. ~12 mm deep. Standoffs for: BBQ20 + carrier PCB on top, 18650 holder underneath, power switch + USB-C breakout on side panels.
- **Hinge** = print-in-place PETG, integrated into the shell STL. 3 mm pin, 4 mm barrel, two parallel hinges spaced for stability. Annealed or PETG-CF survives heavy use. (Alternative chassis: cigar box donor — see the section above.)
- **Internal cable run** = JST-SH or USB-C ribbon through the hinge tube. Route with strain relief and pre-shape the bend so it doesn't fatigue at the pivot.

## Wiring

```
[BBQ20 FFC] ─► [Carrier PCB FFC connector]
                       │
                  [RP2040 QMK]
                       │
              ┌────────┴────────┐
              ▼                 ▼
        [USB-C to Pi]    [JST-SH 4-pin]
                              (I²C alt)
              │
              ▼
   [up through hinge to Pi USB port in lid]

[18650 pack (Workshop 01)] ─► [base shell power switch] ─► [boost] ─► [Pi 5V in lid]
                                                                       (through hinge)
```

## Software

**Default (USB-HID):** nothing on the Pi side. DietPi sees a standard USB keyboard, BlueZ stays disabled (no more BT pairing needed). External BT keyboard from Workshop 00 still pairs and works if desired.

**Optional (I²C via i2c_puppet):** install the i2c_puppet driver from [solderparty/i2c_puppet](https://github.com/solderparty/i2c_puppet), enable I²C on the Pi, route the interrupt GPIO. Saves the Pi's USB port for a radio dongle later (relevant if you're also doing Workshop 03).

## Pre-workshop prep (organizer)

Three weeks out:
- [ ] Order custom carrier PCBs from JLCPCB in qty (1.5× headcount; rejects happen)
- [ ] Pre-populate RP2040 / USB-C via JLCPCB assembly service, or hand-solder if qty is small
- [ ] Flash QMK firmware on every carrier; test against one BBQ20 module before declaring the batch good

Two weeks out:
- [ ] Print lid and base shells in PETG (~3 hr each, budget 4–5 print days for both halves per kit)
- [ ] Source BBQ20 modules — verify the flex pinout matches the carrier connector (some AliExpress batches differ)

One week out:
- [ ] Press heat-set inserts into all shell halves
- [ ] Pre-assemble the hinge to one half of each shell so workshop builders only have to align the other half

Day before:
- [ ] Pack kits. Each: lid shell, base shell (with hinge attached), BBQ20 module, carrier PCB (firmware-flashed), screws/inserts, JST-SH pigtail, USB-C pigtail for the hinge run.

## Workshop run-of-show (2 hr 00 min)

| Time | Block |
|---|---|
| 0:00–0:15 | Intro: the clamshell architecture, why integrate the keyboard, what's on the custom PCB. Hand around the bare carrier so people can see the RP2040 / FFC connector. |
| 0:15–0:30 | Disassemble basic build. Pi + screen come out for transplant into the lid shell. PiSugar2 either retired (if pairing this with Workshop 01) or relocated to base. |
| 0:30–0:50 | Assemble base: BBQ20 onto carrier PCB FFC, carrier onto base shell standoffs, install power switch and USB-C breakout. |
| 0:50–1:10 | Run cable through hinge from carrier USB-C up to a USB-C pigtail that mates to the Pi's micro-USB OTG (with a low-profile adapter). Strain-relieve at the hinge. |
| 1:10–1:30 | Install Pi + e-paper into lid, screw lid to upper hinge half. Close clamshell — verify it closes flush and doesn't pinch cables. |
| 1:30–1:50 | First boot. Pi boots, USB-HID keyboard appears in `lsusb`, typing on BBQ20 echoes in tty. Pair with the VIA web app to remap. |
| 1:50–2:00 | VIA remap demo (move `sym` to be a Hyper key, etc.). Photo, sticker, pitch Workshop 03. |

## Common failure modes and fixes

- **Keyboard not detected as USB HID.** RP2040 firmware not flashed, or USB-C cable through the hinge is bad. Reflash via the carrier's BOOT pad; test cable with a known-good device first.
- **Some keys dead, others fine.** BBQ20 FFC not fully seated in the carrier connector — the connector latch must be flipped down after insertion. Or one of the cable's traces is broken (rare; replace the module).
- **Backlight always on or never on.** PWM GPIO config in QMK firmware, or wrong polarity in the carrier's backlight driver. Check firmware vs. carrier rev.
- **Clamshell won't close flush.** Cable through the hinge is too thick or routed badly. Switch to a thinner cable, or relieve the hinge channel with a file.
- **Print-in-place hinge binds or snaps.** Pin clearance too tight, or printed at low layer adhesion. Re-print with 0.3 mm pin clearance and 80% infill on the hinge region; anneal in a 70 °C oven for 30 min to fuse layers.
- **i2c_puppet path: kernel module not loading.** `dtoverlay=i2c-rtc` conflicts. Disable the conflicting overlay; check `dmesg | grep i2c_puppet`.

## References

- [Solder Party BBQ20KBD on Tindie](https://www.tindie.com/products/arturo182/bb-q20-keyboard-with-trackpad-usbi2cpmod/) — reference design for the keyboard interface
- [`solderparty/i2c_puppet`](https://github.com/solderparty/i2c_puppet) — firmware and driver, basis for the I²C path
- [QMK on RP2040](https://docs.qmk.fm/#/feature_rp2040) — firmware target
- [Penkesu](http://penkesu.computer/) — GBA SP hinge geometry reference
- [`../03-input.md`](../03-input.md) — BBQ20 and keyboard buyer's guide context

## Where to go next

- **Skipped Workshop 01?** Consider doing it now — the clamshell base has room for the 18650 pack.
- **Want radio gear in the lid?** → [Workshop 03: Radio Expansion Capstone](./03-radio-capstone.md)
