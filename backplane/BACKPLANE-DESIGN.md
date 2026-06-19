# A7S Cyberdeck Backplane (Shield) — Design + BOM

**Target:** Radxa Cubie A7S (Allwinner A733, `sun60iw2p1`). The backplane is a **shield** that
plugs onto the A7S **30-pin (2×15)** and **15-pin (1×15)** GPIO headers and forms the front face of
the deck.

**Pinout source of truth:** `recon/BRINGUP.md` + `recon/BSP-DTS-MAP.md` (BSP DTS
`device-a733-v1.4.8`, Product Brief Rev 1.3, schematic v1.10). All GPIO is **3.3 V logic
(3.63 V max)**. Board = 50.8 × 50.8 mm.

**Radio socket = the "8+1" standard** finalized in `~/Research/radio/05-socket-standard-8plus1.md`
(docs 01–06). This doc maps that standard + the deck mechanics onto A7S pins.

**Decisions locked:**
- Deliverable = design doc + BOM (KiCad after sign-off).
- TFT = 2.8" ILI9341 SPI + **resistive XPT2046 touch** (shares SPI1); sits on the **front face**.
- Input MCU = **RP2040-Zero** (5 V pin, onboard 3V3 reg, ADC). **Inputs ONLY** — buttons, joystick,
  encoder. It is the interface-dev MCU and is **kept entirely off the radio path** (no radio bridging,
  no radio ID). Spare RP2040 GPIO is reserved for future interface work.
- Joystick = **analog thumbstick** (2× RP2040 ADC + push).
- Power = **external battery → A7S USB-C1 (power port)**. Shield taps 5 V from the 30-pin header
  (pins 2/4). **No power connector, charger, or reverse-protection on the shield.**
- Radio = **TWO 8+1 sockets** (2×4 nRF24-order core + AUX/ID pin 9 each) on shared SPI1.
  **All radio control + AUX lines map to A7S header pins** (the 45-pin budget covers it).
  **ESP-01 / UART radios → casing-mounted mini-breadboards** via a backside breakout (doc-06).
- **Mechanics (see §9):** front = TFT + 4 buttons along the bottom edge under the screen. Radio
  sockets + breakout = **backside, overhanging the edge opposite the USB-C/Ethernet ports**.
  Joystick + 2 extra buttons + rotary encoder = **off-board, solder-wired** to shield pads.

---

## 1. Block diagram

```
              external USB-C battery / power bank (5V, >=3.5A)
                              |  USB-C
                       +------v-----------------------------+
                       |  A7S USB-C1 (power+OTG, USB2)       |
                       |  5V rail ---> 30-pin pin2/pin4 -----+---> SHIELD 5V net
                       |  SPI1 PD10-14  UART2 PB0/PB1        |       | (1A polyfuse + bulk cap)
                       |  UART3 PJ22/PJ23  TWI2 PD16/PD17    |       |
                       |  GPIO PB2 PB3 PB4 PB6 PB7 PB8       |       |
                       |       PJ24 PJ25 PM3 PM4 PG0-PG5     |       |
                       +-------------------------------------+       |
                          ^   ^   ^   ^                  +----------+----------+
        30-pin + 15-pin female sockets (shield back)     |          |          |
                          |   |   |                   RP2040-Zero  3V3 LDO   TFT VCC=5V
   SPI1 (SCK/MOSI/MISO) --+   |   |                   5V          (AP2112K)
        |       |       |     |   |                     |            |
   TFT_CS   TOUCH_CS  RADIO1_CS(PJ24) RADIO2_CS(PB7)  4 btn      3V3_SW (load sw, PB4)
   (PD10)   (PM3)     RADIO1 FLEX PB3/PJ25            (front)      |  -> both radio sockets
   TFT_DC   TOUCH_IRQ RADIO2 FLEX PB8/PG0          off-board:      |  -> UART breakout 3V3
   (PD14)   (PM4)     pin9 AUX -> PG1 / PG2 (A7S)   joy(2ADC+SW)
   TFT_RST(PB2) TFT_BL(PB6,PWM)                     2 btn, encoder (solder pads)
   UART2(PB0/PB1) <==> RP2040-Zero (input events only)
   UART3(PJ22/PJ23)+I2C+spare PG1-5 ==> BACKSIDE BREAKOUT -> casing mini-breadboards
```

