# Header-mate verification — rev1 (broken) vs rev2 (fixed)

What A7S pin each shield pad physically contacts, before and after the `build_pcb.py` **rot 90°→270°** fix.

- **rev1 (fabbed, DOA):** pad *P* mated A7S pin *(N+1−P)* — a 180° diagonal flip.
- **rev2 (fixed):** pad *P* mates A7S pin *P*.

**Legend:** ❌ SHORT = a supply driven into GND (this is what killed the A7S). ❌ pwr→GPIO = 5V/3V3 onto a signal pin. ⚠ = benign-but-wrong contact. ✅ = correct.

### 30-pin header (J1)

| shield pad | shield net (SoC) | rev1 → A7S pin (func) | rev1 | rev2 → A7S pin (func) | rev2 |
|--:|---|---|:--:|---|:--:|
| 1 | +3V3 (+3.3V) | pin 30 (GND) | ❌ SHORT | pin 1 (+3.3V) | ✅ |
| 2 | +5V (+5V) | pin 29 (PB2) | ❌ pwr→GPIO | pin 2 (+5V) | ✅ |
| 3 | UART3_RX (PJ23) | pin 28 (PD16) | ⚠ wrong sig | pin 3 (PJ23) | ✅ |
| 4 | +5V (+5V) | pin 27 (PD17) | ❌ pwr→GPIO | pin 4 (+5V) | ✅ |
| 5 | UART3_TX (PJ22) | pin 26 (PD14) | ⚠ wrong sig | pin 5 (PJ22) | ✅ |
| 6 | GND (GND) | pin 25 (GND) | ✅ ok | pin 6 (GND) | ✅ |
| 7 | RP2040_RX/U2TX (PB0) | pin 24 (PD10) | ⚠ wrong sig | pin 7 (PB0) | ✅ |
| 8 | console_TX (PB9) | pin 23 (PD11) | ⚠ wrong sig | pin 8 (PB9) | ✅ |
| 9 | GND (GND) | pin 22 (PL5) | ⚠ GND→sig | pin 9 (GND) | ✅ |
| 10 | console_RX (PB10) | pin 21 (PD13) | ⚠ wrong sig | pin 10 (PB10) | ✅ |
| 11 | RP2040_TX/U2RX (PB1) | pin 20 (GND) | ⚠ wrong sig | pin 11 (PB1) | ✅ |
| 12 | (unused) (PB5) | pin 19 (PD12) | ⚠ wrong sig | pin 12 (PB5) | ✅ |
| 13 | (unused) (PL6) | pin 18 (PJ25) | ⚠ wrong sig | pin 13 (PL6) | ✅ |
| 14 | GND (GND) | pin 17 (+3.3V) | ❌ SHORT | pin 14 (GND) | ✅ |
| 15 | (unused) (PL7) | pin 16 (PJ24) | ⚠ wrong sig | pin 15 (PL7) | ✅ |
| 16 | RADIO1_CS (PJ24) | pin 15 (PL7) | ⚠ wrong sig | pin 16 (PJ24) | ✅ |
| 17 | +3V3 (+3.3V) | pin 14 (GND) | ❌ SHORT | pin 17 (+3.3V) | ✅ |
| 18 | RADIO1_FLEXB (PJ25) | pin 13 (PL6) | ⚠ wrong sig | pin 18 (PJ25) | ✅ |
| 19 | SPI1_MOSI (PD12) | pin 12 (PB5) | ⚠ wrong sig | pin 19 (PD12) | ✅ |
| 20 | GND (GND) | pin 11 (PB1) | ⚠ GND→sig | pin 20 (GND) | ✅ |
| 21 | SPI1_MISO (PD13) | pin 10 (PB10) | ⚠ wrong sig | pin 21 (PD13) | ✅ |
| 22 | (unused) (PL5) | pin 9 (GND) | ⚠ wrong sig | pin 22 (PL5) | ✅ |
| 23 | SPI1_CLK (PD11) | pin 8 (PB9) | ⚠ wrong sig | pin 23 (PD11) | ✅ |
| 24 | TFT_CS (PD10) | pin 7 (PB0) | ⚠ wrong sig | pin 24 (PD10) | ✅ |
| 25 | GND (GND) | pin 6 (GND) | ✅ ok | pin 25 (GND) | ✅ |
| 26 | TFT_DC (PD14) | pin 5 (PJ22) | ⚠ wrong sig | pin 26 (PD14) | ✅ |
| 27 | I2C_SDA (PD17) | pin 4 (+5V) | ⚠ wrong sig | pin 27 (PD17) | ✅ |
| 28 | I2C_SCK (PD16) | pin 3 (PJ23) | ⚠ wrong sig | pin 28 (PD16) | ✅ |
| 29 | TFT_RST (PB2) | pin 2 (+5V) | ⚠ wrong sig | pin 29 (PB2) | ✅ |
| 30 | GND (GND) | pin 1 (+3.3V) | ❌ SHORT | pin 30 (GND) | ✅ |

