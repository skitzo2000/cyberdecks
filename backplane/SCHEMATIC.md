# A7S Cyberdeck Backplane — Schematic (netlist)

Authoritative electrical design for the shield. This is the "schematic figured out" — every component
(refdes/value/footprint) and every net (all pins). Transcribes 1:1 into KiCad; `a7s_backplane_skidl.py`
generates a KiCad netlist from the same definition. Pin maps per `BACKPLANE-DESIGN.md` (A7S BSP pinout).

Convention: `Jx.n` = pin n of connector Jx. Net names are CAPS. **GND** and **+5V/+3V3** are global.

---

## 1. Sheets (functional blocks)
1. **HDR** — A7S host headers J1 (2×15) + J2 (1×15): the pin→net fan-out.
2. **PWR** — 5V tap, polyfuse, 3V3 LDO, radio load switch, bulk/decoupling.
3. **DISP** — SPI1 bus + TFT/ILI9341 + XPT2046 touch (J3).
4. **RADIO** — two 8+1 sockets (J5/J5b, J6/J6b) on SPI1.
5. **INPUT** — RP2040-Zero (A1) + on-shield buttons (SW1–4) + J8 off-board solder field.
6. **IO** — UART3/I²C/spare breakout J7, QWIIC J9, console test points.

---

## 2. Components

| Ref | Value / Part | Footprint | Block |
|---|---|---|---|
| J1 | Header 2×15 female 2.54 | `Connector:Conn_02x15_Odd_Even` / socket | HDR |
| J2 | Header 1×15 female 2.54 | `Conn_01x15` socket | HDR |
| J3 | TFT 2.8" ILI9341+XPT2046, 1×14 socket | `Conn_01x14` | DISP |
| J5 | Radio1 socket 2×4 (nRF24 order) | `Conn_02x04_Odd_Even` | RADIO |
| J5b | Radio1 AUX 1×1 | `Conn_01x01` | RADIO |
| J6 | Radio2 socket 2×4 | `Conn_02x04_Odd_Even` | RADIO |
| J6b | Radio2 AUX 1×1 | `Conn_01x01` | RADIO |
| J7 | Breakout 2×7 (→ casing breadboards) | `Conn_02x07_Odd_Even` | IO |
| J8 | Input solder field 1×16 (edge, beginner holes) | `Conn_01x16` Ø1.0/2.3 | INPUT |
| J9 | QWIIC/I²C 1×4 | `Conn_01x04` | IO |
| A1 | RP2040-Zero module | castellated module fp (custom) | INPUT |
| SW1–SW4 | Tactile button 6 mm | `SW_Push` THT | INPUT |
| F1 | Polyfuse 1.1 A (MF-R110) | 1206 / THT | PWR |
| U1 | AP2112K-3.3 LDO (600 mA) | SOT-23-5 | PWR |
| U2 | TPS22918 load switch | SOT-23-6 | PWR |
| C1 | 470 µF / 10 V (5V bulk) | THT radial | PWR |
| C2 | 470 µF / 10 V (3V3_SW radio) | THT radial | PWR |
| C3,C4 | 1 µF (LDO in/out) | 0603 | PWR |
| C5 | 1 µF (load-switch VOUT) | 0603 | PWR |
| C6 | 0.1 µF (RP2040) | 0603 | INPUT |
| C7 | 0.1 µF (TFT) | 0603 | DISP |
| C8,C9 | 0.1 µF (radio1/2 3V3) | 0603 | RADIO |
| C10,C11 | 0.1 µF (LDO/load-sw) | 0603 | PWR |
| R1,R2 | 2.2 kΩ (I²C pull-up) | 0603 | IO |
| R3,R4 | 100 Ω (UART series) | 0603 | INPUT |
| R5 | 10 kΩ (3V3_SW_EN pulldown) | 0603 | PWR |
| TP1,TP2 | Test point (console) | TestPoint | IO |

> **Ambidextrous (layout note, not extra nets):** SW1–4, J5/J5b, J6/J6b, J7, J8 get a **second DNP
> footprint on the opposite (top) overhang strip wired to the identical nets**; populate only the strip
> that ends up at the bottom for the build (§9 of design doc). Schematic lists each once.

---

## 3. A7S header pin → net (the fan-out)

### J1 — 2×15 (mates A7S 30-pin)
| Pin | A7S | Net | | Pin | A7S | Net |
|--:|---|---|---|--:|---|---|
| 1 | 3V3 | +3V3_SBC* | | 2 | 5V | +5V_IN |
| 3 | PJ23 | UART3_RX | | 4 | 5V | +5V_IN |
| 5 | PJ22 | UART3_TX | | 6 | GND | GND |
| 7 | PB0 | A7S_U2TX | | 8 | PB9 | CONSOLE_TX (TP1) |
| 9 | GND | GND | | 10 | PB10 | CONSOLE_RX (TP2) |
| 11 | PB1 | A7S_U2RX | | 12 | — | NC |
| 13 | — | NC | | 14 | GND | GND |
| 15 | — | NC | | 16 | PJ24 | RADIO1_CS |
| 17 | 3V3 | +3V3_SBC* | | 18 | PJ25 | RADIO1_FLEXB |
| 19 | PD12 | SPI_MOSI | | 20 | GND | GND |
| 21 | PD13 | SPI_MISO | | 22 | — | NC |
| 23 | PD11 | SPI_SCK | | 24 | PD10 | TFT_CS |
| 25 | GND | GND | | 26 | PD14 | TFT_DC |
| 27 | PD17 | I2C_SDA | | 28 | PD16 | I2C_SCK |
| 29 | PB2 | TFT_RST | | 30 | GND | GND |