---

## 2. Bus / resource allocation (A7S side)

| Resource | A7S pins | Used for |
|---|---|---|
| **SPI1** (only header SPI) | PD11 CLK, PD12 MOSI, PD13 MISO | Shared bus: TFT + touch + **both** radios |
| SPI1 CS0 (hw) | PD10 | TFT_CS |
| GPIO CS | PM3 | TOUCH_CS (XPT2046) |
| GPIO CS | PJ24 | **RADIO1_CS** (socket pin 4) |
| GPIO CS | PB7 | **RADIO2_CS** (socket pin 4) |
| GPIO flex | PB3 / PJ25 | **RADIO1 FLEX_A / FLEX_B** (pins 3 / 8) |
| GPIO flex | PB8 / PG0 | **RADIO2 FLEX_A / FLEX_B** (pins 3 / 8) |
| GPIO aux | PG1 / PG2 | **RADIO1 / RADIO2 AUX** (socket pin 9 — DIO1/GDO/2nd-INT) |
| GPIO out | PB4 | **3V3_SW enable** (shared radio load switch) |
| **UART2** | PB0 TX, PB1 RX | RP2040-Zero link (input events only) |
| **UART3** | PJ22 TX, PJ23 RX | backside breakout (ESP-01 etc.) |
| **TWI2 (I2C)** | PD16 SCK, PD17 SDA | breakout + radio ID-EEPROM bus |
| GPIO | PD14 / PB2 | TFT_DC / TFT_RST |
| PWM0 | PB6 | TFT backlight |
| GPIO in | PM4 | TOUCH_IRQ |
| spare | PG3–PG5 | breakout to casing breadboards |
| UART0 | PB9/PB10 | RESERVED debug console — test pads only |

> **Radios are 100% on A7S header pins; the RP2040 touches no radio signal.** Each socket's **pin-9
> AUX** is a plain A7S GPIO (PG1/PG2) usable as a 2nd interrupt (CC1101 GDO / LoRa DIO1). The A7S has
> no header ADC, so module **detection = SPI register probe** (nRF24 CONFIG; CC1101/CC2500
> PARTNUM/VERSION 0x30/0x31) for bare modules, or an **I²C ID-EEPROM on TWI2** for carriers — not an
> analog ID resistor. Only **PD13 (MISO)** is shared-read → TFT is **write-only** (SDO NC); radios +
> XPT2046 tri-state MISO when deselected.

---

## 3. A7S header pin map

### 30-pin header (2×15)
| Pin | SoC | Net | | Pin | SoC | Net |
|--:|---|---|---|--:|---|---|
| 1 | 3V3 | 3V3_SBC (light) | | 2 | 5V | **5V_IN** tap |
| 3 | PJ23 | UART3_RX → breakout | | 4 | 5V | **5V_IN** tap |
| 5 | PJ22 | UART3_TX → breakout | | 6 | GND | GND |
| 7 | PB0 | RP2040_RX ← (UART2-TX) | | 8 | PB9 | console (testpad) |
| 9 | GND | GND | | 10 | PB10 | console (testpad) |
| 11 | PB1 | RP2040_TX → (UART2-RX) | | 12 | — | NC |
| 13 | — | NC | | 14 | GND | GND |
| 15 | — | NC | | 16 | PJ24 | RADIO1_CS |
| 17 | 3V3 | 3V3_SBC (light) | | 18 | PJ25 | RADIO1 FLEX_B |
| 19 | PD12 | SPI1_MOSI | | 20 | GND | GND |
| 21 | PD13 | SPI1_MISO | | 22 | — | NC |
| 23 | PD11 | SPI1_CLK | | 24 | PD10 | TFT_CS |
| 25 | GND | GND | | 26 | PD14 | TFT_DC |
| 27 | PD17 | I2C_SDA | | 28 | PD16 | I2C_SCK |
| 29 | PB2 | TFT_RST | | 30 | GND | GND |

