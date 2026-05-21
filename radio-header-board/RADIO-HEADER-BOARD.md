# Radio Header Board — Slim Pogo-Pin Cyberdeck Radio Infrastructure

A **two-piece** radio carrier system for cyberdecks:

1. **RHB-Pogo** — a thin (~4 mm including compressed pogo pins) adapter that snaps onto the BACK of the Raspberry Pi via spring-loaded contacts on the GPIO solder-pad footprint, exactly like the PiSugar 3. A PiSugar 3 (or other pogo-mounted accessory) snaps onto the bottom of OUR board in turn. Pi GPIO header on top is untouched — e-paper or any other HAT mounts normally at standard height.
2. **RHB-Carrier** — a 4-slot radio module hub that lives anywhere in the chassis (rear edge near antennas, side panel, top of case), connected to RHB-Pogo via a single thin FFC ribbon cable.

This document is the design source-of-truth. The board referenced as the "daughter-PCB" in [`../workshops/03-main-build.md`](../workshops/03-main-build.md) and [`../workshops/04-radio-applications.md`](../workshops/04-radio-applications.md) IS this system (the workshops were written assuming a single stacked board; reconciliation deferred — see §12).

## 1. Scope and design goals

| Goal | How met |
|---|---|
| Plug any cheap RF chip into a deck without a custom PCB per radio | RHB-Carrier has four physical module slots: CC1101 1×8 socket, HopeRF RFM95/69 16-pin SMD, nRF24L01+ 2×4, universal 1×9 spare header |
| Don't block the Pi GPIO header | Pogo-pin mount under the Pi — Pi's GPIO header stays mechanically free for any HAT above (e-paper, audio, sensor) at standard ~10 mm stack height |
| Stack a PiSugar at the bottom if needed | RHB-Pogo passes through all 40 GPIO positions with gold pads on its underside in the standard Pi-GPIO layout — the PiSugar's own pogo pins land on those pads as if they were the Pi PCB |
| Slim form factor in metal cyberdeck chassis | RHB-Pogo adds ~4 mm under the Pi (pogo compression + PCB); RHB-Carrier is 1.6 mm thick and lives in unused chassis space; total system thickness contribution lower than any stacking-header approach |
| One unambiguous power switch | Master 5 V slide switch on RHB-Carrier (SS-12F44, panel-mount, edge-poking) — gates the JST-PH input OR the FFC-supplied rail, whichever is feeding the carrier |
| Cheap enough to give away in a workshop kit | Target ≤$8 in parts at qty 10 (both boards + FFC) from JLCPCB |

Non-goals: no MCU on either board (no RP2040, no ESP32 co-pro), no OLED, no USB hub silicon. RHB-Pogo is a passive pin-router with 40 spring contacts and one FFC connector. RHB-Carrier has one LDO, one switch, four sockets, two USB-A receptacles, and four u.FL pads. That's it.

## 2. Mechanical

### 2.1 RHB-Pogo (the adapter under the Pi)

| Param | Value |
|---|---|
| Board outline | 55 × 30 mm — matches the GPIO-strip portion of the Pi Zero 2 W footprint; sits under all of Pi Zero 2 W or under the GPIO edge of Pi 4/5 |
| Thickness | 1.6 mm FR-4, ENIG finish (mandatory — for gold pads on underside) |
| Pogo pin array, TOP | 40 SMT spring-loaded contacts in standard 2.54 mm × 2.54 mm Pi GPIO pattern (2 rows × 20 columns). Uncompressed height ~3 mm; compressed ~1.5 mm under ~40 g/pin force |
| Passthrough pad array, BOTTOM | 40 gold-plated dimples on the underside, one per pogo pin, matching the same 2×20 GPIO layout. Each pogo pin's tail is connected to its counterpart bottom pad via a single short trace. A PiSugar 3 (or any pogo-pin device that pad-contacts the Pi GPIO) snaps to this layer and sees identical electrical geometry as if it were attached directly to the Pi |
| FFC connector | Hirose FH12-24S-0.5SH-G (or HRS FH-equivalent) — 24-pin, 0.5 mm pitch, bottom-contact FFC/FPC, SMT. Single row, latched. Carries the GPIO subset RHB-Carrier needs (17 GPIO lines + SPI bus + 5 V + 3 V3 + GND) |
| Mounting | 4× M2 holes at the standard Pi Zero 2 W standoff pattern (58 × 23 mm). Optional 4× neodymium press-fit magnets (5 mm × 2 mm thick, N52 grade) for tool-free snap mount to steel mounting hardware |
| Stack height under Pi | ~4 mm typical (1.6 mm PCB + 1.5 mm compressed pogo + ~1 mm clearance) |

```
RHB-Pogo, top view (the side facing Pi PCB):

           58 mm
   +------------------------------+
   | ⊙                          ⊙ |  ← M2 magnet/screw
   |                              |
   |  ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●  |  ← 40 pogo pins on 2.54mm pitch
   |  ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●  |
   |  pin 1 →                       ← pin 40   |
   |                              |
   |    [---FFC 24-pin---]        |  ← edge connector, ribbon goes RIGHT
   | ⊙                          ⊙ |
   +------------------------------+
                     30 mm

Bottom view (the side facing PiSugar):

   +------------------------------+
   |                              |
   |  ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  |  ← 40 gold dimples
   |  ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  |    (PiSugar pogo contact points)
   |                              |
   +------------------------------+
```

### 2.2 RHB-Carrier (the 4-slot radio hub)

