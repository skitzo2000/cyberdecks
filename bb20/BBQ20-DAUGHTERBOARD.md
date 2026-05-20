# BBQ20 → USB QMK Daughterboard Design Notes

Source-of-truth references for building your own RP2040 carrier for a raw BlackBerry Q20-class keyboard module (the same physical part used by Solder Party's BBQ20KBD, the Beepy, and most BB-keyboard cyberdeck builds).

All schematic facts below were extracted directly from Solder Party's open-hardware repo (`solderparty/bbq20kbd_hw`, CERN-OHL v1.2) and their `i2c_puppet` reference firmware. Treat the Solder Party board as the de facto reference design — if you build a "smaller / re-laid-out / different MCU" variant, you're essentially re-spinning their PCB with a different placement.

---

## 1. What the "BBQ20 module" actually is

- A **34-pin FFC tail** carrying a 7-row × 7-column membrane matrix, an integrated optical trackpad (I²C, 1.8 V logic), white LED backlight, and an analog microphone.
- The "Q20" name is Solder Party marketing. Physically, sellers list it as a **BlackBerry Classic (SQC100) keyboard replacement** or, depending on the vendor, "BB Q10 + trackpad" — the module is the keyboard out of the BlackBerry Classic phone.
- Counterfeits abound on AliExpress, and many bare Q10 modules **don't include the trackpad subsystem** even though the FFC tail has the trackpad pins. Always confirm with the seller that the module is the Classic-spec part with optical sensor populated. (The Q10-only version is a useful fallback — see §7.)

---

## 2. 34-pin FFC pinout (from `keyboard.kicad_sch`)

Connector on the host PCB must be **34-pin, 0.5 mm pitch FFC/FPC, bottom-contact** (the BB tail has contacts on the top face). Hirose FH12-34S-0.5SH or Molex 502078-3470 are the usual choices.

| Pin | Net          | Direction      | Voltage / Notes                                                |
| --: | ------------ | -------------- | -------------------------------------------------------------- |
|  1  | GND          | —              | digital ground                                                  |
|  2  | TP_SHUTDOWN  | MCU → module   | **1.8 V logic**, active-low trackpad shutdown                  |
|  3  | TP_SCL       | MCU → module   | **1.8 V logic**, I²C clock to trackpad sensor                  |
|  4  | TP_MOTION    | module → MCU   | **1.8 V logic**, active-low motion interrupt (falling edge)    |
|  5  | TP_SDA       | bidir          | **1.8 V logic**, I²C data to trackpad sensor                   |
|  6  | TP_RESET     | MCU → module   | **1.8 V logic**, active-low trackpad reset                     |
|  7  | NC           | —              | (no schematic connection; treat as reserved)                   |
|  8  | VDD_2V8      | rail in        | **2.8 V** core supply for trackpad sensor (≈ a few mA)         |
|  9  | NC           | —              | reserved                                                       |
| 10  | VDD_1V8      | rail in        | **1.8 V** I/O supply for trackpad logic                        |
| 11  | NC           | —              | reserved                                                       |
| 12  | COL1         | MCU bidir      | 3.3 V matrix col (strobe or sense, depending on scan polarity) |
| 13  | COL2         | MCU bidir      | 3.3 V matrix col                                               |
| 14  | COL3         | MCU bidir      | 3.3 V matrix col                                               |
| 15  | COL4         | MCU bidir      | 3.3 V matrix col                                               |
| 16  | COL5         | MCU bidir      | 3.3 V matrix col                                               |
| 17  | COL6         | MCU bidir      | 3.3 V matrix col                                               |
| 18  | COL7         | MCU bidir      | 3.3 V matrix col (carries 1 key — the right-2 side button)     |
| 19–21 | NC         | —              | reserved                                                       |
| 22  | AGND         | —              | analog ground for microphone                                   |
| 23  | MIC          | module → MCU   | analog audio out (≈ 0–VDD); route to ADC if you want voice     |
| 24  | MIC_VDD      | rail in        | mic bias; tie to 3.3 V via series-RC if used, leave NC if not  |
| 25  | NC           | —              | reserved                                                       |
| 26  | ROW7         | MCU bidir      | 3.3 V matrix row                                               |
| 27  | ROW6         | MCU bidir      | 3.3 V matrix row                                               |
| 28  | ROW5         | MCU bidir      | 3.3 V matrix row                                               |
| 29  | ROW4         | MCU bidir      | 3.3 V matrix row                                               |
| 30  | ROW3         | MCU bidir      | 3.3 V matrix row                                               |
| 31  | ROW2         | MCU bidir      | 3.3 V matrix row                                               |
| 32  | ROW1         | MCU bidir      | 3.3 V matrix row                                               |
| 33  | LEDK         | sink           | backlight LED cathode (sink to GND through an N-FET)           |
| 34  | LEDA         | rail in        | backlight LED anode (tie to 3.3 V)                             |

The keyboard scan is a **7-row × 7-col** matrix where one column (COL7) only has the single right-2 side button populated. Solder Party scan as 7×6 + 1 GPIO button in firmware, but you can equally treat it as 7×7 — both work.

The four side buttons live in the matrix: `KEY_BTN_LEFT1`, `KEY_BTN_LEFT2`, `KEY_BTN_RIGHT1` are on COL1 at various rows, and `KEY_BTN_RIGHT2` is the lone key on COL7.

---

## 3. RP2040 GPIO assignment (i2c_puppet reference)

From `boards/bbq20kbd_breakout.h`. Replicate or remap; nothing here demands specific RP2040 pins except USB D±:

| RP2040 GPIO | Function                                                              |
| ----------: | --------------------------------------------------------------------- |
| GP0         | INT out (asserts to external I²C host; skip if you're USB-only)       |
| GP1–GP7     | ROW1–ROW7 (drive low one at a time, read columns)                     |
| GP8, GP9, GP14, GP13, GP12, GP11 | COL1–COL6 (sense, with internal pull-ups)          |
| GP10        | COL7 / KEY_BTN_RIGHT2 (single-button column — treat as direct GPIO)   |
| GP15, GP17, GP19, GP21, GP26 | GPIO-expander pins on the PMOD side (optional)         |
| GP16        | TP_RESET (3.3 V; level-shifted to 1.8 V before module)                |
| GP18        | TP_SDA  (3.3 V → 1.8 V)                                               |
| GP22        | TP_MOTION (1.8 V → 3.3 V via shifter)                                 |
| GP23        | TP_SCL  (3.3 V → 1.8 V)                                               |
| GP24        | TP_SHUTDOWN (3.3 V → 1.8 V)                                           |
| GP25        | BKL (PWM → N-FET gate, drives LEDK)                                   |
| GP27 / ADC1 | MIC (optional analog mic)                                             |
| GP28, GP29  | I²C-slave puppet bus (Stemma QT / Qwiic) — drop if USB-only           |
| GP20        | debug UART TX (optional)                                              |

For USB-HID-only QMK builds you can free GP0, GP15, GP17, GP19, GP21, GP26, GP28, GP29 and use whatever's convenient on your layout.

---

## 4. Trackpad subsystem

The optical finger-navigation sensor is **on the BB module itself** — you do **not** place it on your carrier. Your job is just to feed it the right rails and talk I²C to it.

- I²C address: **0x3B**
- Register map (used by `app/touchpad.c`):
  - 0x00 = PID, 0x01 = REV, 0x02 = MOTION (bit7 MOT, bit4 OVF),
    0x03 = DELTA_X, 0x04 = DELTA_Y, 0x05 = DELTA_XY_H,
    0x11 = CONFIG (bit7 HiRes), 0x2E = OBSERV, 0x42 = MBURST
- Motion line is active-low, edge-triggered; firmware reads MOTION → DELTA_X → DELTA_Y on each interrupt.
- Sensor wants ~5 ms after RESET-deassert before responding.

The register signature is consistent with a PixArt PAT9125-class optical finger nav IC (8-bit deltas, MOT/OVF bits exactly there). You don't need to know the exact die — talk to it as a black box at 0x3B.

---

## 5. Daughterboard BOM (minimum viable, USB-HID only)

Quantities/values are taken from the Solder Party reference. Reference designators match the schematic so you can cross-check.

### Connectors & MCU
| Ref         | Part                                              | Notes                                      |
| ----------- | ------------------------------------------------- | ------------------------------------------ |
| **FFC1**    | Hirose FH12-34S-0.5SH (or eq. 34-pin 0.5 mm FPC, bottom contact) | mates the keyboard tail                |
| **J3**      | USB Type-C receptacle, USB 2.0 (16-pin, e.g. GCT USB4105-GF-A) | power + data                              |
| **U1**      | Raspberry Pi RP2040 (QFN-56)                      | XIP via external flash                     |
| **U2**      | AP2112K-3.3 LDO (SOT-23-5, ≥ 600 mA)              | VBUS 5 V → 3.3 V rail                     |
| **U3**      | GD25Q16xS (or W25Q16JV) — 16 Mbit QSPI flash      | RP2040 program storage                     |
| **Y1**      | 12.000 MHz crystal, ±30 ppm                       | RP2040 XIN/XOUT                            |
| **D1**      | Schottky, ≥ 1 A (e.g. SS14, MBR0530)              | VBUS reverse-isolation                     |

### Trackpad-side support (the "carrier" stuff)
| Ref         | Part                                              | Why                                        |
| ----------- | ------------------------------------------------- | ------------------------------------------ |
| **U5**      | ME6212C18M5G (1.8 V LDO, SOT-23-5)                | generates VDD_1V8 from 3.3 V               |
| **U6**      | ME6212C28M5G (2.8 V LDO, SOT-23-5)                | generates VDD_2V8 from 3.3 V               |
| **Q1–Q3, Q5, Q6** | 5 × BSS138 N-MOSFET (SOT-23)                | bidir level shifter on TP_SDA, TP_SCL, TP_MOTION, TP_RESET, TP_SHUTDOWN |
| **R8, R10, R12, R14, R17** | 5 × 10 kΩ 0402 (3.3 V side pull-ups) | shifter low side                          |
| **R9, R11, R13, R15, R18** | 5 × 10 kΩ 0402 (1.8 V side pull-ups) | shifter high side                         |
| **C14**     | 0.1 µF 0402 X7R                                   | 1.8 V LDO output bypass                    |
| **C15**     | 0.1 µF 0402 X7R                                   | 2.8 V LDO output bypass                    |

The five-MOSFET shifter is the standard NXP AN10441 bidirectional topology — same FET, two 10 k pull-ups per line, gate tied to the 1.8 V rail. Don't substitute a unidirectional IC like a 74LVC-something on TP_SDA — it has to be bidirectional.

### Backlight driver
| Ref       | Part                       | Notes                                                          |
| --------- | -------------------------- | -------------------------------------------------------------- |
| **Q4**    | BSS138 N-MOSFET (SOT-23)   | gate from RP2040 GP25, drain to LEDK (FFC pin 33)              |
| **R16**   | 10 kΩ 0402                 | gate pull-down (keeps backlight off at reset)                  |
| (LEDA)    | tie FFC pin 34 to +3.3 V   | anode of internal LED chain                                    |

No series resistor in the LED path — the keyboard module already has on-board current limiting. Solder Party drives the gate with hardware PWM on a PWM4B channel; QMK BACKLIGHT_PIN handles that.

### USB & power
| Ref         | Part                                            | Notes                                          |
| ----------- | ----------------------------------------------- | ---------------------------------------------- |
| **R1, R2**  | 2 × 5.1 kΩ 0402                                 | USB-C CC1/CC2 pull-downs (UFP advertising)     |
| **R5, R6**  | 2 × 27 Ω 0402                                   | USB D± series termination                       |
| **C1–C8, C14, C15** | 0.1 µF 0402 X7R per MCU rail/LDO        | decoupling                                      |
| **C9**      | 1 µF 0402/0603                                  | LDO input cap                                  |
| **C10, C11** | 2 × 10 µF 0805 X7R                             | bulk on 5 V and 3.3 V                           |
| **C12, C13** | 2 × 12 pF 0402 C0G                             | crystal load                                    |

### Boot / reset / programming
| Ref       | Part                       | Notes                                                          |
| --------- | -------------------------- | -------------------------------------------------------------- |
| **R3**    | 1 kΩ 0402                  | series on QSPI_CS to BOOTSEL test point                        |
| **R4**    | 10 kΩ 0402                 | pull-up on RUN                                                 |
| **R7**    | 10 kΩ 0402                 | flash CS pull-up                                               |
| **R22**   | 1 kΩ 0402                  | UART-TX series (optional debug)                                |
| **TP1**   | exposed pad / button       | BOOTSEL — short to GND while plugging USB to enter UF2 mode    |
| **TP2**   | exposed pad / button       | RESET (RUN to GND)                                             |
| **TP3, TP4** | SWCLK, SWDIO            | break out for ARM debugger if you want one                     |

### Optional but recommended
- USB ESD: Add a TPD2EUSB30 or eq. across D±/VBUS — the bare USB-C lines on a handheld are exposed.
- Reset button: a SKQG style side switch on RUN-to-GND is much nicer than shorting a TP.
- BOOTSEL button: same, on the QSPI_CS test point.
- Stemma QT / Qwiic JST-SH 4-pin (J1) and PMOD 2×6 header (J2) cost ~$0.40 in parts and let the same board be reused as an I²C peripheral for projects like Beepy or a Pi Zero deck.
- A tiny ferrite bead on VBUS in if you're putting this near a 2.4 GHz radio.

### Approximate cost @ qty 1 (US/EU 2026)
- BB Q20 module (AliExpress): **$3–$10**
- All small passives + LDOs + MOSFETs: **~$2**
- RP2040 + flash + crystal + LDO: **~$3–4**
- USB-C receptacle + ESD: **~$1.20**
- FFC connector: **~$1**
- 2-layer PCB (JLCPCB, 5×): **~$5 + shipping**

Total roughly **$15–22 in BOM** plus board cost, vs. **$44–55 for the assembled Solder Party board**.

---

## 6. Firmware path

You have three viable routes:

1. **Run `i2c_puppet` unchanged** if you stick to the Solder Party GPIO map. It already emits USB HID keyboard + mouse and exposes I²C-slave for embedded hosts. **Easiest. No QMK.** Just `cmake -DPICO_BOARD=bbq20kbd_breakout` and flash.
2. **QMK port** — exists already, see `solderparty/qmk_firmware` fork and `ZitaoTech/BBQ20-USB-keyboard`. The QMK port handles the matrix and the trackpad-as-pointing-device cleanly via `POINTING_DEVICE_ENABLE` + a custom driver that talks to the 0x3B sensor. Use this if you want VIA remapping, custom layers, RGB later, etc.
3. **KMK / CircuitPython** if you like Python. There's a CircuitPython BBQ10Keyboard library (`arturo182_CircuitPython_BBQ10Keyboard`) that targets the i2c_puppet bus, so this is really a "use i2c_puppet + Python host" combo.

Realistic recommendation: prototype with **i2c_puppet** (firmware already exists, ship in a weekend), then migrate to **QMK** once the hardware is verified — you'll thank yourself for the layer system on a 5-row keeb.

---

## 7. Sourcing notes

**Searching AliExpress / eBay** — the keyword that works best is `BlackBerry Classic Q20 keyboard` or `BB Classic SQC100 keyboard`. Avoid listings titled only "BB Q10 keyboard" unless the photo clearly shows the trackpad slot in the centre. Some sellers do photograph a Q10 module but ship a Q20 — and vice versa — confirm in chat.

**Lectronz / Tindie** — Solder Party and ZitaoTech both sell the **module + their carrier** as a finished product (Solder Party BBQ20KBD at $44–55, ZitaoTech BBQ20 USB at $50–70). If you don't care about owning the PCB design, the assembled boards are barely more than a hand-built BOM.

**Salvage** — a parted-out BlackBerry Classic (SQC100, 2014–2017) yields the keyboard module for ~$10–20 on eBay. Look for "BB Classic for parts." Avoid water-damaged units.

**Q10-only fallback** — if you only find a Q10 keyboard (no trackpad), the FFC has fewer functional signals but the same connector. You won't get the trackpad lines (TP_*, VDD_1V8, VDD_2V8 — leave NC). Combine with a separate trackpad sensor (BB9900 trackpad PCB on eBay is the community pick, see `ZitaoTech/BBQ10-USB_BLE_Keyboard`) or just ship without a pointing device.

**Counterfeit risk** — the cheap $3 keyboards on AliExpress sometimes have flaky membrane domes that quit after 50 k presses. If you're building more than one unit, factor in ~20% spare yield.

---

## 8. Critical pitfalls

- **Do not drive any TP_* pin from a 3.3 V GPIO without level-shifting.** The trackpad sensor will latch up. The five-MOSFET shifter is mandatory.
- **LDO sequencing**: bring VDD_1V8 up before or with VDD_2V8 — both are derived from 3.3 V so this happens automatically if you tie both LDO `EN` pins to 3.3 V. Don't gate one of them off the MCU unless you also pulse TP_RESET afterwards.
- **FFC contact orientation**: the BB module tail has contacts on the **top** face. A "top-contact" FFC connector on your PCB will not mate — you need a **bottom-contact** part. Hirose FH12 in `…S-0.5SH` suffix = bottom-contact; FH12 in `…T-0.5SH` = top-contact. Order the wrong one and the keys read open.
- **Pin 1 location** on the FFC connector varies by vendor. Confirm with a multimeter before energizing — pin 1 of the keyboard is the GND pad nearest the corner stiffener.
- **Backlight gate direction**: BSS138 is N-channel low-side. If you accidentally wire it as high-side (gate from MCU, source to LEDK) the backlight flashes once and dies — Q4's body diode reverse-biases LED string.
- **USB-C without CC pull-downs** (R1, R2) just won't enumerate when plugged into a Type-C charger or computer. This is the #1 first-spin failure on hand-rolled USB-C boards.

---

## 9. Open-source references

- Solder Party hardware: [solderparty/bbq20kbd_hw](https://github.com/solderparty/bbq20kbd_hw) — schematic.pdf, KiCad files, iBOM, CERN-OHL v1.2 (you can re-spin and sell).
- Solder Party firmware: [solderparty/i2c_puppet](https://github.com/solderparty/i2c_puppet) — pin map in `boards/bbq20kbd_breakout.h`, matrix in `app/keyboard.c`, trackpad in `app/touchpad.c`.
- ZitaoTech alternative: [ZitaoTech/BBQ20-USB-keyboard](https://github.com/ZitaoTech/BBQ20-USB-keyboard) — pared-down USB-only build, QMK-based, includes the 3D-printed case STL.
- QMK port: search "qmk bbq20" — typically lives as a fork.
- BB Q10-only PMOD precursor: [arturo182/BBQ10KBD](https://github.com/arturo182/BBQ10KBD) (older, 24-pin connector, no trackpad).
- BBKB community wiki: [bbkb-community.github.io](https://bbkb-community.github.io/) — list of every BB-keyboard cyberdeck/handheld in the wild.
- Reverse-engineering the BB Passport keyboard (different module, useful methodology): [tinlethax.wordpress.com](https://tinlethax.wordpress.com/2022/03/06/reverse-engineering-blackberry-passport-keyboard-part-1/).