> Pins 12/13/15/22 not enumerated in recon → **NC** until verified vs schematic v1.10.

### 15-pin header (1×15) — GND only, no power rails
| Pin | SoC | Net |
|--:|---|---|
| 1 | PB3 | RADIO1 FLEX_A |
| 2 | PM3 | TOUCH_CS |
| 3 | PM4 | TOUCH_IRQ |
| 4 | GND | GND |
| 5 | PB6 | TFT_BL (PWM0) |
| 6 | PB4 | 3V3_SW enable |
| 7 | PB8 | RADIO2 FLEX_A |
| 8 | PB7 | RADIO2_CS |
| 9 | GND | GND |
| 10 | PG0 | RADIO2 FLEX_B |
| 11 | PG1 | RADIO1 AUX (socket pin 9) |
| 12 | PG2 | RADIO2 AUX (socket pin 9) |
| 13–15 | PG3–PG5 | spare → backside breakout |

---

## 4. Connectors

### 4.1 TFT — 2.8" ILI9341 + XPT2046 (14-pin, "TJCTM24028-SPI" order)
VCC=5V (module has 3V3 reg + level shifter); CS/RESET/DC = PD10/PB2/PD14; SDI/SCK = PD12/PD11;
LED = PB6 (PWM0); **SDO = NC** (write-only); T_CLK/T_DIN/T_DO = PD11/PD12/PD13; T_CS/T_IRQ = PM3/PM4.

### 4.2 RP2040-Zero (soldered) — all input I/O
| RP2040-Zero | Net | Where |
|---|---|---|
| 5V / GND | 5V / GND | from pins 2/4 |
| GP0 / GP1 | TX / RX ↔ A7S UART2 | cross over, 100 Ω series |
| GP2..GP5 | **BTN1..BTN4** | **on shield, front bottom edge** |
| GP6 / GP7 | BTN5 / BTN6 | **off-board solder pads** |
| GP26 / GP27 | JOY_X / JOY_Y (ADC) | off-board solder pads |
| GP8 | JOY_SW | off-board |
| GP9 / GP10 / GP11 | ENC_A / ENC_B / ENC_SW | off-board solder pads |
| GP12-15 / GP28 / GP29 | **spare** | reserved for future interface dev (no radio) |
| 3V3 (out) | local | pot Vcc, button/encoder pull-ups |

### 4.3 Radio — TWO 8+1 sockets (J-RADIO1, J-RADIO2), backside
Each = a **2×4 receptacle in exact nRF24L01+ order** + an offset **pin 9 AUX/ID** (a bare module
never reaches pin 9):

```
 pin1 GND     | pin2 +3V3_SW       pin3 FLEX_A | pin4 CS
 pin5 SCK     | pin6 MOSI          pin7 MISO   | pin8 FLEX_B
              pin9 AUX/ID (offset)
```

| Socket | Role | RADIO1 net | RADIO2 net | nRF24 | CC1101/CC2500 | RFM/LoRa |
|--:|---|---|---|---|---|---|
| 1 | GND | GND | GND | GND | GND | GND |
| 2 | +3V3 (switched) | 3V3_SW | 3V3_SW | VCC | VCC | VCC |
| 3 | FLEX_A | PB3 | PB8 | CE | GDO0 | RESET |
| 4 | CS/NSS | PJ24 | PB7 | CSN | CSN | NSS |
| 5 | SCK | PD11 | PD11 | SCK | SCK | SCK |
| 6 | MOSI | PD12 | PD12 | MOSI | MOSI | MOSI |
| 7 | MISO | PD13 | PD13 | MISO | MISO(=GDO1) | MISO |
| 8 | FLEX_B | PJ25 | PG0 | IRQ | GDO2 | DIO0 |
| 9 | AUX/ID | PG1 | PG2 | — | — | DIO1/ID |