\* +3V3_SBC = A7S 3V3 output, **left unloaded** (sense only) — radios/peripherals run off +3V3_SW.

### J2 — 1×15 (mates A7S 15-pin)
| Pin | A7S | Net |
|--:|---|---|
| 1 | PB3 | RADIO1_FLEXA |
| 2 | PM3 | TOUCH_CS |
| 3 | PM4 | TOUCH_IRQ |
| 4 | GND | GND |
| 5 | PB6 | TFT_BL |
| 6 | PB4 | 3V3_SW_EN |
| 7 | PB8 | RADIO2_FLEXA |
| 8 | PB7 | RADIO2_CS |
| 9 | GND | GND |
| 10 | PG0 | RADIO2_FLEXB |
| 11 | PG1 | RADIO1_AUX |
| 12 | PG2 | RADIO2_AUX |
| 13 | PG3 | SPARE0 |
| 14 | PG4 | SPARE1 |
| 15 | PG5 | SPARE2 |

---

## 4. Power tree (PWR)

```
+5V_IN (J1.2,J1.4) -> F1 -> +5V
  +5V: C1(470u)+, C10(0.1u), U1.VIN, U1.EN, A1.5V, J3.1(TFT VCC), J7.6
  U1 AP2112K-3.3: VIN=+5V, EN=+5V, GND, VOUT=+3V3_LDO ; C3(1u) in, C4(1u) out
  +3V3_LDO -> U2.VIN (TPS22918)
  U2: VIN=+3V3_LDO, GND, ON=3V3_SW_EN, VOUT=+3V3_SW ; C11(0.1u), C5(1u) out
     3V3_SW_EN: J2.6(PB4) + R5(10k) pulldown to GND  (radio rail OFF until host drives PB4 high)
  +3V3_SW: C2(470u)+, J5.2, J6.2, C8, C9, J7.5, J9.2, R1, R2
RP_3V3 = A1.3V3 (RP2040 onboard reg out) -> J8 JOY/ENC 3V3, C6(0.1u)
GND = global.
```

> U1 EN tied high (always on). U2 EN (`ON`) is GPIO-gated by PB4 so the host can power-cycle wedged
> radios. **Confirm U2 exact pinout** (VIN/GND/ON/CT/VOUT) against the chosen TPS22918 variant;
> CT pin → leave open or small cap for soft-start.

---

## 5. Net list (every net → all pins)

**Power**
- `+5V_IN` : J1.2, J1.4, F1.1
- `+5V` : F1.2, C1.1, C10.1, U1.1(VIN), U1.3(EN), A1.5V, J3.1, J7.6
- `+3V3_LDO` : U1.5(VOUT), C3?.. , C4.1, U2.VIN
- `+3V3_SW` : U2.VOUT, C2.1, C5.1, C11.1, J5.2, J6.2, C8.1, C9.1, J7.5, J9.2, R1.1, R2.1
- `+3V3_SBC` : J1.1, J1.17  *(no other connections — reserved)*
- `RP_3V3` : A1.3V3, C6.1, J8.1(JOY_3V3), J8.9(ENC_3V3 opt)
- `GND` : J1.6, J1.9, J1.14, J1.20, J1.25, J1.30, J2.4, J2.9, F1?—no, C1.2, C2.2, C3.2, C4.2, C5.2, C6.2, C7.2, C8.2, C9.2, C10.2, C11.2, U1.2, U2.GND, A1.GND, R5.2, SW1.2, SW2.2, SW3.2, SW4.2, J3.2, J5.1, J6.1, J7.7, J7.8, J8(GNDs), J9.1, TP—

**SPI1 bus**
- `SPI_SCK` : J1.23, J3.7, J3.10, J5.5, J6.5
- `SPI_MOSI` : J1.19, J3.6, J3.12, J5.6, J6.6
- `SPI_MISO` : J1.21, J3.13, J5.7, J6.7   *(NOT J3.9 — TFT SDO left NC, write-only)*

**TFT / touch**
- `TFT_CS` : J1.24, J3.3
- `TFT_DC` : J1.26, J3.5
- `TFT_RST` : J1.29, J3.4
- `TFT_BL` : J2.5, J3.8
- `TOUCH_CS` : J2.2, J3.11
- `TOUCH_IRQ` : J2.3, J3.14
- `TFT_SDO_NC` : J3.9  *(no-connect)*