### 15-pin header (J2)

| shield pad | shield net (SoC) | rev1 → A7S pin (func) | rev1 | rev2 → A7S pin (func) | rev2 |
|--:|---|---|:--:|---|:--:|
| 1 | RADIO1_FLEXA (PB3) | pin 15 (PG5) | ⚠ wrong sig | pin 1 (PB3) | ✅ |
| 2 | TOUCH_CS (PM3) | pin 14 (PG4) | ⚠ wrong sig | pin 2 (PM3) | ✅ |
| 3 | TOUCH_IRQ (PM4) | pin 13 (PG3) | ⚠ wrong sig | pin 3 (PM4) | ✅ |
| 4 | GND (GND) | pin 12 (PG2) | ⚠ GND→sig | pin 4 (GND) | ✅ |
| 5 | TFT_BL (PB6) | pin 11 (PG1) | ⚠ wrong sig | pin 5 (PB6) | ✅ |
| 6 | (spare) (PB4) | pin 10 (PG0) | ⚠ wrong sig | pin 6 (PB4) | ✅ |
| 7 | RADIO2_FLEXA (PB8) | pin 9 (GND) | ⚠ wrong sig | pin 7 (PB8) | ✅ |
| 8 | RADIO2_CS (PB7) | pin 8 (PB7) | ✅ ok | pin 8 (PB7) | ✅ |
| 9 | GND (GND) | pin 7 (PB8) | ⚠ GND→sig | pin 9 (GND) | ✅ |
| 10 | RADIO2_FLEXB (PG0) | pin 6 (PB4) | ⚠ wrong sig | pin 10 (PG0) | ✅ |
| 11 | RADIO1_AUX (PG1) | pin 5 (PB6) | ⚠ wrong sig | pin 11 (PG1) | ✅ |
| 12 | RADIO2_AUX (PG2) | pin 4 (GND) | ⚠ wrong sig | pin 12 (PG2) | ✅ |
| 13 | (spare) (PG3) | pin 3 (PM4) | ⚠ wrong sig | pin 13 (PG3) | ✅ |
| 14 | (spare) (PG4) | pin 2 (PM3) | ⚠ wrong sig | pin 14 (PG4) | ✅ |
| 15 | (spare) (PG5) | pin 1 (PB3) | ⚠ wrong sig | pin 15 (PG5) | ✅ |

### Power / ground safety summary (rev2)

| rail | shield pads | → A7S pins | status |
|---|---|---|:--:|
| +5V  | J1: 2, 4 | 2, 4 | ✅ |
| +3V3 | J1: 1, 17 | 1, 17 | ✅ |
| GND  | J1: 6,9,14,20,25,30 · J2: 4,9 | same | ✅ |

**Verify on the fabbed rev2 bare board before mating a live A7S:** with an ohmmeter, J1 pads 1/2/4/17 → GND must read **open**. Then power the A7S alone (LED blinks), power off, mate, power on.