- Pins 4–7 hard-universal SPI; pins 3 & 8 flex per module (software). **Drop-in: nRF24 family +
  CC1101 + CC2500.** Both sockets share SPI1; each has its own CS + flex + ID.
- **Both radios can be populated and active at once** (per-chip CS on the shared bus).
- CC1101 GDO order is vendor-specific — read silkscreen, set FLEX_A/B in software.
- Linux: two `spi1` children (`reg=2`, `reg=3`), `cs-gpios = <PJ24>, <PB7>`; flex (PB3/PJ25, PB8/PG0)
  and AUX (PG1/PG2) as gpio/irq — all on the A7S, none on the RP2040.

### 4.4 Module detect + A7S deviations
Bare modules → **SPI register probe** (nRF24 CONFIG/STATUS; CC1101/CC2500 PARTNUM/VERSION 0x30/0x31).
Carriers/harnesses → **I²C ID-EEPROM on TWI2** (the A7S can read I²C; it cannot read an analog ID
resistor — no header ADC). Pin 9 itself is a digital AUX/2nd-interrupt (PG1/PG2).

> **A7S deviations from the 8+1 host contract** (both forced): (1) no header ADC → pin-9 ID uses an
> I²C EEPROM (or SPI probe), **not** an analog resistor, and **never** the RP2040; (2) no socket
> SPI↔UART mux (SPI1 SCK is TFT-shared) → UART radios use the backside breakout + casing breadboard,
> not the socket. SPI radio plug-and-play is fully preserved, entirely on A7S pins.

### 4.5 Backside breakout → casing mini-breadboards (J-BRK)
The shield has **no room for a breadboard** (front is the TFT). The breadboards mount in the **casing**;
the shield exposes a backside breakout that wires to them:

| J-BRK pin | Net | For |
|---|---|---|
| UART3_TX / UART3_RX | PJ22 / PJ23 | ESP-01 / HC-12 / HC-05 (doc-06 recipe) |
| I2C_SDA / I2C_SCK | PD17 / PD16 | I2C sensors / QWIIC / ID-EEPROM |
| +3V3_SW / +5V | LDO / 5V_IN | module power (3V3 ≥500 mA for ESP bursts) |
| GND ×2 | GND | — |
| PG3..PG5 | spare GPIO | straps (CH_PD/RST/GPIO0/GPIO2) / general I/O |

> Only **one spare hardware UART (UART3)** reaches the breakout (UART0=console, UART2=RP2040,
> UART4 pins=RADIO1). A 2nd simultaneous UART radio = a **USB-serial dongle** on an A7S USB port — the
> RP2040 is **not** used to bridge it. ESP-01: 470 µF + 100 nF at the module, CH_PD/GPIO2/RST high,
> GPIO0 low=flash; **never 5 V to ESP.**

### 4.6 Off-board input solder field (J-IN) — beginner-friendly edge holes
The RP2040-Zero is **soldered to the shield**; its input GPIOs are **routed out to a row of plated
through-holes along a shield edge** so the casing-mounted controls solder to **big, clearly-labeled
edge holes** — not to the RP2040's tiny castellations. This is the recommended wiring path (soldering
straight to the RP2040 pads is possible but cramped and error-prone).

Beginner-friendly hole spec: **Ø1.0–1.2 mm hole / Ø2.2–2.5 mm annular ring**, 2.54 mm pitch, on the
**board edge** (iron + wire reach it from the side), each hole silkscreen-labeled and boxed per device:

