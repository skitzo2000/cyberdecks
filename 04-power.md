# The 2026 Cyberdeck Power & Battery Buyer's Guide

A cyberdeck lives or dies by its power system. Get it wrong and you have a beautiful brick; get it right and you have a runtime-monster you can fly with, charge from a wall wart, or top off from the sun. This guide covers ten subsystem categories, current 2026 street pricing, and the math you need to spec a build.

---

## 1. Pi-Targeted UPS / Power HATs

Drop-in modules that sit on the GPIO header, provide UPS behavior, and (usually) charge a Li-ion pack while powering the SBC. Best for Raspberry Pi-class decks under ~15 W.

| Module | Price (USD) | Chemistry / Capacity | Output | Notes |
|---|---|---|---|---|
| PiSugar 3 (Zero) | ~$40 | 1S LiPo 1200 mAh built-in | 5 V / 2.5 A | RTC, hardware charge protection, soft-shutdown over I2C. Great for Pi Zero/Zero 2 W. |
| PiSugar 3 Plus | ~$50 | 1S LiPo 5000 mAh | 5 V / 3 A | RTC, anti-touch switch, watchdog. Fits Pi 3/4/5. Pogo-pin contact ([PiSugar](https://www.pisugar.com/products/pisugar-3-plus-raspberry-pi-ups)) |
| PiSugar S Plus | ~$55 | 1S LiPo 5000 mAh | 5 V / 2.5 A | Older S-series; cheaper but no Plus features. |
| Waveshare UPS HAT (original) | ~$22 | 2× 18650 (not incl.) | 5 V / 3 A | Basic I2C fuel-gauge; simultaneous charge+output. |
| Waveshare UPS HAT (B) | ~$28 | 2× 18650 (not incl.) | 5 V / 5 A | Pogo pins, high-current; good for Pi 4/5 + SSD. |
| Waveshare UPS HAT (C) | ~$15 | 1× 14500 | 5 V / 1 A | Zero-format. |
| Waveshare UPS HAT (D) | ~$25 | 1× 21700 (not incl.) | 5 V / 5 A | Single-cell 21700; compact. |
| Waveshare UPS HAT (E) | ~$32 | 4× 21700 (not incl.) | 5 V / 6 A | Bi-directional fast charging, biggest in class ([Waveshare](https://www.waveshare.com/ups-hat-e.htm)) |
| Geekworm X1200 | ~$25 | 2× 18650 (not incl.) | 5.1 V / 5 A | Pi 5 native, low-power shutdown, USB-C PD in ([Geekworm](https://geekworm.com/products/x1200)) |
| Geekworm X1202 | ~$35 | 4× 18650 (not incl.) | 5.1 V / 5 A | Doubles X1200 capacity; runtime-king for Pi 5 ([Geekworm](https://geekworm.com/products/x1202)) |
| Geekworm X728 | ~$45 | 2× 18650 | 5.1 V / 6 A | AC-loss detection, auto-on, buzzer; Pi 3/4. |
| Pimoroni LiPo SHIM (Pi) | ~$13 | 1S LiPo (not incl.) | 5 V / 1.5 A | No charger; just boost. For ultralight Zero builds. |
| Pimoroni LiPo SHIM for Pico | ~$12 | 1S LiPo | 5 V / boost | Power button + charge LED for Pico ([Pimoroni](https://shop.pimoroni.com/en-us/products/pico-lipo-shim)) |
| UPS PIco HV4.0B | ~$70 | Supercap + opt. LiPo | 5 V / 3 A | Industrial-grade, RTC, I2C status, opt. battery. |
| Argon ONE V5 UPS add-on | ~$55 | 2× 18650 (not incl.) | 5 V PD | Slides under Argon ONE V5; clean integration. |

**Pros:** turnkey, soft-shutdown, RTC, plug-and-play. **Cons:** Pi-only, output capped ~5–6 A at 5 V, no 12 V rail for accessories.

---

## 2. 18650 / 21700 Cell Packs and Holders

The workhorse format for serious cyberdecks. Choose cells by chemistry, capacity, and continuous discharge (CDR) — never trust unbranded listings.

| Cell | Format | Capacity | Max CDR | ~Wh | Price/cell |
|---|---|---|---|---|---|
| Samsung 30Q | 18650 | 3000 mAh | 15 A | ~10.8 | $5–7 |
| Samsung 35E | 18650 | 3500 mAh | 8 A | ~12.6 | $5–7 |
| Molicel P28A | 18650 | 2800 mAh | 25 A (35 A pulse) | ~10.1 | $6–8 ([ODG](https://www.origin-ic.com/blog/molicel-p28a-vs-samsung-30q-18650-battery-review/48406)) |
| LG M50LT | 21700 | 5000 mAh | 7.3 A | ~18 | $7–9 |
| Samsung 40T (40T5) | 21700 | 4000 mAh | 25 A | ~14.4 | $8–10 ([18650BatteryStore](https://www.18650batterystore.com/products/samsung-40t)) |
| Samsung 30T | 21700 | 3000 mAh | 35 A | ~10.8 | $8–10 |
| Molicel P30B | 21700 | 3000 mAh | 35 A | ~10.8 | $9–11 |
| Molicel P42A | 21700 | 4200 mAh | 30 A | ~15.1 | $10–12 |
| Keystone holder 1042 (single 18650) | — | — | 10 A | — | $1.20 |
| Keystone holder 1043 (single 21700) | — | — | 15 A | — | $1.80 |
| Pre-built 3S2P 18650 30Q pack | 3S2P | 6000 mAh @ 11.1 V | ~30 A | ~66 | $55–80 |
| Pre-built 4S2P 21700 P42A pack | 4S2P | 8400 mAh @ 14.4 V | ~60 A | ~120 | $120–150 |

**Pros:** highest energy density per dollar, replaceable, recyclable, huge selection. **Cons:** require BMS, mechanical packaging, fuses; pre-built packs can exceed FAA carry-on limits — check Wh.

---

## 3. LiPo Pouch Cells

Use when you need a flat form factor (slide under a slab keyboard, fill a thin lid). Lower CDR than 18650s; puncture is catastrophic.

| Cell | Capacity | Voltage | Dimensions | Price |
|---|---|---|---|---|
| PKCell LP503562 | 1200 mAh | 3.7 V | 5×35×62 mm | $5–7 |
| PKCell LP103450 | 2000 mAh | 3.7 V | 10×34×50 mm | $7–9 |
| PKCell LP606090 | 4000 mAh | 3.7 V | 6×60×90 mm | $14–18 |
| Tattu 1S 4.35V slim | 2500 mAh | 3.8 V HV | varies | $18–25 |
| Tattu 2S R-line 1300 mAh | 1300 mAh | 7.6 V HV | slim brick | $25–35 |
| Generic 3.7 V 10000 mAh slab | 10000 mAh | 3.7 V | 8×60×110 mm | $20–28 |

Connectors are typically 2-pin JST-PH (≤2 A), JST-XH for balance leads, or XT30/XT60 for higher current. Always wire a balance lead if multi-cell. **Pros:** ultra-thin, custom shapes available. **Cons:** fire risk if punctured, lower CDR, faster aging.

---

## 4. BMS / Protection Boards

Required for any pack that isn't pre-built. Match S-count to series cells and pick discharge rating ≥ 1.5× peak load.

| BMS | Config | Continuous A | Features | Price |
|---|---|---|---|---|
| Generic HX-1S-FB6 / TP4056 | 1S | 1 A charge / 3 A discharge | Over/under-V, short-circuit; cheapest option | $0.50–1 |
| Generic 2S 8 A | 2S | 8 A | Basic protection; no balancing | $2–4 |
| HX 3S 25 A | 3S | 25 A | OV/UV/OC/short | $4–7 |
| HX 4S 40 A | 4S | 40 A | OV/UV/OC/short, common-port | $6–10 |
| JBD 4S 60 A (SP04S034) | 4S | 60 A | Balanced, separated port | $14–22 |
| JBD Smart BMS 4S 60 A BT | 4S | 60 A | App via BT, SoC, temp probe | $35–55 |
| DALY 4S 100 A | 4S | 100 A | Common-port, robust | $22–30 |
| DALY Smart BMS 4S 100 A BT | 4S | 100 A | BT app, SoC, UART, balancer ([DALY](https://www.dalybms.com/smart-bms/)) | $50–75 |
| JK Smart BMS 4S 60 A active balance | 4S | 60 A | Active 2 A balance, BT, CAN | $70–95 |

**Pros:** Smart-BMS gives accurate SoC, telemetry, and remote shutoff. **Cons:** Cheap dumb-BMS boards lack temperature sensing; many "common-port" boards drop charging if a protection trips on discharge.

---

## 5. DC-DC Converters / Regulators

Convert pack voltage (e.g., 3S 11.1 V) to your rails (5 V for SBC, 12 V for display). Efficiency = runtime.

| Module | Type | V_in | V_out | I_out | Efficiency | Price |
|---|---|---|---|---|---|---|
| LM2596 generic | Buck | 4–35 V | 1.2–35 V adj | 2 A (3 A peak) | ~80–85% | $1–2 |
| MP1584EN module | Buck | 4.5–28 V | 0.8–20 V adj | 3 A | ~88% | $1.50–3 |
| XL4015 module | Buck | 5–32 V | 0.8–30 V adj | 5 A | ~90% | $3–5 |
| Pololu D24V22F5 | Buck | 4.5–36 V | 5 V fixed | 2.2 A | ~93% | $15 |
| Pololu D24V50F5 | Buck | 6–38 V | 5 V fixed | 5 A | ~94% ([Pololu](https://www.pololu.com/product/2851)) | $20 |
| Pololu S7V8A adj. | Buck-boost | 2.7–11.8 V | 2.5–8 V | ~1 A | ~92% | $15 |
| Pololu D24V90F5 | Buck | 6.5–40 V | 5 V | 9 A | ~95% | $30 |
| Mean Well RSD-30G-5 | Isolated | 9–36 V | 5 V | 6 A | ~85% | $35 |
| Mean Well DDR-30G-12 DIN | Isolated | 9–36 V | 12 V | 2.5 A | ~87% | $40 |

**Pros:** Pololu/Mean Well = clean low-EMI rails for radios/audio. **Cons:** Cheap LM2596/XL4015 modules sag under load and produce HF noise; derate listed current 30–50% for thermal margin.

---

## 6. USB-C PD Trigger and Source Boards

Run your deck from any USB-C PD wall wart, laptop charger, or power bank. Trigger boards request 9/12/15/20 V from the source.

| Board | IC | Output | Control | Price |
|---|---|---|---|---|
| ZY12PDN | Custom | 5/9/12/15/20 V | Button cycle, 100 W | $5–8 |
| ZYPDS YZX Studio | Custom | Configurable | Solder/button | $8–12 |
| Adafruit HUSB238 STEMMA QT | HUSB238 | 5/9/12/15/20 V | I2C or jumpers | $7 |
| WeAct AP33772 board | AP33772 | PPS + fixed | I2C, PPS support | $8–12 |
| Adafruit AP33772S | AP33772S | PPS + EPR | I2C, up to 28 V | $10 |
| Generic PD trigger 65 W | Various | Selectable | Solder pads | $3–5 |
| TI BQ25895 charger module | BQ25895 | 1S Li-ion charge | I2C, up to 5 A, MPPT-ish | $8–14 |
| IP5328P power-bank IC board | IP5328P | 5/9/12 V QC + boost | Push-button | $4–7 |
| Adafruit BQ24074 charger | BQ24074 | Solar/USB charge | Pass-through | $15 |

**Pros:** turn a USB-C PD brick into a deck PSU, eliminate barrel jacks. **Cons:** Button-only triggers can be cycled accidentally; prefer I2C parts (HUSB238/AP33772) for safety.

---

## 7. Solar Input

Useful for trickle-charging during field ops; not realistic as a primary supply for 30 W+ x86 decks.

| Item | Power | Voltage | Notes | Price |
|---|---|---|---|---|
| Voltaic P122 mini | 0.3 W | 5 V (~6 V Voc) | 50 mA peak, ETFE | $4 |
| Voltaic P124 | 1.2 W | 5 V | 200 mA peak | $14 ([Adafruit](https://www.adafruit.com/product/5368)) |
| Voltaic P105 ETFE | 5 W | 5 V | 940 mA peak, SunPower cells | $40 ([Adafruit](https://www.adafruit.com/product/5367)) |
| Voltaic P110 | 10 W | 5 V | Foldable, ~1.8 A | $65 |
| PowerFilm MP3-25 | 0.75 W | 3 V | Indoor/outdoor flexible | $30 |
| PowerFilm LightSaver | 2.5 W (panel) | USB out | Integrated 3200 mAh | $100 |
| Adafruit Sunny Buddy MPPT | up to 1S Li | adj. | 450 mA default, up to 2 A | $18 |
| Adafruit bq24074 USB/DC/solar charger | 1S | 5–10 V in | MPPT pin, 1.5 A | $15 |
| Genasun GV-5 MPPT 5 A | 5 A | Li-ion configurable | High-end, ~98% MPPT | $90 |

**Pros:** off-grid runtime, "set and forget" trickle charging. **Cons:** Wh per dollar is terrible vs. carrying spare cells; foldable panels weigh more than the energy they capture in a typical day.

---

## 8. Repurposed Power Banks (Battery + PSU in one)

The easiest 2026 path: a single ≤100 Wh USB-C PD power bank IS the power system. With a PD trigger board you have 5/9/12/15/20 V on tap.

| Power Bank | Capacity | Wh | Output | Price |
|---|---|---|---|---|
| Anker 737 (PowerCore 24K) | 24000 mAh | **88.56 Wh** | 140 W PD3.1 + 18 W USB-A | $130–150 ([Anker](https://www.anker.com/products/a1289)) |
| Anker Prime 27650 mAh 250 W | 27650 mAh | **99.54 Wh** | 250 W combined, OLED | $170–200 |
| Anker Prime 26250 mAh 300 W | 26250 mAh | **94.5 Wh** | 300 W max, app control, TSA-OK | $180 |
| Baseus Blade 2 | 20000 mAh | **74 Wh** | 100 W PD, slim laptop-style | $80–100 |
| INIU P63 100 W | 25000 mAh | **92 Wh** | 100 W PD | $60–80 |
| UGREEN Nexode 145 W | 25000 mAh | **97 Wh** | 145 W PD3.1 | $100 |
| Shargeek Storm 2 Slim | 20000 mAh | **74 Wh** | 100 W, transparent | $130 |

**Pros:** safety-certified, FAA-friendly Wh ratings, integrated BMS/fuel gauge/display, replaceable. **Cons:** no native 12 V (need a PD trigger), can't be hard-mounted easily, additional weight from case/screen.

---

## 9. Power-Monitoring / Fuel Gauges

Without telemetry you're flying blind. Cheap to add; saves your pack.

| Module | Method | Range | Notes | Price |
|---|---|---|---|---|
| INA219 breakout (Adafruit #904) | Shunt + I2C | 26 V / ±3.2 A | Classic, ±0.5% ([Adafruit](https://www.adafruit.com/product/904)) | $11 |
| INA219 generic | Shunt + I2C | 26 V / 3.2 A | Bare module | $2–3 |
| INA226 module | Shunt + I2C | 36 V / configurable | Higher resolution | $5–8 |
| Adafruit INA260 STEMMA QT (#4226) | Integrated shunt | 36 V / 15 A | 1.5 mA resolution, no external shunt ([Adafruit](https://www.adafruit.com/product/4226)) | $13 |
| Adafruit MAX17048 (#5580) | Coulomb-counting equivalent | 1S Li-ion/LiPo | True % SoC w/ ModelGauge ([Adafruit](https://www.adafruit.com/product/5580)) | $10 |
| MAX17260 module | Coulomb counter | 1–7S | Real Ah tracking | $15–20 |
| Bare voltmeter LED panel | Analog | 4.5–30 V | Power-budget-eating; informational only | $2 |
| Joulescope JS220 | Pro bench | nA–10 A | Lab calibration; only if you're tuning sleep modes | $899 |

**Pros:** MAX17048 gives you a phone-grade battery percentage on a 1S pack for $10. **Cons:** INA-style sensors only show instantaneous V/I — you must integrate in firmware for Wh used.

---

## 10. Connectors and Cabling

Connector failures are the most common cyberdeck repair. Spec for 2× peak current, fuse every battery output.

| Connector | Ampacity | Use | Notes |
|---|---|---|---|
| JST-PH 2.0 mm | ~2 A | Single LiPo cells | Adafruit/SparkFun standard |
| JST-SH 1.0 mm | ~1 A | Tiny LiPos, sensors | STEMMA QT signal connector (not for power) |
| JST-XH 2.54 mm | ~3 A per pin | Balance leads | Multi-cell balance only — never main current |
| JST-RCY (BEC) | ~5 A | RC packs | Legacy, avoid |
| XT30 | 30 A continuous | 1S–3S small packs | Compact, polarized |
| XT60 | 60 A continuous | 3S–6S main packs | Cyberdeck workhorse |
| XT90 | 90 A continuous | Anti-spark variant | Overkill for most decks |
| Anderson Powerpole PP15/30/45 | 15/30/45 A | Modular, swappable | Genderless, hot-swap (ham radio standard) |
| Anderson PowerPole APP-180 | 180 A | Big packs | Industrial |
| USB-C cable 3 A (60 W) | 3 A @ 20 V | Default PD | Most cheap cables |
| USB-C cable 5 A (100 W) e-marked | 5 A @ 20 V | Laptop-class | Must have e-marker chip |
| USB-C cable EPR (240 W) | 5 A @ 48 V | PD 3.1 EPR | Required for 28 V/36 V/48 V triggers |

**Fuse selection:** ATC/ATO blade or PTC resettable; size at 1.25–1.5× continuous load, never over the BMS rating. Place fuse on the **B+ wire as close to the pack as possible.** A 4S 5 Ah pack with a 5 A peak load should use a 7.5 A fast-blow.

---

## How to Choose: Power Budget, Runtime, Safety

### Step 1 — Estimate your continuous load (Watts)

| Subsystem | Typical Idle | Typical Active |
|---|---|---|
| Pi Zero 2 W | 0.4 W | 1.5 W |
| Pi 4B | 2.7 W | 6.5 W |
| Pi 5 | 3 W | 8–12 W |
| Pi 5 + NVMe + 7" display | 5 W | **15–18 W** |
| LattePanda Mu (x86 N100) | 4 W | 12–18 W |
| Framework 13 mainboard (i5/i7) | 6 W | **30–55 W** |
| GPD/Steam Deck APU mainboard | 7 W | **35–65 W** |
| HDMI 5–7" display | 1.5 W | 3–4 W |
| Mechanical keyboard (RGB off) | 0.1 W | 0.3 W |
| Mechanical keyboard (RGB on) | 0.5 W | 2 W |
| LTE/4G modem | 0.5 W | 2.5 W peak 5 W |

**Rule of thumb:** SBC decks land at **10–25 W active.** x86 decks land at **30–65 W active.**

### Step 2 — Runtime math

> **Runtime (hours) = Pack Wh × System Efficiency / Average Load W**

Use **0.85** as efficiency for a buck regulator chain, **0.75** if you boost then buck. Example: 3S2P 30Q pack = 11.1 V × 6.0 Ah = **66.6 Wh**. Pi 5 deck at 12 W average: 66.6 × 0.85 / 12 = **~4.7 hours.**

### Step 3 — Charging while using

Spec a charger ≥ 1.5× your average draw so the pack still gains charge during use. For PD-fed builds, a 65 W brick comfortably runs a 30 W deck while charging at ~30 W net. **Use a charger IC with thermal foldback** (BQ25895, IP5328P) — never trickle through a TP4056 above 1 A indoors.

### Step 4 — Thermal safety

- Mount cells with **2 mm air gap** between cells and chassis; LiPo pouches need a hard backer.
- Add an NTC thermistor on the pack — most Smart-BMS units accept one; budget ~$2.
- Cells at 100% SoC stored hot lose ~20% capacity/yr; store decks at **40–60% SoC.**
- Never charge below 0 °C — plating destroys Li-ion cells.

### Step 5 — Air-travel limits (critical for 2026)

| Battery Wh | Carry-on | Checked | Notes |
|---|---|---|---|
| ≤ 100 Wh | **Yes, unlimited installed; spares carry-on only** | Installed in device only | Standard laptop/power-bank tier ([FAA](https://www.faa.gov/hazmat/packsafe/airline-passengers-and-batteries)) |
| 100–160 Wh | **Yes, with airline approval** | No | **Max 2 spares per passenger** |
| > 160 Wh | No | No | Cargo only (special permit) |

**ICAO addendum effective March 27, 2026:** Passengers limited to **two power banks** total, no in-flight recharging from seat USB, devices must stay accessible (seat pocket / under seat, not overhead). Rolling out across all 193 ICAO member states. U.S. carriers (American eff. May 1, 2026; Southwest already enforcing) are explicit about the two-power-bank cap.

**Practical implication for builders:** Keep total deck pack ≤ **99 Wh** for hassle-free travel. A 4S2P P42A pack at 14.4 V × 8.4 Ah = **121 Wh** — exceeds the free limit, requires approval, counts as one of your two spare allotments if removable. The sweet spot is **3S2P 30Q (~67 Wh)** or **2× 21700 P42A 4S (~60 Wh)**: both pre-cleared by FAA/TSA and leave headroom for a separate 99 Wh USB-C power bank as backup.

### Recommended starter stacks

- **Ultralight Pi Zero deck:** Pi Zero 2 W + PiSugar 3 + INA219 + JST-PH. ~$70 total power BOM, ~8 h runtime.
- **Pi 5 daily-driver deck:** Pi 5 + Geekworm X1202 + 4× Samsung 30Q + DALY 4S 100 A + INA260 + XT60. ~$120, ~6–8 h runtime, FAA-OK.
- **x86 Framework deck:** Anker Prime 250 W (99.5 Wh power bank) + Adafruit AP33772S trigger @ 20 V + Pololu D24V90F5 for 5 V rail. ~$240, drops in zero-BMS-headache, FAA-friendly.
- **Field/off-grid:** 3S2P 21700 P42A pack + JBD Smart 4S BT BMS + Genasun GV-5 MPPT + Voltaic P110 10 W panel + BQ25895 USB-C input. ~$320, multi-day runtime with sun.

---

## Sources

### Regulatory / Air Travel
- [FAA PackSafe — Lithium Batteries](https://www.faa.gov/hazmat/packsafe/lithium-batteries) · [FAA PackSafe — Airline Passengers and Batteries](https://www.faa.gov/hazmat/packsafe/airline-passengers-and-batteries)
- [TSA Lithium Battery Rules (>100 Wh)](https://www.tsa.gov/travel/security-screening/whatcanibring/items/lithium-batteries-more-100-watt-hours)
- [CineD — Flying with Batteries in 2026 (ICAO update)](https://www.cined.com/flying-with-batteries-in-2026-what-the-new-global-power-bank-rules-mean-for-filmmakers/)
- [TheStreet — Southwest Lithium Battery Rules](https://www.thestreet.com/travel/southwest-airlines-cites-faa-guidance-for-strict-new-lithium-battery-rules)

### UPS HATs and Power Modules
- [PiSugar 3 Plus](https://www.pisugar.com/products/pisugar-3-plus-raspberry-pi-ups) · [CNX Software PiSugar3 writeup](https://www.cnx-software.com/2025/01/06/pisugar3-is-a-low-cost-raspberry-pi-ups-module-with-rtc-hardware-battery-protection-and-power-management-features/)
- [Waveshare UPS HAT (E)](https://www.waveshare.com/ups-hat-e.htm)
- [Geekworm X1200](https://geekworm.com/products/x1200) · [Geekworm X1202](https://geekworm.com/products/x1202)
- [Pimoroni Pico LiPo SHIM](https://shop.pimoroni.com/en-us/products/pico-lipo-shim)

### Cells, BMS, Regulators
- [Origin-IC — Molicel P28A vs Samsung 30Q](https://www.origin-ic.com/blog/molicel-p28a-vs-samsung-30q-18650-battery-review/48406)
- [18650 Battery Store — Samsung 40T](https://www.18650batterystore.com/products/samsung-40t)
- [Vaping360 — Best 21700 Cells 2026](https://vaping360.com/best-batteries/21700s/)
- [DALY Smart BMS](https://www.dalybms.com/smart-bms/)
- [Pololu D24V50F5 5V buck](https://www.pololu.com/product/2851)

### USB-C PD Triggers and Power Banks
- [Gough's Tech Zone — PD Trigger Board Testing](https://goughlui.com/2023/10/22/tested-project-usb-c-pd-trigger-decoy-boards-yzx-studio-zypds-zy12pdn/)
- [ZY12PDN trigger (Amazon)](https://www.amazon.com/Acxico-Trigger-Detector-Charging-ZY12PDN/dp/B081YVSCTL)
- [Anker 737 PowerCore 24K](https://www.anker.com/products/a1289) · [Anker 737 review 2026](https://smartgadgetkit.com/anker-737-power-bank-review/)
- [Anker Prime 26250 mAh 300 W (Amazon)](https://www.amazon.com/Anker-Portable-Charging-TSA-Approved-Included/dp/B0F66LNB8D)

### Solar and Fuel Gauges
- [Voltaic P124 (Adafruit)](https://www.adafruit.com/product/5368) · [Voltaic P105 ETFE (Adafruit)](https://www.adafruit.com/product/5367)
- [Adafruit INA219 (#904)](https://www.adafruit.com/product/904) · [Adafruit INA260 STEMMA QT (#4226)](https://www.adafruit.com/product/4226) · [Adafruit MAX17048 (#5580)](https://www.adafruit.com/product/5580)

### Connectors
- [Grepow — LiPo Battery Connector Types](https://www.grepow.com/blog/exploring-lipo-battery-connector-types.html)