| Param | Value |
|---|---|
| Board outline | 85 × 56 mm — Pi 4/5 footprint (lives in chassis interior, not mechanically tied to Pi) |
| Thickness | 1.6 mm FR-4, HASL is fine here |
| FFC connector | Same Hirose FH12-24S-0.5SH-G as RHB-Pogo — bottom-contact, 24-pin, 0.5 mm pitch |
| Module slots | (see §5) — 1×8 CC1101 socket, RFM95/69 16-pin SMD castellated landing, 2×4 nRF24L01+ socket, 1×9 universal spare header |
| Master power switch | SS-12F44 SPDT slide, right-angle, edge-mounted facing user |
| 3 V3 LDO | AP2112K-3.3, 600 mA, SOT-25 |
| Power input | JST-PH 2-pin, 5 V — for builds without PiSugar (use a stand-alone 18650 pack or USB-C power tap) |
| Power from pogo adapter | 5 V + 3 V3 + GND also delivered via the FFC, so if PiSugar is supplying power upstream, the carrier needs no separate JST-PH connection |
| USB-A passthrough | 2× through-hole vertical USB-A type, wired to a 4-pin JST-SH header that runs to Pi's USB host port |
| Antenna pads | 4× u.FL, one per slot |
| Mounting | 4× M2.5 holes in a 75 × 46 mm pattern (custom — chassis fastens to these, not the Pi) |
| Power LEDs | D2 green (5 V rail post-switch), D3 blue (3 V3 LDO output) |

```
RHB-Carrier, top view:

                            85 mm
   +-------------------------------------------------+
   |  ⊙  [FFC 24-pin]                          ⊙    |  ← FFC in from pogo adapter
   |     ▲                                            |
   |     │                                            |
   |  [PWR SW] [LEDs]                  [u.FL A]      |
   |                                   [u.FL B]      |
   |  +--SLOT A--+ +--SLOT B--+        [u.FL C]      |
   |  |  CC1101  | |  RFM95/  |        [u.FL D]      |
   |  |  1x8 skt | |  69 SMD  |   +--SLOT D--+       |
56 |  |          | |  16-pin  |   | nRF24L01+|       |
mm |  +----------+ +----------+   |  2x4 skt |       |
   |                              +----------+       |
   |  +--SLOT C: 1x9 universal spare header-+        |
   |  | 3V3 GND MOSI MISO SCK CS RST DIO0 1|        |
   |  +---------------------------------------+      |
   |                                                  |
   |  [JST-PH 5V] [JST-SH USB] [USB-A]  [USB-A]      |
   |  ⊙                                          ⊙   |
   +-------------------------------------------------+
                            85 mm
```

### 2.3 The FFC ribbon cable

| Param | Value |
|---|---|
| Type | 24-pin, 0.5 mm pitch, Type A (contacts on the SAME side both ends — flat path through) |
| Length | 100 mm default; 150 mm or 200 mm for chassis that need it |
| Source | Pre-built, AliExpress/LCSC ~$0.30 each in qty 10 |
| Pin map | Documented in §3.1 — the 24 lines that traverse the ribbon |

### 2.4 Total stack analysis

For a Pi Zero 2 W with e-paper HAT on top, RHB-Pogo underneath, PiSugar 3 below:

```
                                           Z position
e-paper HAT top surface                    +10.1 mm
   ├── e-paper HAT PCB (1.6 mm)            
   ├── Pi GPIO factory header (8.5 mm)
Pi PCB top                                    0 mm    ← reference plane
Pi PCB bottom                              –1.6 mm
RHB-Pogo pogo pin compressed (–1.5 mm)
RHB-Pogo top surface                       –3.1 mm
   ├── RHB-Pogo PCB (1.6 mm)
RHB-Pogo bottom surface                    –4.7 mm
PiSugar 3 pogo pin compressed (–1.5 mm)
PiSugar 3 top surface                      –6.2 mm
   ├── PiSugar 3 PCB (1.6 mm)
PiSugar 3 bottom                           –7.8 mm
   ├── 18650 cell case (~18 mm)
Total deck thickness (Pi Zero 2W + e-paper + RHB + PiSugar):
   10.1 + 7.8 + 18 ≈ 36 mm  vs the old stacking-header design's ~50 mm
```

RHB-Pogo adds ~4 mm of vertical space below the Pi. The PiSugar adds another ~3 mm of board + the 18650 case for the cell. Net win vs the v1 design: ~6 mm slimmer, and the Pi GPIO header on top is back to normal HAT-stacking height instead of being raised by a 14 mm extra-tall header.

RHB-Carrier lives elsewhere in the chassis (not part of the Z stack at all).

## 3. Raspberry Pi 40-pin GPIO claim