| Group | Holes (→ RP2040) |
|---|---|
| **JOY** | 3V3 · GND · X→GP26 · Y→GP27 · SW→GP8 |
| **ENC** (EC11) | A→GP9 · B→GP10 · SW→GP11 · GND (+3V3 if module needs it) |
| **BTN5 / BTN6** | GP6 · GP7 · shared GND |

A single set of each — the casing mounts the off-board joystick/encoder/buttons on the chosen side and
wires here; handedness is handled by **rotating the whole deck 180°** (see §9), not duplicate pads.
Place J-IN centered on the bottom strip so wires reach a left- or right-mounted joystick.

Optional strain-relief: a couple of unconnected lacing holes by the field for zip-ties. (Wish-item.)

### 4.7 Flipper-accessory compatibility (mapping only, §4.8 doc-04)
Our SPI/UART/I2C/3V3/5V/GND nets map 1:1 to the Flipper Zero GPIO convention so Flipper-ecosystem
module wiring translates directly. No Flipper connector or bus-isolation on the shield.

---

## 5. Power tree + budget

```
ext battery (USB-C 5V >=3.5A) -> A7S USB-C1 -> board 5V -> 30pin pins2/4
   -> [F1 1A polyfuse] -> SHIELD 5V (+ 470uF + 0.1uF)
        |-> RP2040-Zero 5V         (~50 mA)
        |-> TFT VCC 5V             (~120-150 mA w/ backlight)
        |-> AP2112K-3.3 LDO -> 3V3_LDO
              |-> load switch (PB4) -> 3V3_SW -> both radio sockets + breakout 3V3
        (XPT2046 from TFT module 3V3)
```

| Rail | Worst-case | Notes |
|---|---|---|
| A7S (USB-C1) | up to 3 A | NPU/PCIe/USB peak; deck-typical 1–2 A |
| Shield 5V (pins 2/4) | ~0.45 A | RP2040 + TFT + LDO |
| 3V3_SW | ~0.5 A peak | ESP-01 burst / nRF24+PA+LNA (~250 mA) |
| **Battery total** | **~3.5 A peak** | power bank **≥5V/3.5A** (PD ideal) |

- No charger/protection on the shield — USB-C1 handles entry; shield only taps the protected 5V.
- F1 1 A polyfuse on the 5V tap. U1 = AP2112K-3.3 (600 mA; 1 A AP7361C if ESP run hard).
- U2 = load switch (TPS22918/AP22802, PB4-gated) → cold-boot a wedged radio. Shared by both sockets
  (per-socket switching = trivial upgrade using PG1).
- Don't power radios from `3V3_SBC` (header pin 1/17) — limited SBC output.

---

## 6. Software / device-tree (BSP Linux 5.15)
- `spi1` enabled; children `cs-gpios = <PD10>,<PM3>,<PJ24>,<PB7>`: ili9341(`fbtft`) reg0 (DC=PD14,
  RST=PB2, BL=PWM0); ads7846 reg1 (IRQ=PM4); radio1 reg2 (FLEX PB3/PJ25); radio2 reg3 (FLEX PB8/PG0).
- `uart2` (PB0/PB1) RP2040; `uart3` (PJ22/PJ23) breakout; `twi2` (PD16/PD17) I2C; `pwm0` (PB6)
  backlight; `PB4` gpio load-switch. Keep SPI1 ≤ ~8 MHz with radios populated (doc 05).
- Confirm `fbtft`/`ads7846` in `bsp_defconfig`; verify pinmux (`gpioinfo`) before powering peripherals.

---

## 7. BOM

See the maintained parts lists (sourcing links, no prices):

- **[BOM-SHIELD.md](./BOM-SHIELD.md)** — parts on the backplane PCB (generated from the netlist, all-THT).
- **[BOM-DECK.md](./BOM-DECK.md)** — the full deck system (A7S, power, radio modules, off-board inputs, chassis).