**Radio 1**
- `RADIO1_CS` : J1.16, J5.4
- `RADIO1_FLEXA` : J2.1, J5.3
- `RADIO1_FLEXB` : J1.18, J5.8
- `RADIO1_AUX` : J2.11, J5b.1

**Radio 2**
- `RADIO2_CS` : J2.8, J6.4
- `RADIO2_FLEXA` : J2.7, J6.3
- `RADIO2_FLEXB` : J2.10, J6.8
- `RADIO2_AUX` : J2.12, J6b.1

**Radio power/decap**: C8 across J5.2/J5.1 (+3V3_SW/GND); C9 across J6.2/J6.1.

**RP2040 ↔ A7S UART2 (cross-over, series R)**
- `A7S_U2TX` : J1.7, R3.1
- `RP_RX` : R3.2, A1.GP1
- `A7S_U2RX` : J1.11, R4.1
- `RP_TX` : R4.2, A1.GP0

**On-shield buttons (RP2040 internal pull-ups; switch to GND)**
- `BTN1` : A1.GP2, SW1.1   | `BTN2` : A1.GP3, SW2.1
- `BTN3` : A1.GP4, SW3.1   | `BTN4` : A1.GP5, SW4.1
- (SW1–4 pin2 → GND)

**Off-board inputs → J8 solder field**
- `BTN5` : A1.GP6, J8.13
- `BTN6` : A1.GP7, J8.14
- `JOY_X` : A1.GP26, J8.3
- `JOY_Y` : A1.GP27, J8.4
- `JOY_SW` : A1.GP8, J8.5
- `ENC_A` : A1.GP9, J8.6
- `ENC_B` : A1.GP10, J8.7
- `ENC_SW` : A1.GP11, J8.8
- J8.1=RP_3V3, J8.2=GND, J8.9=RP_3V3(enc opt), J8.10=GND, J8.15=GND, J8.16=GND

**I²C**
- `I2C_SDA` : J1.27, R1.2, J7.3, J9.3
- `I2C_SCK` : J1.28, R2.2, J7.4, J9.4
- (R1/R2 other end → +3V3_SW)

**UART3 + spares → breakout J7 (2×7)**
- `UART3_TX` : J1.5, J7.1
- `UART3_RX` : J1.3, J7.2
- `SPARE0` : J2.13, J7.9 | `SPARE1` : J2.14, J7.10 | `SPARE2` : J2.15, J7.11
- J7.5=+3V3_SW, J7.6=+5V, J7.7=GND, J7.8=GND, J7.12=GND, J7.13/14 = spare GPIO/NC

**Load-switch enable**
- `3V3_SW_EN` : J2.6, U2.ON, R5.1   (R5.2 → GND)

**Console (test points, unloaded)**
- `CONSOLE_TX` : J1.8, TP1
- `CONSOLE_RX` : J1.10, TP2

**No-connect**: J1.12, J1.13, J1.15, J1.22; J3.9; A1.GP12, GP13, GP14, GP15, GP28, GP29.

---

## 6. RP2040-Zero (A1) pin usage
| Pin | Net | | Pin | Net |
|---|---|---|---|---|
| 5V | +5V | | GP8 | JOY_SW |
| GND | GND | | GP9/GP10/GP11 | ENC_A/B/SW |
| 3V3 | RP_3V3 (out) | | GP26/GP27 | JOY_X/JOY_Y (ADC) |
| GP0 | RP_TX → A7S RX | | GP12–GP15 | NC (spare, future I/O) |
| GP1 | RP_RX ← A7S TX | | GP28/GP29 | NC (spare ADC) |
| GP2–GP5 | BTN1–BTN4 | | | |
| GP6/GP7 | BTN5/BTN6 | | | **No radio nets on the RP2040.** |

---

## 7. Design rules baked in
- **TFT write-only**: J3.9 (SDO) NC → only one driver per MISO; radios + XPT2046 tri-state.
- **SPI1 ≤ ~8 MHz** when radios populated (multi-chip MISO integrity).
- **UART cross-over** + 100 Ω series (R3/R4); optional 0 Ω/solder-jumper in series to lift RP_TX for
  independent RP2040 USB flashing.
- **Radio 3V3 is load-switched** (U2) + 470 µF (C2) → clean power-cycle, no nRF24+PA+LNA brownout.
- **+3V3_SBC unloaded** — all peripheral 3V3 from U1/U2, not the A7S rail.
- Buttons/encoder use **RP2040 internal pull-ups**; joystick pot ref = RP_3V3.

---

## 8. To KiCad
`a7s_backplane_skidl.py` encodes this netlist. Generate the KiCad netlist with:
```
nix-shell -p 'python3.withPackages(p:[p.skidl])' kicad
python3 a7s_backplane_skidl.py        # -> a7s_backplane.net
```
Then: new KiCad project → import netlist → assign/confirm footprints → place (using the STEP-measured
header origins for J1/J2) → route. Symbol/footprint lib refs in the script are standard KiCad 8 names;
validate on first run.