Same as v1 — the design claims 17 GPIO lines from the Pi. The RHB-Pogo board taps all 40 pad positions (to provide passthrough for PiSugar's contacts), but only 17 of them are routed to the FFC connector and on to RHB-Carrier.

| Pi pin | BCM | Function | Used by | On FFC? |
|---|---|---|---|---|
| 19 | GPIO 10 | SPI0 MOSI | All 4 slots | ✓ |
| 21 | GPIO 9  | SPI0 MISO | All 4 slots | ✓ |
| 23 | GPIO 11 | SPI0 SCLK | All 4 slots | ✓ |
| 26 | GPIO 7  | SPI0 CE1 | Slot A CSN | ✓ |
| 29 | GPIO 5  | spare | Slot A GDO0 | ✓ |
| 31 | GPIO 6  | spare | Slot A GDO2 | ✓ |
| 37 | GPIO 26 | spare | Slot B NSS | ✓ |
| 32 | GPIO 12 | spare | Slot B DIO0 | ✓ |
| 33 | GPIO 13 | spare | Slot B RESET | ✓ |
| 36 | GPIO 16 | spare | Slot C CS | ✓ |
| 15 | GPIO 22 | spare | Slot C DIO0 | ✓ |
| 16 | GPIO 23 | spare | Slot C DIO1 | ✓ |
| 18 | GPIO 24 | spare | Slot C DIO2 | ✓ |
| 22 | GPIO 25 | spare | Slot C RESET | ✓ |
| 11 | GPIO 17 | spare | Slot D CSN | ✓ |
| 13 | GPIO 27 | spare | Slot D CE | ✓ |
| 7  | GPIO 4  | spare | Slot D IRQ | ✓ |
| 2  | — | 5 V | Pi 5V rail | ✓ (passes power either direction) |
| 4  | — | 5 V | Pi 5V rail (redundant) | – (PiSugar uses this directly) |
| 6  | — | GND | Ground | ✓ |
| 14 | — | GND | Ground | – (PiSugar uses) |
| 1  | — | 3 V3 | Pi 3V3 rail | – (RHB-Carrier has its own LDO) |

Reserved (not routed to FFC, available on RHB-Pogo passthrough pads for PiSugar or other accessories):

| Pi pin | BCM | Function | Why reserved |
|---|---|---|---|
| 24 | GPIO 8  | SPI0 CE0 | E-paper HAT CS — passes through to Pi GPIO header for the HAT above |
| 3  | GPIO 2  | I²C0 SDA | BBQ20, OLED, PiSugar status I²C — passthrough only |
| 5  | GPIO 3  | I²C0 SCL | Same |
| 8  | GPIO 14 | UART0 TXD | BBQ20 UART fallback |
| 10 | GPIO 15 | UART0 RXD | Same |
| 12 | GPIO 18 | PCM CLK | Audio HAT compatibility |
| 35 | GPIO 19 | PCM FS | Same |
| 38 | GPIO 20 | PCM DIN | Same |
| 40 | GPIO 21 | PCM DOUT | Same |
| 27 | GPIO 0  | ID SD | HAT EEPROM |
| 28 | GPIO 1  | ID SC | Same |

### 3.1 FFC pin map (24-pin, 0.5 mm pitch)

The 24-pin FFC carries the GPIO subset RHB-Carrier needs, plus power and ground.

| FFC pin | Signal | Pi BCM | Notes |
|---|---|---|---|
| 1 | 5V | (Pi pin 2) | Power, either direction (Pi→Carrier or PiSugar→Carrier→Pi) |
| 2 | GND | (Pi pin 6) | |
| 3 | SPI0_MOSI | GPIO 10 | |
| 4 | SPI0_MISO | GPIO 9 | |
| 5 | SPI0_SCLK | GPIO 11 | |
| 6 | GND | — | Shield return between MISO and high-toggle GPIOs |
| 7 | Slot A CSN | GPIO 7 (CE1) | CC1101 chip select |
| 8 | Slot A GDO0 | GPIO 5 | CC1101 packet IRQ |
| 9 | Slot A GDO2 | GPIO 6 | CC1101 status |
| 10 | Slot B NSS | GPIO 26 | RFM95/69 chip select |
| 11 | Slot B DIO0 | GPIO 12 | RFM IRQ |
| 12 | Slot B RESET | GPIO 13 | RFM reset |
| 13 | Slot C CS | GPIO 16 | Universal spare CS |
| 14 | Slot C RESET | GPIO 25 | Adafruit-Bonnet-compatible |
| 15 | Slot C DIO0 | GPIO 22 | Adafruit-Bonnet-compatible |
| 16 | Slot C DIO1 | GPIO 23 | Adafruit-Bonnet-compatible |
| 17 | Slot C DIO2 | GPIO 24 | Adafruit-Bonnet-compatible |
| 18 | GND | — | Shield return |
| 19 | Slot D CSN | GPIO 17 | nRF24L01+ select |
| 20 | Slot D CE | GPIO 27 | nRF24L01+ chip-enable |
| 21 | Slot D IRQ | GPIO 4 | nRF24L01+ interrupt |
| 22 | UART_BYP_TX | GPIO 14 | For Slot C HC-12/HC-05 bypass mode |
| 23 | UART_BYP_RX | GPIO 15 | Same |
| 24 | GND | — | |

Two extra UART lines (FFC pins 22, 23) are routed to support Slot C's UART_BYPASS jumper for HC-12 / HC-05 / ESP-01 modules; they're harmless when the bypass jumper is open. Keeps the carrier's external connector count down (no separate UART break-out needed).

## 4. SPI fan-out and CS allocation

Unchanged from v1: four slots share SPI0 (MOSI/MISO/SCLK on GPIO 10/9/11). Each slot has its own dedicated CS GPIO. All chips (CC1101, RFM95, RFM69HCW, nRF24L01+, and generic SX127x/SX126x in slot C) tri-state MISO when CS is high — no bus buffer needed.

```
Pi SPI0 ──┬── pogo pin → RHB-Pogo trace → FFC → RHB-Carrier ─┐
          │                                                    │
          │  also passes UP through Pi GPIO header to          │
          │  any HAT above (e-paper CE0 etc.)                  │
          │                                                    │
          └────────────────────────────────────────────────────┴── all 4 slots
                                                                   (CS-isolated)
```

The FFC's MISO line is tri-stated by every module when its CS is high. Total bus loading: 4 chips (slots) + 1 HAT (e-paper above Pi) = 5 SPI peripherals on SPI0. Drive the bus at ≤5 MHz to handle any tri-state slop and the FFC's modest capacitance (~30 pF/m).

## 5. Module slots

Slot pin maps are identical to v1. Slot pinouts repeated here for completeness.

### 5.1 Slot A — CC1101 sub-GHz (1×8 socket on RHB-Carrier)

Fixed sub-GHz radio, stays plugged across all workshop builds.

**Physical:** 1×8 socket header, 2.54 mm pitch, female. Accepts through-hole CC1101 modules sold ~$3–5 (Ebyte E07-M1101D-TH or generic clones).

**Pinout** (per socket pin, pin 1 nearest to JST-PH input):

| Pin | Net | Goes to |
|---|---|---|
| 1 | GND | Carrier GND |
| 2 | VCC | 3 V3 (carrier LDO output) |
| 3 | GDO0 | FFC pin 8 → Pi GPIO 5 |
| 4 | CSN | FFC pin 7 → Pi GPIO 7 (CE1) |
| 5 | SCK | FFC pin 5 → Pi GPIO 11 |
| 6 | MOSI | FFC pin 3 → Pi GPIO 10 |
| 7 | MISO | FFC pin 4 → Pi GPIO 9 |
| 8 | GDO2 | FFC pin 9 → Pi GPIO 6 |

Driver: [`LSatan/SmartRC-CC1101-Driver-Lib`](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib). Software pin map: `CSN=7 GDO0=5 GDO2=6`.

### 5.2 Slot B — HopeRF RFM95W / RFM69HCW (16-pin SMD castellated)

LoRa (RFM95W, SX1276) or sub-GHz FSK (RFM69HCW), reflow-mounted directly on the carrier. Same footprint accepts RFM95W/96W/98W/RFM69HCW interchangeably.

| Module pin | Net | Goes to |
|---|---|---|
| 1 | GND | Carrier GND |
| 4 | 3.3V | Carrier 3V3 |
| 5 | DIO0 | FFC pin 11 → GPIO 12 |
| 9 | RESET | FFC pin 12 → GPIO 13 (10 kΩ pull-up to 3V3) |
| 10 | NSS | FFC pin 10 → GPIO 26 |
| 11 | SCK | FFC pin 5 → GPIO 11 |
| 12 | MISO | FFC pin 4 → GPIO 9 |
| 13 | MOSI | FFC pin 3 → GPIO 10 |
| 14, 16 | GND | Carrier GND |
| 15 | ANT | u.FL `ANT-B` pad |
| 2, 3, 6–8 | DIO3/4/1/2/5 | No-connect pads with optional 0Ω jumpers (default open) |

Driver: [`Adafruit_CircuitPython_RFM9x`](https://github.com/adafruit/Adafruit_CircuitPython_RFM9x) (LoRa) or [`Adafruit_CircuitPython_RFM69`](https://github.com/adafruit/Adafruit_CircuitPython_RFM69) (FSK). Software pin map: `CS=board.D26 RESET=board.D13 DIO0=board.D12`.

### 5.3 Slot C — Universal spare 1×9 header (Adafruit-Bonnet-compatible)

Drop-in pin order matches the Adafruit LoRa Radio Bonnet for Raspberry Pi. Stock Adafruit code runs with one constant change (CE1 → D16, because we burned CE1 on Slot A).

| Pin | Label | Net | Goes to |
|---|---|---|---|
| 1 | 3V3 | Carrier 3V3 | |
| 2 | GND | Carrier GND | |
| 3 | MOSI | FFC pin 3 → GPIO 10 | (or UART0 TXD via UART_BYPASS jumper) |
| 4 | MISO | FFC pin 4 → GPIO 9 | (or UART0 RXD via UART_BYPASS jumper) |
| 5 | SCK | FFC pin 5 → GPIO 11 | |
| 6 | CS | FFC pin 13 → GPIO 16 | |
| 7 | RESET | FFC pin 14 → GPIO 25 | Matches Adafruit |
| 8 | DIO0 | FFC pin 15 → GPIO 22 | Matches Adafruit |
| 9 | DIO1 | FFC pin 16 → GPIO 23 | Matches Adafruit |

Optional pads next to the header:
- `DIO2` → FFC pin 17 → GPIO 24 (for RFM95 pin 7)
- `CE` → FFC pin 20 → GPIO 27 (for nRF24L01+ adapter modules)

**UART_BYPASS jumper:** solder bridge that re-routes header pins 3, 4 from SPI MOSI/MISO to UART0 TXD/RXD (FFC pins 22, 23). Bridge for HC-12 / HC-05 / ESP-01; leave open for SPI radios.

Accepted modules: Adafruit RFM95W LoRa Breakout, Heltec SX1262 module, Ai-Thinker Ra-02 (with jumper bundle for the extra 7 of its 16 pins), ESP-01 / ESP-01S (with adapter), HC-12 / HC-05 (UART_BYPASS bridged), generic SX-class boards.

### 5.4 Slot D — nRF24L01+ (2×4 socket)

| Socket pin | Label | Net | Goes to |
|---|---|---|---|
| 1 | GND | Carrier GND | |
| 2 | VCC | Carrier 3V3 | + 10 µF tantalum (C7) within 5 mm — **mandatory**, see pitfalls |
| 3 | CE | FFC pin 20 → GPIO 27 | Chip enable, separate from CSN |
| 4 | CSN | FFC pin 19 → GPIO 17 | Active low chip select |
| 5 | SCK | FFC pin 5 → GPIO 11 | |
| 6 | MOSI | FFC pin 3 → GPIO 10 | |
| 7 | MISO | FFC pin 4 → GPIO 9 | |
| 8 | IRQ | FFC pin 21 → GPIO 4 | Active low interrupt |

Driver: [`nRF24/RF24`](https://github.com/nRF24/RF24) C++, [`circuitpython-nrf24l01`](https://github.com/nRF24/CircuitPython_nRF24L01) Python. Software pin map: `CE=27 CSN=17 IRQ=4`.

## 6. USB-A passthrough

Two USB-A through-hole vertical receptacles on the rear edge of RHB-Carrier (NOT on RHB-Pogo — the pogo adapter has no USB). Wired to a 4-pin JST-SH header that takes a short cable to the Pi's USB host port.

| JST-SH pin | Net | Notes |
|---|---|---|
| 1 | 5 V | From master switch, 700 mA PTC fused (F1) |
| 2 | D– | Tees to both USB-A ports |
| 3 | D+ | Tees to both USB-A ports |
| 4 | GND | Carrier GND |

USB does NOT traverse the FFC — the FFC is for GPIO only. The USB cable from RHB-Carrier to the Pi's USB port is a separate physical link. On Pi Zero 2 W this is the OTG port via an OTG adapter; on Pi 4/5 it's any of the four USB-A ports via a JST-SH-to-USB-A cable.

Bus arbitration rules unchanged from v1: the two USB-A ports tee onto one bus, treat as "either-or" not "both." See §10.7.

## 7. Power architecture

Multiple power-source scenarios are supported. The carrier auto-selects via Schottky-OR'd 5 V inputs.

```
SCENARIO 1 — Pi powered via its USB-C, no PiSugar, no JST-PH on RHB-Carrier:

  Pi USB-C → Pi 5V rail → Pi GPIO pin 2/4 → pogo pin → FFC pin 1 → Carrier 5V rail
                                                                    ├── PWR SW
                                                                    ├── LDO → 3V3 → radios
                                                                    └── 700 mA PTC → USB-A

SCENARIO 2 — PiSugar 3 underneath, supplies 5V to Pi:

  PiSugar boost → 5V → PiSugar pogo pin → RHB-Pogo bottom pad → trace → top pogo
                                                                          ↓
                                       ┌────────────────────────────── Pi GPIO pin 2/4
                                       ↓                                  → Pi powered
                                  FFC pin 1 → Carrier 5V rail
                                                ├── PWR SW
                                                ├── LDO → 3V3 → radios
                                                └── 700 mA PTC → USB-A

SCENARIO 3 — Standalone 18650 pack on JST-PH (no PiSugar, optionally no USB-C):

  JST-PH 5V → SS14 Schottky → Carrier 5V rail (ORed with FFC pin 1)
                                                ├── PWR SW
                                                ├── LDO → 3V3 → radios
                                                └── 700 mA PTC → USB-A
                              also feeds back through FFC pin 1 → pogo → Pi 5V
```

**Power-flow components:**
- **SS14 Schottky diodes:** two of them — one on the JST-PH input (reverse-pol protect), one on the FFC's 5V line, OR'd at the Carrier 5V rail node. Voltage drop ~0.3 V at 600 mA. Whichever input is higher wins, no contention.
- **SS-12F44 master switch:** gates the OR'd 5V on its way to the radios + LDO + USB-A PTC. Does NOT gate the FFC return to the Pi — so flipping the switch OFF kills the radios and USB-A passthrough but leaves the Pi running on whatever upstream source.
  - This is a CORRECTION from the v1 design which had the switch kill everything. The pogo-pin layout makes radio-only kill the natural default: the Pi has its own switch (USB-C unplug, PiSugar button, or 18650-pack switch upstream), so duplicating that on the carrier is redundant. Carrier switch = radio-rail kill only.
- **AP2112K-3.3 LDO:** unchanged from v1. 600 mA, SOT-25, feeds all four module slots' VCC pins.
- **Power LEDs:** D2 green (5V on Carrier, post-switch), D3 blue (LDO 3V3 healthy).

**Note on user-perceived behavior with switch OFF:**
- Pi keeps running (the carrier's switch doesn't gate the FFC → pogo → Pi 5V passthrough)
- Radios fully de-energized (3V3 LDO off, all module VCC pins at 0V)
- USB-A peripherals lose power
- E-paper HAT above the Pi keeps running (it's on the Pi's own 3V3, not ours)

This is the more useful failure mode for a cyberdeck — RF silence without sacrificing the rest of the deck. The v1 "everything off" semantic is still achievable by killing power upstream (the PiSugar button, or unplugging USB-C).

## 8. Antenna chain

Four u.FL receptacles on the rear edge of RHB-Carrier, one per slot, on short 50 Ω microstrip from each module's ANT pin. Same design as v1.

- 100 mm u.FL → SMA-F bulkhead pigtails route to chassis-edge SMA bulkheads
- No on-board antennas; chassis-edge SMA is mandatory for any serious RF
- See [`../05-networking-radio.md`](../05-networking-radio.md) for full antenna pairing recommendations

Pogo adapter has no RF on it.

## 9. Bill of materials

Refdes by board. Prices Q2 2026 USD, JLCPCB BOM upload qty 10.

### 9.1 RHB-Pogo BOM

| Refdes | Part | Package | Qty | Source | $ each | $ total |
|---|---|---|---|---|---|---|
| PCB | 55 × 30 mm, 2 layers, ENIG (gold on underside dimples) | — | 1 | JLCPCB | 0.80 | 0.80 |
| PP1–PP40 | SMT spring-loaded contact, ~3 mm uncomp / 1.5 mm comp, gold tip | SMT (custom) | 40 | LCSC C513611 or eq. | 0.05 | 2.00 |
| J1 | Hirose FH12-24S-0.5SH-G FFC connector, 24-pin 0.5 mm, bottom contact | SMT | 1 | LCSC C146095 | 0.30 | 0.30 |
| Optional MG1–MG4 | Neodymium magnet, 5 × 2 mm, N52, axial-magnetized | press-fit hole | 4 | AliExpress | 0.05 | 0.20 |
| **Subtotal (RHB-Pogo, per unit)** | | | | | | **$3.30** |

### 9.2 RHB-Carrier BOM

| Refdes | Part | Package | Qty | Source | $ each | $ total |
|---|---|---|---|---|---|---|
| PCB | 85 × 56 mm, 2 layers, HASL, blue or matte black solder mask | — | 1 | JLCPCB | 0.55 | 0.55 |
| J1 | Hirose FH12-24S-0.5SH-G FFC connector (matches RHB-Pogo) | SMT | 1 | LCSC C146095 | 0.30 | 0.30 |
| J2 | JST-PH 2-pin, top entry, 2.0 mm | TH | 1 | LCSC C160403 | 0.10 | 0.10 |
| J3 | JST-SH 4-pin USB tap | SMT | 1 | LCSC C146095 | 0.07 | 0.07 |
| J4, J5 | USB-A type-A vertical, through-hole | TH | 2 | LCSC C123564 | 0.18 | 0.36 |
| J6–J9 | u.FL receptacle, IPEX-1 (one per slot) | SMD | 4 | LCSC C40678 | 0.10 | 0.40 |
| J10 | Slot A — 1×8 socket, 2.54 mm | TH | 1 | LCSC C124416 | 0.06 | 0.06 |
| J11 | Slot B — RFM95/69 castellated landing (PCB only) | SMD pad | 1 | — | 0 | 0 |
| J12 | Slot C — 1×9 socket, 2.54 mm | TH | 1 | LCSC C124417 | 0.07 | 0.07 |
| J13 | Slot D — 2×4 socket, 2.54 mm | TH | 1 | LCSC C124419 | 0.09 | 0.09 |
| SW1 | SS-12F44 SPDT slide, R/A | TH | 1 | LCSC C319521 | 0.10 | 0.10 |
| U1 | AP2112K-3.3 LDO | SOT-25 | 1 | LCSC C6186 | 0.06 | 0.06 |
| D1 | SS14 Schottky 1 A (JST-PH reverse-pol) | SMA | 1 | LCSC C2480 | 0.02 | 0.02 |
| D2 | SS14 Schottky 1 A (FFC 5V OR-diode) | SMA | 1 | LCSC C2480 | 0.02 | 0.02 |
| D3 | LED green 0805 (5V) | 0805 | 1 | LCSC C72043 | 0.02 | 0.02 |
| D4 | LED blue 0805 (3V3) | 0805 | 1 | LCSC C72041 | 0.02 | 0.02 |
| F1 | PRG18BB100M PTC 1 A | 0805 | 1 | LCSC C16219 | 0.05 | 0.05 |
| R1, R2 | 1 kΩ LED limit | 0805 | 2 | LCSC C17513 | 0.005 | 0.01 |
| R3, R4 | 10 kΩ pull-ups (Slot B RESET, Slot D IRQ) | 0805 | 2 | LCSC C17414 | 0.005 | 0.01 |
| C1–C3 | 10 µF 16V (5V input, LDO in, LDO out) | 1206 / 0805 | 3 | LCSC C19702 | 0.02 | 0.06 |
| C4–C7 | 10 µF 6.3V per-slot decap | 0805 | 4 | LCSC C19702 | 0.02 | 0.08 |
| C8–C11 | 100 nF HF decap per slot | 0603 | 4 | LCSC C14663 | 0.005 | 0.02 |
| **Subtotal (RHB-Carrier, per unit)** | | | | | | **$2.47** |

### 9.3 Cable + per-kit total

| Item | $ each | Per kit |
|---|---|---|
| RHB-Pogo (assembled) | 3.30 | 3.30 |
| RHB-Carrier (assembled) | 2.47 | 2.47 |
| 24-pin 0.5 mm FFC, 100 mm, Type A | 0.30 | 0.30 |
| **Both boards + cable (per unit, qty 10)** | | **$6.07** |

| Modules (builder supplies per deck) | $ each | Notes |
|---|---|---|
| CC1101 sub-GHz module (E07-M1101D-TH) | 3.50 | |
| HopeRF RFM95W LoRa 868/915 MHz | 4.20 | |
| nRF24L01+ blue board | 1.50 | |
| Ai-Thinker Ra-02 for Slot C (optional) | 4.00 | |
| u.FL → SMA-F pigtails (4× for full kit) | 1.20 each = 4.80 | |
| **All 4 modules + 4 pigtails** | | **$17.50** |

| Optional | $ each |
|---|---|
| PiSugar 3 | ~35 |
| 18650 cell + holder (for JST-PH input) | ~5 |

**Workshop minimum-viable kit (RHB-Pogo + RHB-Carrier + FFC + CC1101 + 1 pigtail):** ~$10.40.

## 10. Pitfalls and gotchas

1. **Pogo pin alignment is critical.** The 40 pogo pins on RHB-Pogo MUST land on the Pi's GPIO solder-pad pattern with <0.3 mm position error. Order the PCB with the tightest position tolerance JLCPCB offers (±0.05 mm via the precision drill option). Cheap PCB drilling can drift enough that pin 1 sits on pin 2's pad — every signal is then shifted by one.

2. **Pogo pin clamping force.** 40 pins × 40 g/pin = ~1.6 kg of total clamping force needed for reliable contact. Magnets ALONE (4× N52 5×2 mm) provide ~600 g — NOT enough. Use M2 screws into the Pi's standoff holes for the primary clamp; magnets are convenience-only (to keep the assembly stable when screws aren't yet engaged).

3. **Pi 5 has the SoC on the BOTTOM with the Active Cooler clipped to it.** RHB-Pogo will NOT fit on a Pi 5 with the Active Cooler installed — the cooler thermal pad sits exactly where the pogo pin array goes. Pi 5 builds require: (a) using a passive heatsink ON TOP of the Pi 5 SoC instead, (b) leaving the SoC bare (thermal throttling under load), or (c) modifying the cooler to clear a window for the pogo footprint. Document this on the workshop SD card before a Pi 5 builder shows up.

4. **PiSugar 3 conflicts with Pi 5 already** — this isn't a new constraint from us. PiSugar 3 is officially Pi 4 / Zero 2 W. If your deck is Pi 5 + PiSugar, your build was already off the supported path.

5. **The pogo passthrough requires ENIG plating.** HASL leaves a non-flat surface that bounces the PiSugar's pogo pins. ENIG (Electroless Nickel + Immersion Gold) is mandatory for the bottom side of RHB-Pogo. Adds ~$0.30/board over HASL but absolutely required.

6. **FFC connector mate-cycle limit.** Hirose FH12 series is rated for 30 mate/unmate cycles. Workshops where the FFC is plugged/unplugged daily will wear them out within a year. Tell builders: connect once at assembly, leave alone.

7. **FFC Type A vs Type B confusion.** Type A has contacts on the SAME side both ends (straight pass). Type B has contacts on OPPOSITE sides (mirror). Pre-built cables come in both — order Type A explicitly. Wrong type wires everything backwards (pin 1 to pin 24) and the Pi sees garbage.

8. **CC1101 module pin order varies** between Ebyte / clones. Same warning as v1: verify with multimeter before powering.

9. **nRF24L01+ requires bulk decoupling AT THE MODULE.** 10 µF tantalum (C7) within 5 mm of pin 2 (VCC). Mandatory. PA+LNA variants need 22 µF.

10. **u.FL is 30-cycle rated.** Pigtail through chassis SMA for frequent antenna swaps. Same as v1.

11. **SPI clock above 8 MHz can corrupt MISO** with five chips on the bus (4 slots + e-paper HAT). Default driver clock to 5 MHz. Same as v1.

12. **Switch semantics changed from v1.** SS-12F44 now kills only the radio rail (LDO + USB-A passthrough), not the Pi. See §7. If you want a full-deck kill, route it via the PiSugar button or upstream 18650 pack switch.

13. **The pogo adapter is NOT field-serviceable.** All pogo pins and the FFC connector are SMT — must be JLCPCB-assembled (or equivalent). No hand-soldering in a workshop. Ship them pre-built.

14. **Magnets can scrape the Pi's bottom-side SMT components.** Pi 4 has a few small caps near the GPIO header on the bottom side; Pi 5 has the SoC underneath. Verify magnet placement clears all bottom-side components by 2+ mm. If you can't get clearance, drop the magnets and rely on screws only.

## 11. Sourcing and manufacturing

### 11.1 RHB-Pogo

| Item | Cost qty 10 | Cost qty 100 |
|---|---|---|
| PCB (55×30 mm, 2-layer, ENIG bottom) | $4 / 10 = $0.40 | $12 / 100 = $0.12 |
| JLCPCB Economic SMT (pogo pins + FFC connector) | $8 setup + $0.25 × 10 = $10.50 | $8 setup + $0.25 × 100 = $33 |
| Shipping DHL Express USA | $25 | $35 |
| **All-in / 10 units** | **~$3.99 / unit** | |
| **All-in / 100 units** | | **~$0.80 / unit** |

Why higher SMT cost than RHB-Carrier: the 40 pogo pins are non-standard parts; JLCPCB charges a setup fee per non-stocked component. Submit pogo pins as a single line-item with full datasheet upload. Confirm with JLCPCB before final BOM commit — if they refuse the pin part, fall back to LCSC C50046 (also short-stroke spring contact, slightly different geometry; check pad sizing).

### 11.2 RHB-Carrier

| Item | Cost qty 10 | Cost qty 100 |
|---|---|---|
| PCB (85×56 mm, 2-layer, HASL) | $5 / 10 = $0.50 | $10 / 100 = $0.10 |
| JLCPCB Economic SMT (~12 SMT parts incl. FFC, LDO, LEDs, MLCC) | $8 setup + $0.07 × 10 = $8.70 | $8 setup + $0.07 × 100 = $15 |
| Shipping (combined with RHB-Pogo order) | shared | shared |
| **All-in / 10 units** | **~$2.50 / unit** | |
| **All-in / 100 units** | | **~$0.40 / unit** |

### 11.3 FFC cables

Pre-built 24-pin 0.5 mm pitch FFC, Type A, sold in 100 mm / 150 mm / 200 mm lengths on AliExpress / LCSC: ~$0.30 each in qty 10, drops to ~$0.10 in qty 100. Order a few extra for spares.

### 11.4 Combined workshop kit fab order

For a 30-person workshop, order qty 50 of each board (covers spares + future workshops):
- 50× RHB-Pogo @ $0.80 = $40
- 50× RHB-Carrier @ $0.40 = $20
- 50× FFC cables @ $0.10 = $5
- Per-kit fab cost: $1.30
- Per-kit modules + pigtails: ~$10–17 depending on radio inclusions

KiCad project: two separate `.kicad_pro` files under `radio-header-board/kicad/rhb-pogo/` and `radio-header-board/kicad/rhb-carrier/`. Same JLCPCB Library Loader footprints. Net naming convention follows the BBQ20 daughterboard project in `../bb20/refs/`.

## 12. Reconciliation with workshop docs

The two-piece pogo-pin design supersedes the workshop's previous "daughter-PCB with stacking header" assumption. Deferred to follow-up commit per user direction. Edits needed:

- [`../workshops/03-main-build.md`](../workshops/03-main-build.md):
  - BOM line "Workshop daughter-PCB (CC1101 socket + spare radio header + USB-A breakout) ... $5" → replace with two lines (RHB-Pogo @ $0.80 + RHB-Carrier @ $0.40 + FFC) and update description
  - Remove the "2×20 stacking GPIO header (extra-tall, 14 mm) — Adafruit #2223" BOM line entirely — no longer used
  - Update wiring section steps 2–4 to describe pogo-snap mount + FFC connection rather than HAT-style stacking
- [`../workshops/04-radio-applications.md`](../workshops/04-radio-applications.md):
  - SPI bus map: `GPIO 25 = CC1101 GDO0` → **GPIO 5**, `GPIO 24 = CC1101 GDO2` → **GPIO 6**
  - "Spare radio header" pinout → replace with Slot C pinout from §5.3
  - Compatible modules table grows by RFM95/69 (Slot B) and nRF24L01+ (Slot D)
- (Possibly new) `workshops/02-radio-board-build.md` — a short pre-build session where workshop attendees solder the RHB-Carrier through-hole parts (sockets, USB-A, switch, JST-PH) onto the pre-assembled SMT board. RHB-Pogo arrives fully built (no soldering).

Workshop reconciliation remains a separate commit after this design lands.

## 13. References

- [Adafruit LoRa Radio Bonnet for Raspberry Pi — pinout guide](https://learn.adafruit.com/adafruit-radio-bonnets/pinouts) — authoritative for Slot C / Adafruit-compatible pin map (CE1, GPIO 25 RESET, GPIO 22 DIO0, GPIO 23 DIO1, GPIO 24 DIO2)
- [LSatan/SmartRC-CC1101-Driver-Lib](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) — CC1101 driver, canonical hardware-wiring table; full README copied to `refs/SmartRC-CC1101-README.md`
- [Adafruit_CircuitPython_RFM9x](https://github.com/adafruit/Adafruit_CircuitPython_RFM9x) — RFM95W / LoRa driver, default pin map
- [Adafruit_CircuitPython_RFM69](https://github.com/adafruit/Adafruit_CircuitPython_RFM69) — RFM69HCW driver, default pin map
- [`circuitpython-nrf24l01`](https://github.com/nRF24/CircuitPython_nRF24L01) — nRF24L01+ Python driver
- [PiSugar 3 hardware overview](https://www.pisugar.com/pisugar3.html) — pogo-pin contact pattern reference for the underside passthrough layer
- [Ebyte E07-M1101D-TH product page](https://www.cdebyte.com/products/E07-M1101D-TH) — CC1101 module datasheet
- [HopeRF RFM95W datasheet](https://www.hoperf.com/modules/lora/RFM95.html) — 16-pin SMD castellated footprint, RF specs
- [Mill-Max Spring-Loaded Connector reference](https://www.mill-max.com/products/spring-loaded-products/spring-loaded-connectors) — pogo pin alternative source if LCSC stock is short
- [`../05-networking-radio.md`](../05-networking-radio.md) — full radio buyer's guide, antenna context
- [`../workshops/03-main-build.md`](../workshops/03-main-build.md), [`../workshops/04-radio-applications.md`](../workshops/04-radio-applications.md) — workshops that use this hardware
- [`../bb20/BBQ20-DAUGHTERBOARD.md`](../bb20/BBQ20-DAUGHTERBOARD.md) — the BBQ20 keyboard carrier design doc

## 14. Status

- 2026-05-20 v1: stacked daughter-PCB with 14 mm extra-tall stacking header. Too thick — rejected.
- 2026-05-20 v2 (this doc): slim pogo-pin two-piece architecture. PiSugar-compatible underneath, Pi GPIO header untouched on top. Reviewable for design choices before any board is sent for fab.
- Pending: KiCad project scaffold (two projects: rhb-pogo, rhb-carrier), BOM CSVs for JLCPCB upload, workshop doc reconciliation, photos / hero render for the project README.