---

## 9. Mechanical / physical layout

The shield is **larger than the 50.8 mm A7S** so the 2.8" TFT and a button row fit. It stacks on the
A7S via the two female header rows (on the **back** face).

**A7S mechanical (from STEP v1.10 `refs/` + drawing):** board **50.8 × 50.8 mm**. Board frame in the
STEP origin: **X ∈ [−23.31, +27.49], Y ∈ [−29.68, −80.48] mm.** **4× Ø2.7 mm mounting holes** (4.5 mm
pad) on a **43.8 × 43.8 mm square** at **(−19.81, −33.18), (+23.99, −33.18), (−19.81, −76.98),
(+23.99, −76.98)**. The shield **replicates this exact hole pattern** (4× corner, **M2.5** standoffs).

**Orientation = LANDSCAPE.** The A7S is held with the GPIO headers top/bottom and the ports on the right:
| Connector | Edge | Evidence |
|---|---|---|
| **30-pin (2×15) header** | **TOP** (Y≈−30) | user; STEP frame (1×15 is the opposite/bottom edge) |
| **15-pin (1×15) header** | **BOTTOM** (Y≈−79) | user; STEP 1×15 @ (2.08, −78.71) |
| USB-C ×2 + USB-A + RJ45 | **RIGHT** (X≈+27) | user "all ports right edge"; photos; STEP USB-A @ +22.9 |
| Camera 31P FPC | **LEFT** (X≈−23) | STEP @ (−21.96, −49.08) |

The shield **mounts on BOTH headers** (female rows top + bottom), runs **landscape**, **hangs LEFT**
(ports clear on the right), and has a control **overhang strip on BOTH the top and bottom edges** so the
4-button row can be under the screen in either handedness (see ambidextrous note). Right edge aligns to
the A7S right edge → ports exposed.

```
                 FRONT (user-facing), landscape                  RIGHT EDGE of A7S
   +=========================================================+   (stays exposed):
   | (TOP overhang strip — footprints, populated if L-hand)  |     USB-C  USB-C
   |  [J-RAD]   [b1][b2][b3][b4]   [J-RAD]   [J-IN]/[J-BRK]   |     USB-A
   +---------------------------------------------------------+     RJ45
   |  [ 30-pin 2x15 female socket — top mount ]   |  A7S      |
   |        2.8" TFT (ILI9341 + touch) LANDSCAPE  |  footprint|
   |  [ 15-pin 1x15 female socket — bottom mount ]|  (right-  |
   +---------------------------------------------------------+ aligned)
   | (BOTTOM overhang strip — populated if R-hand)           |
   |  [J-RADIO1] [B1][B2][B3][B4] [J-RADIO2] [J-IN]/[J-BRK]   |
   +=========================================================+
       <-- shield overhangs LEFT past the A7S left edge -->
   RP2040 (soldered) + LDO + load sw + caps live on the BACK behind the TFT (central).
```

- **Front:** landscape TFT over the A7S footprint; **4 buttons centered under the screen** on the
  *active* control strip; the **2 radio sockets flank them**; J-BRK + J-IN edge holes on the same strip.
- **Back:** female sockets top (30-pin) + bottom (15-pin) mate the A7S; **RP2040 (soldered) + power stay
  central** behind the TFT (they rotate with the deck — no need to move them).
- **Off-board (casing):** joystick, 2 extra buttons (B5/B6), encoder, 2 mini-breadboards → wire to
  **J-IN** edge holes (→ RP2040) and **J-BRK**.
- **Clearance:** shield right edge by the A7S right edge → USB-C/USB-A/RJ45 exposed; keep the radios
  within the overhang (not past the right edge into the ports). Left overhang clears the camera FPC.

