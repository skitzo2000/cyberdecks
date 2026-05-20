# Workshop 02 — BB Q20 Clamshell Base

A ~75-minute workshop for assembling a clamshell **base** shell containing a BlackBerry Q20 keyboard, passive I²C carrier PCB, optional 18650 pack from Workshop 01, and an external power switch. The base mates with the lid (built in Workshop 03) via a print-in-place hinge.

> ⭐ **Skip this workshop if you want a separate BT keyboard.** Order a Rii i8+ (~$18), pair it during Workshop 03. The deck's back becomes a slab cover instead of a hinge.

## What you leave with

A complete clamshell BASE — BBQ20 wired through a passive I²C carrier, power switch installed, 18650 pack (if you brought one) seated in the cell holder. The base has the lower hinge half ready to mate with the lid in Workshop 03.

## Status: PCB design pending

**The passive I²C carrier PCB is the gating deliverable for this workshop.** Schematic + Gerbers belong in a separate hardware repo (TBD). Workshop cannot run until the PCB has been ordered and verified in qty. The PCB is *passive* — just an FFC connector for the BBQ20, level shifters if required, and a JST-SH 4-pin for I²C to the Pi.

## Bill of Materials (per kit)

| Part | Source | Qty | Cost |
|---|---|---|---|
| BlackBerry Q20 keyboard module (bulk salvage) | AliExpress | 1 | $12 |
| Passive I²C carrier PCB (FFC + level shifter + JST-SH) | JLCPCB qty 10+ | 1 | $3 |
| SPDT slide power switch, panel mount | Digi-Key — bulk | 1 | $1 |
| JST-SH 4-pin pigtail (carrier to Pi, routes through hinge in W03) | Adafruit — bulk | 1 | $1 |
| Pre-printed PETG clamshell base shell (w/ print-in-place lower hinge) | Organizer | 1 | $3 filament |
| M2.5 brass heat-set inserts (8) + screws (8) | Ruthex — bulk | 1 set | $1 |
| Solder, flux, jumper wire, heat-shrink | Amortized | — | ~$1 |
| **Total** | | | **~$22** |

If you completed Workshop 01, bring your 18650 pack — it mounts inside this same base shell.

## The carrier PCB — functional spec

Passive only. The Pi handles keyboard decoding via [`i2c_puppet`](https://github.com/solderparty/i2c_puppet). Trades QMK-on-keyboard for cost savings and keeps the Pi's USB-OTG free for radio dongles (Workshop 04).

**Required connectors / interfaces:**

- **BBQ20 FFC connector** — 24-pin, 0.5 mm pitch (verify against the actual module variant before tape-out)
- **JST-SH 4-pin output** — 3.3 V, GND, SDA, SCL → routes to Pi I²C0 + interrupt GPIO via the hinge
- **No on-board MCU** — passive level shifter only. RP2040+USB-HID variant is a v2 stretch goal.

**Form factor:** ~60 × 45 mm, matches BBQ20 footprint. M2.5 mounting holes on a 50 × 35 mm grid matching base shell standoffs.

**Open design questions** (resolve before tape-out):
- 3.3 V regulation from upstream 5 V, or pass through directly? BBQ20 is 3.3 V only.
- Backlight pin breakout? BBQ20 has white LEDs — route to a JST contact for an optional PWM line from the Pi.

## Clamshell base mechanical

- Base shell: same outer footprint as the lid (Workshop 03), ~12 mm deep
- Standoffs for BBQ20 + carrier on top; 18650 holder underneath (optional); power switch + USB-C charge breakout on side panels
- Hinge: **lower half** of the print-in-place PETG hinge built into the rear edge. (Upper half is on the lid; you pin them together in Workshop 03.)
- Cigar box alternative: documented in the take-home guide for builders who want wood — the keyboard module fits in any box ≥ 100 × 70 × 20 mm with some dremel work.

## Wiring

```
[BBQ20 24-pin FFC] ─► [Carrier PCB FFC connector]
                              │
                       [Level shifters]
                              │
                       [JST-SH 4-pin to Pi I²C, via hinge in W03]

[18650 pack JST-PH from Workshop 01 — optional]
       │
       ▼
[Power switch on right outer face]
       │
       ▼
[JST-PH to Pi 5V — routes through hinge in W03]
```

If you skipped Workshop 01, the power switch and cell holder are omitted. The hinge carries only the I²C JST-SH up to the lid, where PiSugar 3 feeds the Pi directly.

## Run-of-show (75 min)

| Time | Block |
|---|---|
| 0:00–0:10 | Intro: clamshell architecture, base vs lid, how it mates in Workshop 03 |
| 0:10–0:25 | Seat BBQ20 FFC into the carrier connector; latch closed. Continuity-test against carrier test pads. |
| 0:25–0:40 | Press heat-set inserts; mount carrier on base shell standoffs; install power switch and (if 18650) cell holder + USB-C charge breakout. |
| 0:40–0:55 | Wire the I²C JST-SH pigtail to the carrier; wire the 18650 power chain (switch in line) if applicable. |
| 0:55–1:10 | Smoke test: instructor connects your carrier's I²C to a test Pi running `i2c_puppet`. Type on the BBQ20; verify characters reach the Pi tty. |
| 1:10–1:15 | Pack, label, photo. See you in Workshop 03. |

## Common failure modes

- **Some keys dead, others fine.** FFC not fully seated — latch must close flat after insertion. Or damaged FFC cable.
- **No characters reach Pi.** I²C pull-ups missing or wrong I²C address — verify carrier rev's pinout matches `i2c_puppet` default (0x1F).
- **Print-in-place hinge half binds.** Pin clearance too tight or low layer adhesion. Re-print at 0.3 mm pin clearance, 80% infill on hinge region, anneal 70 °C × 30 min.
- **Hinge half wallows.** Pin too thin. Increase to 3.5 mm diameter and re-print.

## References

- [`solderparty/i2c_puppet`](https://github.com/solderparty/i2c_puppet) — driver basis
- [`../03-input.md`](../03-input.md) — BBQ20 buyer's guide and keyboard context
- [Penkesu](http://penkesu.computer/) — clamshell geometry reference

## Where to go next

- [Workshop 03: Main Deck Build](./03-main-build.md) — bring this base plus your battery; we attach the lid.