### Ambidextrous setup — duplicated top/bottom strips + 180° deck rotation
A 180° rotation swaps left↔right **and** top↔bottom, so under-screen buttons would land *over* the screen.
Fix: the control strip (4 buttons + 2 radios + J-IN + J-BRK) has **footprints on BOTH the top and bottom
overhangs**, wired to the same nets. Build-time handedness:

| Build | Populate strip | Deck | Display | Result |
|---|---|---|---|---|
| **Right-handed** | BOTTOM | normal (ports right) | normal | buttons under screen |
| **Left-handed** | TOP | rotate deck 180° (ports left) | `rotate=180` | TOP strip is now at the bottom → buttons under screen |

- **One PCB**; you solder the 4 buttons + 2 radios + connectors onto the strip that ends up **at the
  bottom** for the chosen hand; the other strip's footprints stay unpopulated. This is the "holes are
  there for both, just flip the arrangement" path.
- **RP2040 + power stay central** — unaffected by which strip is populated.
- Software: display `rotate=180`, invert touch X/Y, remap button order in RP2040 firmware for L-hand.
- Mounting holes symmetric + **15-pin header board-centered (X≈2.09)** → mounts identically either way.
- Cost: a **top overhang** (board grows ~10–12 mm taller) + duplicate (unpopulated) footprints — cheap.

### Silkscreen requirements (per user)
Every off-board solder pad is **silkscreen-labeled with its signal + grouped/boxed per component**, so
wiring is obvious at the bench without this doc:
- **J-IN** boxed per device, centered on the bottom strip: `JOY: 3V3·GND·X·Y·SW` | `ENC: A·B·SW·GND`
  | `BTN5 · BTN6 · GND`. (Handedness = 180° deck rotation, not duplicate pads — see §9.)
- Pin-1 marker + net labels on J-RADIO1/2, J-BRK, TFT socket, power tap, I²C.
- Reference + value silk on all THT parts; polarity/orientation marks for RP2040, LDO, load switch,
  electrolytics, and the radio sockets (square pad = socket pin 1).

### Resolved from STEP v1.10 / photos
- Board frame + mounting-hole coords — **locked**. Orientation = **landscape**; **30-pin top / 15-pin
  bottom / ports right / FPC left**; shield hangs **left**, radios flank the buttons on the bottom strip.

### Still to measure (for KiCad placement)
- **Both header origins (30-pin TOP + 15-pin BOTTOM) exact XY** — STEP named only the 1×15 (@ 2.08,
  −78.71). Measure both in FreeCAD/KiCad STEP-import (or from the A7S PCB/DXF) before placing the
  female sockets — they set the whole shield datum.
- Top-side **component heights** under the shield → stacking-header length (8.5 mm vs 11–14 mm tall) to
  clear the SoC/RAM/shields. Right-edge **port body depths** → confirm shield right edge doesn't foul them.
- Confirm header **gender** (assumed male → shield uses female).

---

## 10. Risks / verify-on-hardware
1. Unmapped 30-pin pins 12/13/15/22 → NC; confirm vs schematic v1.10.
2. No A7S header ADC → radio pin-9 ID = I²C EEPROM (TWI2) or SPI register probe, never the RP2040.
3. In-socket UART omitted (SPI1 SCK is TFT-shared) → UART radios on the casing breadboard.
4. SPI MISO: TFT write-only; keep SPI1 ≤ ~8 MHz with radios populated (multi-chip MISO integrity).
5. CC1101 GDO order vendor-specific → set FLEX_A/B in software per silkscreen.
6. nRF24+PA+LNA brownouts → 470 µF on radio 3V3; load switch enables clean power-cycle.
7. Only one spare UART (UART3) — second UART radio = USB-serial dongle (RP2040 stays inputs-only).
8. Board size + mounting holes locked (50.8 mm, 4× Ø2.7 on 43.8 mm sq). Still pending from STEP/3D:
   port edges, header XY offset, top-side heights (stack length), header gender.
9. Encoder = off-board solder-connect (**confirmed**).
```
```
