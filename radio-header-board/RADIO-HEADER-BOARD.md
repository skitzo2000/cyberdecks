# Radio Header Board — Universal Cyberdeck Daughter-PCB

A 4-slot radio carrier that mounts on the Raspberry Pi 40-pin GPIO header without blocking it, integrates a master power switch, and is the standard radio infrastructure for every cyberdeck in this repo (slab, clamshell, BBQ20, all variants).

This document is the design source-of-truth. The board referenced as the "daughter-PCB" in [`../workshops/03-main-build.md`](../workshops/03-main-build.md) and [`../workshops/04-radio-applications.md`](../workshops/04-radio-applications.md) IS this board.

## 1. Scope and design goals

| Goal | How met |
|---|---|
| Plug any cheap RF chip into a deck without a custom PCB per radio | Four physical module slots covering the common $1–8 module footprints: CC1101 1×8, HopeRF RFM95/69 16-pin SMD, nRF24L01+ 2×4, and a universal 1×9 spare header (SX127x/SX126x breakouts, ESP-01, HC-12, anything) |
| Don't block the Pi GPIO header for other HATs | 2×20 pass-through stacking header (Adafruit 2223, 14 mm extra-tall) — the e-paper HAT or any other 40-pin HAT sits on top, untouched |
| One unambiguous power switch | Master 5 V slide switch (SS-12F44, panel-mount, edge-poking) gates the JST-PH input — kills Pi *and* radios together |
| Universal across all workshop variants | Mounts on Pi Zero 2 W, Pi 4, Pi 5; mechanical envelope is Pi-Zero-sized so it never overhangs a Pi 5; ribbon-cable escape option for chassis where the Pi can't sit near antennas |
| Cheap enough to give away in a workshop kit | Target ≤$8 in parts at qty 10 from JLCPCB, vs $30+ for a comparable assembled Adafruit Bonnet |

Non-goals: this board does NOT add an MCU (no RP2040, no ESP32 co-processor), it does NOT have an OLED, and it does NOT do USB host on its own — those belong to the Pi above it or other co-devices. The radio carrier is a passive pin-router with one transistor circuit (the LDO) and one mechanical switch.

## 2. Mechanical

| Param | Value |
|---|---|
| Board outline | 65 × 56 mm (Pi-Zero-2W footprint, fits over Pi 4/5 as well without overhang) |
| Thickness | 1.6 mm |
| Mounting holes | 4× M2.5, matching Pi Zero 2 W (58 × 23 mm pattern) and Pi 4/5 (58 × 49 mm pattern) — both sets present |
| GPIO header | 2×20 female pass-through stacking header, 14 mm extra-tall (Adafruit 2223 or eq.) on the BOTTOM of the PCB, mating with Pi header below |
| Top-side stacking exposure | Same 2×20 pattern brought up through to the top by the stacking header's long male tails — any 40-pin HAT (Waveshare e-paper, audio HAT, etc.) plugs on top without modification |
| Antenna access | One u.FL pad per radio slot (4 pads total), wired to each slot's ANT pin; optional SMA bulkhead breakout via 5-pin header on rear edge |
| Power switch | SS-12F44 right-angle SPDT slide, edge-mounted on the *front* edge facing the user, ~6 mm throw, 0.3 A 50 V rating |
| Power LED | Green 0805 LED + 1 kΩ series on the regulated 3.3 V output, visible through a chassis cutout next to the switch |
| Power input | JST-PH 2-pin, 2.0 mm pitch, 5 V from PiSugar tap or 18650 boost (PH = LATCHING, won't unseat under chassis vibration like PH-A) |
| USB-A passthroughs | 2× through-hole vertical USB-A type, wired to a 4-pin JST-SH header (5 V / D+ / D- / GND) that mates with a short cable to the Pi's USB-OTG (Zero 2 W) or USB-A bus (Pi 4/5) |

Board layout, left-to-right looking at the top face:

```
+-------------------------------------------------------------+
|  [PWR SW] [PWR LED]                          [u.FL A] [SMA] |
|                                              [u.FL B]       |
|  +--SLOT A--+ +--SLOT B--+                   [u.FL C]       |
|  |  CC1101  | |  RFM95/  |     +--SLOT D--+  [u.FL D]       |
|  |  1x8 skt | |  69 SMD  |     | nRF24L01+|                 |
|  |          | |  16-pin  |     |  2x4 skt |                 |
|  +----------+ +----------+     +----------+                 |
|                                                              |
|  +--SLOT C: universal 1x9 SX127x/SX126x/ESP-01/HC-12--+     |
|  |  3V3  GND  MOSI  MISO  SCK  CS  RST  DIO0  DIO1   |     |
|  +-----------------------------------------------------+    |
|                                                              |
|  [JST-PH 5V in]  [JST-SH USB] [USB-A]  [USB-A]              |
|                                                              |
|  o    2x20 stacking header (passes Pi GPIO upward)    o     |
|  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o o    |
|  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o  o o    |
+-------------------------------------------------------------+
   pin 2 →                                                ← pin 39 (Pi GPIO header underneath)
```

## 3. Raspberry Pi 40-pin GPIO claim

The header board claims 17 GPIOs from the Pi. The rest (I²C0, UART0, PCM, ID EEPROM, CE0) stay free for the HAT stacked on top. Numbers are BCM.

| Pi pin | BCM | Function | Used by | Notes |
|---|---|---|---|---|
| 19 | GPIO 10 | SPI0 MOSI | **All 4 slots** | Shared bus |
| 21 | GPIO 9  | SPI0 MISO | **All 4 slots** | Shared bus |
| 23 | GPIO 11 | SPI0 SCLK | **All 4 slots** | Shared bus |
| 26 | GPIO 7  | SPI0 CE1 | Slot A CSN | CC1101 select |
| 29 | GPIO 5  | spare | Slot A GDO0 | CC1101 packet IRQ |
| 31 | GPIO 6  | spare | Slot A GDO2 | CC1101 status |
| 37 | GPIO 26 | spare | Slot B NSS | RFM95/69 select |
| 32 | GPIO 12 | spare | Slot B DIO0 | RFM RxDone/TxDone IRQ |
| 33 | GPIO 13 | spare | Slot B RESET | RFM reset (active low) |
| 36 | GPIO 16 | spare | Slot C CS | Universal spare select |
| 15 | GPIO 22 | spare | Slot C DIO0 | Matches Adafruit Bonnet |
| 16 | GPIO 23 | spare | Slot C DIO1 | Matches Adafruit Bonnet |
| 18 | GPIO 24 | spare | Slot C DIO2 | Matches Adafruit Bonnet |
| 22 | GPIO 25 | spare | Slot C RESET | Matches Adafruit Bonnet |
| 11 | GPIO 17 | spare | Slot D CSN | nRF24L01+ select |
| 13 | GPIO 27 | spare | Slot D CE | nRF24L01+ chip-enable (TX/RX gate) |
|  7 | GPIO 4  | spare | Slot D IRQ | nRF24L01+ interrupt out |

Reserved — DO NOT route on the header board (these belong to the e-paper or other stacked HATs):

| Pi pin | BCM | Function | Why reserved |
|---|---|---|---|
| 24 | GPIO 8  | SPI0 CE0 | Waveshare e-paper HAT CS (workshop 03) |
|  3 | GPIO 2  | I²C0 SDA | BBQ20 keyboard MCU (clamshell builds), OLED add-ons |
|  5 | GPIO 3  | I²C0 SCL | Same as above |
|  8 | GPIO 14 | UART0 TXD | BBQ20 UART fallback path |
| 10 | GPIO 15 | UART0 RXD | Same |
| 12 | GPIO 18 | PCM CLK | Free for I²S audio HATs |
| 35 | GPIO 19 | PCM FS | Same |
| 38 | GPIO 20 | PCM DIN | Same |
| 40 | GPIO 21 | PCM DOUT | Same |
| 27 | GPIO 0  | ID SD | HAT EEPROM I²C (do not touch) |
| 28 | GPIO 1  | ID SC | Same |

Pi 5 note: GPIOs are exposed via RP1, not the SoC directly. BCM numbering is preserved; `libgpiod` v2 with `/dev/gpiochip4` is the correct interface on Pi 5. The SPI0 controller is fully compatible with Pi 4/Zero code at the spidev layer.

## 4. SPI fan-out and CS allocation

All four radio slots share SPI0 (MOSI/MISO/SCLK on GPIO 10/9/11). Module isolation is enforced at the CS line — each slot has its own dedicated CS GPIO, and modules sitting on the bus with CS de-asserted tri-state their MISO. This is the standard textbook approach; nothing fancy.

Bus contention rules:
- Only one module's CS is asserted at a time. The Linux SPI subsystem enforces this per-transaction.
- All four slots' MISO lines tie together at one bus node. Each module's MISO is verified to tri-state when CS is high. The four chips used here (CC1101, RFM95W, RFM69HCW, nRF24L01+, plus generic SX127x/SX126x in slot C) all tri-state per datasheet, so no bus buffer is needed.
- The e-paper HAT above us also sits on SPI0 (its CS is CE0). When we drive any of our slots, the e-paper's CS stays high and the e-paper tri-states its MISO line.

If you experience MISO glitching at >8 MHz, lower the SPI clock in your driver — none of these radios need more than 5 MHz to be functional.

```
Pi SPI0  ─────┬───┬───┬───┬───┬─── (stacked HAT)
              │   │   │   │   │
   CE0 ───────┼───┼───┼───┼───┼──→  (e-paper, above us)
   CE1 (GPIO7)┘   │   │   │   │  → Slot A CSN (CC1101)
   GPIO 26 ───────┘   │   │   │  → Slot B NSS (RFM95/69)
   GPIO 16 ───────────┘   │   │  → Slot C CS  (universal)
   GPIO 17 ───────────────┘   │  → Slot D CSN (nRF24L01+)
   MOSI ──────────────────────┴──→ all slots + e-paper
   MISO ←──────────────────────── all slots + e-paper (tri-stated when CS high)
   SCLK ──────────────────────→ all slots + e-paper
```

## 5. Module slots

### 5.1 Slot A — CC1101 sub-GHz (1×8 socket, fixed)

The deck's "always there" sub-GHz radio. Stays plugged in across all workshop builds. Listens on 433 MHz or 868/915 MHz depending on the module variant.

**Physical:** 1×8 socket header, 2.54 mm pitch, female. Accepts the through-hole CC1101 modules sold ~$3–5 on AliExpress (search "CC1101 SPI module" — Ebyte E07-M1101D-TH and the smaller no-name boards both have this 1×8 footprint).

**Pinout** (per socket pin, looking at the top face, pin 1 is closest to the JST-PH power input):

| Pin | Net | Goes to |
|---|---|---|
| 1 | GND | Board GND |
| 2 | VCC | 3V3 (LDO output) |
| 3 | GDO0 | Pi GPIO 5 |
| 4 | CSN | Pi GPIO 7 (CE1) |
| 5 | SCK | Pi GPIO 11 |
| 6 | MOSI | Pi GPIO 10 |
| 7 | MISO | Pi GPIO 9 |
| 8 | GDO2 | Pi GPIO 6 |

Verify on receipt: not all $3 modules use the same pin order. The Ebyte E07-M1101D-TH puts pin 1 at GND on the corner with the antenna trace; some clones swap GDO0/CSN. If a module reads `0xFF` from every register on first power, depopulate and flip the socket pinout — there is no electrical safety risk since CC1101 is 3.3 V tolerant on every signal, but you'll need to map differently in software.

ANT pad of the CC1101 module reaches a u.FL pad labeled `ANT-A` on the carrier (one trace, kept under 5 mm).

**Driver:** [`LSatan/SmartRC-CC1101-Driver-Lib`](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) on Arduino, or [`Wireless-Sensor/RFD900x`-class C++ libs](https://github.com/SpaceTeddy/CC1101) and the cyberdeck-stock `~/cc1101-scan.py` shipped on the workshop SD card. Default GDO0 on GPIO 5 means Python code reads `IRQ_PIN = 5` (BCM) — update from workshop 04's stale `25` value.

### 5.2 Slot B — HopeRF RFM95W / RFM69HCW (16-pin SMD castellated)

LoRa (RFM95W, SX1276) or sub-GHz FSK (RFM69HCW) on the canonical HopeRF castellated footprint, mounted directly on the carrier (no socket — these modules are surface-mount and stay).

**Physical:** 16 castellated pads on a 16 × 11 mm rectangle, 2.0 mm pitch on the long sides. Same exact footprint for RFM95W, RFM96W, RFM98W, and RFM69HCW — you can desolder one and reflow another in its place. The carrier provides the landing pattern + an L-bend SMA pad on one end.

**Pinout** (canonical HopeRF, pin 1 marked by dot or notch on the module; numbering goes counter-clockwise viewed from above):

| Pin | Net | Goes to | Notes |
|---|---|---|---|
| 1 | GND | Board GND | |
| 2 | DIO3 | (unused, NC pad) | Optional CAD / chan-busy IRQ |
| 3 | DIO4 | (unused, NC pad) | Optional |
| 4 | 3.3V | 3V3 (LDO output) | 10 µF decap on the pin |
| 5 | DIO0 | Pi GPIO 12 | RxDone (LoRa) / PacketSent (FSK) |
| 6 | DIO1 | (unused, NC pad) | RxTimeout / FifoLevel |
| 7 | DIO2 | (unused, NC pad) | FhssChangeChannel / SyncAddress |
| 8 | DIO5 | (unused, NC pad) | ClkOut / ModeReady |
| 9 | RESET | Pi GPIO 13 | Active low, 10 kΩ pull-up to 3V3 |
| 10 | NSS | Pi GPIO 26 | Slot B chip select |
| 11 | SCK | Pi GPIO 11 | Shared SPI0 |
| 12 | MISO | Pi GPIO 9 | Shared SPI0 |
| 13 | MOSI | Pi GPIO 10 | Shared SPI0 |
| 14 | GND | Board GND | |
| 15 | ANT | u.FL `ANT-B` pad | Short trace |
| 16 | GND | Board GND | Chassis tie |

DIO1/2/3/4/5 are deliberately left as no-connect pads with optional 0Ω jumpers to Slot C's free DIO lines — if you want a second LoRa receiver running interrupts on DIO1 (FifoLevel for streaming-mode) you can bridge the jumper at assembly time. Default: leave open.

**Driver:** [`Adafruit_CircuitPython_RFM9x`](https://github.com/adafruit/Adafruit_CircuitPython_RFM9x) for LoRa (RFM95), [`Adafruit_CircuitPython_RFM69`](https://github.com/adafruit/Adafruit_CircuitPython_RFM69) for FSK (RFM69HCW). Software pin map: `CS=board.D26 RESET=board.D13 DIO0=board.D12`.

### 5.3 Slot C — Universal spare (1×9 header, Adafruit-Bonnet-compatible)

The "anything goes" socket. 1×9 pin female header, 2.54 mm pitch. Designed to accept:

- Adafruit RFM95W LoRa Breakout (8-pin variant, leaves DIO1 floating)
- Heltec SX1262 module on adapter
- Ai-Thinker Ra-02 (SX1278, 16-pin module — wires via separate jumper bundle, only 9 of the 16 land on this header)
- nRF24L01+ via adapter (although Slot D is the proper home)
- ESP-01 (ESP8266 SoC, 2×4 header — fits across pins 1–8 with adapter PCB)
- HC-12 (433 MHz UART transceiver — bypass SPI, see notes below)
- Any future SX-class module

**Pinout** (header pin 1 nearest the board's left edge; matches the Adafruit LoRa Radio Bonnet for Raspberry Pi pin order so that **stock Adafruit code runs unchanged**):

| Pin | Label | Net | Goes to |
|---|---|---|---|
| 1 | 3V3 | 3V3 (LDO) | Power |
| 2 | GND | Board GND | |
| 3 | MOSI | Pi GPIO 10 | Shared SPI0 |
| 4 | MISO | Pi GPIO 9 | Shared SPI0 |
| 5 | SCK | Pi GPIO 11 | Shared SPI0 |
| 6 | CS | Pi GPIO 16 | Slot C select |
| 7 | RESET | Pi GPIO 25 | **Matches Adafruit Bonnet** |
| 8 | DIO0 | Pi GPIO 22 | **Matches Adafruit Bonnet** |
| 9 | DIO1 | Pi GPIO 23 | **Matches Adafruit Bonnet** |

Two additional optional pads next to the header:
- `DIO2` to Pi GPIO 24 — solder a wire from the module's DIO2 pin (RFM95 pin 7) to this pad if your code uses it
- `CE` to Pi GPIO 27 — for nRF24L01+ via adapter, the CE pin (active TX/RX gate) lives here

**Why Adafruit-compatible matters:** the stock CircuitPython library `Adafruit_CircuitPython_RFM9x` defaults to `CS=board.CE1 RESET=board.D25 DIO0=board.D22`. The Bonnet uses CE1 for CS, but we burned CE1 on Slot A (CC1101). Our software pin map for Slot C is therefore: `CS=board.D16 RESET=board.D25 DIO0=board.D22` — one constant changes from Adafruit stock, the rest is drop-in. Worth the swap: the alternative (running Slot C on CE1) would forbid plugging in both CC1101 and a Slot-C LoRa at once, which kills the whole point of a 4-slot board.

**HC-12 / UART modules in Slot C:** if you plug an HC-12 (4-pin: VCC, GND, TX, RX) in across pins 1, 2, 3, 4 of this header, you'll get power but NOT a working serial path — pins 3, 4 are SPI MOSI/MISO not UART. The board includes a `UART_BYPASS` solder jumper next to Slot C that, when bridged, re-routes header pins 3, 4 to Pi GPIO 14 (TXD0) and GPIO 15 (RXD0) respectively. Bridge it for HC-12 / HC-05 / ESP-01 use; leave open for SPI radios. This is the single piece of "creative reuse" needed for cheap UART modules.

### 5.4 Slot D — nRF24L01+ (2×4 socket)

The cheapest 2.4 GHz radio on planet earth ($1.50/module). Standard "blue board" Chinese module with PA+LNA variants ("nRF24L01+PA+LNA" with antenna jack — uses the same socket).

**Physical:** 2×4 female socket header, 2.54 mm pitch. The corresponding male pins on the module are pin 1 in the corner with the silkscreen square; orientation matters because the module has the SoC and antenna pattern on one face only.

**Pinout** (canonical nRF24L01+ "blue board", with module antenna facing the board edge):

| Socket pin | Label | Net | Goes to |
|---|---|---|---|
| 1 | GND | Board GND | |
| 2 | VCC | 3V3 (LDO output) | **See pitfalls** |
| 3 | CE | Pi GPIO 27 | Chip enable (TX/RX gate, separate from CSN) |
| 4 | CSN | Pi GPIO 17 | Active low chip select |
| 5 | SCK | Pi GPIO 11 | Shared SPI0 |
| 6 | MOSI | Pi GPIO 10 | Shared SPI0 |
| 7 | MISO | Pi GPIO 9 | Shared SPI0 |
| 8 | IRQ | Pi GPIO 4 | Active low, RxDataReady / TxDataSent / MaxRetries |

The nRF24L01+ draws short (~150 µs) but sharp current bursts on TX (peak ~115 mA at +0 dBm, ~250 mA on the +PA+LNA module). The Pi's 3V3 rail (or even our LDO) can sag under those bursts and reset the module mid-transmission. **Mandatory:** 10 µF tantalum or aluminum-polymer capacitor placed within 5 mm of the nRF24L01+ VCC pin (refdes C7). A 100 nF ceramic next to it (C8) handles HF noise. With those two caps, the module is stable on the LDO's 3V3 rail; without them, you get random "module not found" and "TX failed" errors that look like a bad solder joint.

**Driver:** [`nRF24/RF24`](https://github.com/nRF24/RF24) C++ lib, [`circuitpython-nrf24l01`](https://github.com/nRF24/CircuitPython_nRF24L01) for Python. Software pin map: `CE=27 CSN=17 IRQ=4 SPI=/dev/spidev0.0`.

## 6. USB-A passthrough

Two USB-A type-A vertical receptacles on the rear edge of the board, intended for plug-in radio peripherals (LILYGO T-Beam for Meshtastic, BU-353-S4 USB GPS, RTL-SDR Blog V4, Flipper Zero in serial mode, nRF52840 dongle, etc.).

These are NOT a USB hub. The two ports tee onto a single bus that runs back to the Pi via a 4-pin JST-SH cable (5 V / D+ / D- / GND) plugged into the Pi's USB host port. On the Pi Zero 2 W this means using the OTG port (USB-A side of an OTG adapter); on the Pi 4/5 this means a short JST-SH-to-USB-A cable plugged into one of the Pi's four USB-A receptacles.

| Pin | Net | Notes |
|---|---|---|
| 1 | 5V | From master switch, 700 mA fused via PTC (PRG18BB100M) |
| 2 | D- | Tees to both USB-A ports |
| 3 | D+ | Tees to both USB-A ports |
| 4 | GND | Board GND |

**Bus arbitration warning:** plugging in two USB devices on these ports simultaneously creates a Y-cable scenario. Most well-behaved USB devices tolerate this, but some (notably some RTL-SDR clones with sloppy USB stacks) will refuse to enumerate when sharing D+/D- with another device. Treat the two USB-A ports as "either-or," not "both at once." Future revision could swap in a CH334 4-port USB 2.0 hub IC ($0.70) for proper multiplex — flagged as v2 stretch.

Why USB-A through-hole instead of USB-C: this board is solder-friendly and workshop-buildable. Through-hole USB-A is the easiest connector on the board (literally four pins + four legs), survives field abuse, and the devices you plug into a cyberdeck radio header (T-Beam, GPS dongle, SDR) ship with USB-A natively. USB-C would add a CC pin-strap requirement and is not worth the parts-count for a passthrough.

## 7. Power architecture

```
                           ┌──── 5V LED ── 1k ── GND
                           │
JST-PH 5V ──┬── SS-12F44 ──┴── 5V rail ──┬──── USB-A 5V (via 700mA PTC)
            │   slide switch              │
            │                             ├──── AP2112K-3.3 LDO ──┬── 3V3 rail
            │                             │                       │
            └── reverse-pol Schottky      │                       ├── 3V3 LED ── 1k ── GND
                (SS14, 1A)                │                       │
                                          │                       └── all 4 radio slots (VCC pins)
                                          │
                                          └── Pi 5V via 2x20 stacking header pins 2, 4
```

**Master slide switch (SS-12F44):** SPDT, panel-mount with right-angle pins, 0.3 A 50 V rating, "C&K" or "Alps" knockoff fine. Mounted on the front edge of the board with the throw facing the user. ON = up, OFF = down. Lifetime > 10,000 cycles. The switch carries the FULL deck current (Pi + e-paper + all radios + USB peripherals) — peak ~600 mA, well under the 300 mA continuous rating only because the PiSugar/18650 supply current-limits ahead of us. If you intend to skip the PiSugar and feed >300 mA continuous through here, upgrade the switch to a higher-rated SPDT (E-Switch RA12 series, 3 A rating).

**3.3 V LDO (AP2112K-3.3):** SOT-25 LDO, 600 mA continuous output, 250 mV typ dropout at 600 mA, 0.5% line regulation. This rail powers ALL four radio sockets' VCC pins. Total budget:
- CC1101 ~30 mA TX peak
- RFM95W TX +20 dBm ~120 mA peak burst
- RFM69HCW TX +20 dBm ~130 mA peak burst (only Slot B can hit this since C and A don't have PA modes ≥+17 dBm)
- nRF24L01+ ~250 mA peak (PA+LNA variant)
- Spare Slot C ~150 mA peak
- = ~680 mA worst-case all-at-once

In practice you won't TX on all four at once. With burst capacitance (4× 10 µF tantalum, one per slot, refdes C4–C7) the LDO holds 3.30 V down to single-slot worst-case peaks. If you plan to run dense LoRaWAN gateway-style multi-slot TX (rare on a deck), upgrade the LDO to AP2114H (1 A rating, same footprint and pinout) — single component swap.

**Why not pass through the Pi's own 3V3 rail?** The Pi's 3V3 rail is rated 500 mA TOTAL, shared between Pi internals + GPIO headers + any HAT above us. A 120 mA LoRa TX burst drops Pi 3V3 by ~80 mV at the connector — enough to spuriously reset HATs that have tight 3V3 detect (the Waveshare e-paper has been known to wedge under this). Independent LDO from 5 V solves it cleanly.

**Reverse-polarity protection:** an SS14 1 A Schottky diode in series on the JST-PH+ line, refdes D1. Cathode toward the switch. If you wire JST-PH backwards, the diode drops the wrong-polarity voltage and the board stays off. ~0.3 V forward drop at 600 mA, acceptable.

**Power LEDs:** two LEDs:
- `D2` green 0805 on 5V (post-switch) — indicates "deck powered"
- `D3` blue 0805 on 3V3 — indicates "radio rail healthy" (the LDO is up). Useful diagnostic — if D2 is on and D3 is off, the LDO has shut down (overcurrent or short on a radio rail).

## 8. Antenna chain

Each of the four slots has a dedicated u.FL receptacle on the rear edge of the board, on a short (<10 mm) trace from the module's ANT pin. Pads labeled `ANT-A` through `ANT-D` next to each receptacle.

```
Slot A (CC1101)     → u.FL ANT-A → 50 Ω trace → external pigtail / chassis SMA bulkhead
Slot B (RFM95/69)   → u.FL ANT-B → 50 Ω trace → external pigtail
Slot C (universal)  → u.FL ANT-C → 50 Ω trace → external pigtail
Slot D (nRF24L01+)  → u.FL ANT-D → 50 Ω trace → external pigtail
```

**Track impedance:** PCB stackup tuned to 50 Ω microstrip on 1.6 mm FR-4 with 0.5 mm trace width over the bottom-side ground pour. JLCPCB's stack matches this within ±5 Ω which is fine at sub-2.4 GHz.

**Chassis antennas (preferred over module-mount whips):** use 100 mm u.FL → SMA bulkhead pigtails (Taoglas or Sucoflex) to bring the RF out of the case to a metal-shell SMA bulkhead. Then 50 Ω SMA antennas of the user's choice attach externally. This isolates the antennas from the cyberdeck's RF-noisy interior (the Pi's HDMI clock, switching regulators, USB 3.0 SSC) and matches the practical pattern from [`../05-networking-radio.md`](../05-networking-radio.md).

**No on-board antennas.** Helical chip antennas and "rubber ducks" on $1 modules look great in product photos but are poor performers at every frequency; in a metal cyberdeck chassis they're useless. External chassis antennas are mandatory for any serious RF work. The board has u.FL pads, period.

## 9. Bill of materials

Refdes match standard KiCad symbol library conventions. Prices are Q2 2026 USD, JLCPCB BOM upload qty 10.

| Refdes | Part | Package | Qty | Source | $ each | $ total |
|---|---|---|---|---|---|---|
| **Board** | 65×56 mm, 2 layers, HASL, blue or matte black | — | 1 | JLCPCB | 0.50 | 0.50 |
| **J1** | 2×20 stacking GPIO header, 14 mm tall (Adafruit 2223) | TH | 1 | Adafruit/Amazon | 1.50 | 1.50 |
| **J2** | JST-PH 2-pin, top entry, 2.0 mm | TH | 1 | LCSC C160403 | 0.10 | 0.10 |
| **J3** | JST-SH 4-pin, side entry, 1.0 mm | SMD | 1 | LCSC C146095 | 0.07 | 0.07 |
| **J4, J5** | USB-A type-A vertical, through-hole | TH | 2 | LCSC C123564 | 0.18 | 0.36 |
| **J6** | u.FL receptacle, IPEX-1 (4× total) | SMD | 4 | LCSC C40678 | 0.10 | 0.40 |
| **J7** | Slot A — 1×8 socket, 2.54 mm, female | TH | 1 | LCSC C124416 | 0.06 | 0.06 |
| **J8** | Slot B — RFM95/69 footprint (16 castellated pads, no header — module solders direct) | SMD pad | 1 | — (PCB only) | 0 | 0 |
| **J9** | Slot C — 1×9 socket, 2.54 mm, female | TH | 1 | LCSC C124417 | 0.07 | 0.07 |
| **J10** | Slot D — 2×4 socket, 2.54 mm, female | TH | 1 | LCSC C124419 | 0.09 | 0.09 |
| **SW1** | SS-12F44 SPDT slide switch, R/A, panel-mount | TH | 1 | LCSC C319521 | 0.10 | 0.10 |
| **U1** | AP2112K-3.3 LDO, 3.3 V 600 mA | SOT-25 | 1 | LCSC C6186 | 0.06 | 0.06 |
| **D1** | SS14 Schottky 1 A 40 V | SMA | 1 | LCSC C2480 | 0.02 | 0.02 |
| **D2** | LED green 0805, 5 V rail indicator | 0805 | 1 | LCSC C72043 | 0.02 | 0.02 |
| **D3** | LED blue 0805, 3.3 V rail indicator | 0805 | 1 | LCSC C72041 | 0.02 | 0.02 |
| **F1** | PRG18BB100M PTC fuse, 1 A hold | 0805 | 1 | LCSC C16219 | 0.05 | 0.05 |
| **R1, R2** | 1 kΩ 0805 (LED current limit) | 0805 | 2 | LCSC C17513 | 0.005 | 0.01 |
| **R3, R4** | 10 kΩ 0805 (pull-ups: Slot B RESET, Slot D IRQ) | 0805 | 2 | LCSC C17414 | 0.005 | 0.01 |
| **C1, C2** | 10 µF 16 V 1206 X7R (5 V input, LDO input) | 1206 | 2 | LCSC C19702 | 0.02 | 0.04 |
| **C3** | 10 µF 6.3 V 0805 X7R (LDO output) | 0805 | 1 | LCSC C19702 | 0.02 | 0.02 |
| **C4–C7** | 10 µF 6.3 V 0805 X7R (per-slot bulk decap) | 0805 | 4 | LCSC C19702 | 0.02 | 0.08 |
| **C8–C11** | 100 nF 50 V 0603 X7R (per-slot HF decap) | 0603 | 4 | LCSC C14663 | 0.005 | 0.02 |
| **Subtotal — board parts** | | | | | | **$3.60** |
| **Modules** (per-deck, builder supplies) | | | | | | |
| | CC1101 sub-GHz module, E07-M1101D-TH | TH | 1 | AliExpress | 3.50 | 3.50 |
| | HopeRF RFM95W LoRa 868/915 MHz | SMD | 1 | LCSC C2884975 | 4.20 | 4.20 |
| | nRF24L01+ blue board | TH | 1 | AliExpress | 1.50 | 1.50 |
| | (Optional) Ai-Thinker Ra-02 for Slot C | TH | 1 | AliExpress | 4.00 | 4.00 |
| **u.FL pigtails (per kit)** | 100 mm u.FL → SMA-F bulkhead, RG-178 | — | 4 | AliExpress | 1.20 | 4.80 |

**Per-board parts only (no modules, no pigtails):** ~$3.60 at qty 10.
**Per-kit with all four radios + four pigtails:** ~$21.60.
**Minimum-viable kit (board + CC1101 + one pigtail):** ~$8.30 — drops the workshop kit cost from $5 to $8 vs. the original 2-slot design but adds three more radio sockets.

Module BOM lines are NOT shipped on the assembled PCB — they go in the workshop kit bag.

## 10. Pitfalls and gotchas

1. **CC1101 module pin order varies.** The E07-M1101D-TH is the workshop default; clones from other vendors may swap GDO0/CSN or VCC/GND. Always verify with a multimeter before powering — VCC backwards onto a CC1101 will brick it within 5 seconds. (Reverse-pol diode D1 protects the LDO, not the modules.)

2. **nRF24L01+ requires bulk decoupling AT THE MODULE.** The 10 µF on C7 (slot D) is mandatory. Builders who skip it report "module not found" errors that look like driver bugs but are brownouts. PA+LNA variants need 22 µF.

3. **The u.FL connectors are fragile.** Each u.FL is rated for ~30 mate/unmate cycles. If you intend to swap antennas frequently, terminate the u.FL once with a pigtail, route the pigtail through a chassis SMA bulkhead, and swap at the SMA side — SMA is rated for >500 cycles.

4. **SPI clock above 8 MHz can corrupt MISO** when four chips share the bus with sloppy tri-state behavior. Default the spidev clock to 5 MHz in any `~/.../cc1101-scan.py` or `lora-hello.py` shipped on the SD card; the radios don't need more for the data rates they support.

5. **Adafruit RFM Bonnet's `D25` for RESET conflicts with the old workshop pin map** which put CC1101 GDO0 on GPIO 25. The new GPIO map (this doc, §3) moves CC1101 GDO0 to GPIO 5. Workshop docs need updating; see §12.

6. **Slot C UART_BYPASS jumper is one-way.** Bridge it for HC-12 / HC-05 / ESP-01; UNBRIDGE before reusing Slot C for an SPI radio. Otherwise SPI MOSI/MISO are shorted to UART TX/RX and you'll see garbled spidev traffic.

7. **USB-A passthrough is two ports on one bus, not a hub.** Plug ONE device at a time unless both devices are known to tolerate D+/D- teeing.

8. **Slide switch breaks the WHOLE deck.** The master kill switch interrupts 5 V to the Pi as well as the radios. This is what the user asked for — single unambiguous "everything off" — but means you can't `radio-off` to save 300 mA while keeping the Pi running. If you later want a radio-only-off mode, add an SI2301-class P-MOSFET between LDO and the radio rail and drive its gate from a free GPIO. Flagged as a v2 stretch.

9. **Pi 5 + 14 mm stacking header height is fine** for the Active Cooler (clears by 4 mm), but the Pi 5 PoE+ HAT and any 30+ mm tall add-ons WILL collide with the next HAT above us. Pi Zero 2 W and Pi 4 have no clearance issue.

10. **Antenna trace impedance assumes JLCPCB default stackup.** If you order from a PCB house with a different prepreg thickness (>1.55 mm or <1.45 mm), recalculate the 0.5 mm microstrip — at 2.4 GHz (nRF24, Slot D) the mismatch causes measurable VSWR.

## 11. Sourcing and manufacturing

**JLCPCB BOM:** all SMD parts listed in §9 have LCSC part numbers compatible with JLCPCB Economic SMT assembly. PTH parts (sockets, JST connectors, USB-A receptacles, slide switch, stacking header) go in the workshop kit bag and are hand-soldered. The PCB houses one side of SMT placement (top); RFM95/69 module goes on the bottom or top — doesn't matter mechanically as long as you order the JLC stencil with the matching layer mask.

| Item | Cost qty 10 | Cost qty 100 |
|---|---|---|
| PCB (65×56 mm, 2-layer, HASL, blue solder mask) | $2 / 10 = $0.20 | $5 / 100 = $0.05 |
| JLCPCB Economic SMT assembly (one side, ~10 SMT parts) | $8 setup + $0.05 × 10 = $8.50 | $8 setup + $0.05 × 100 = $13 |
| Shipping to USA (DHL Express, 5 days) | $25 flat | $35 |
| **All-in / 10 boards** | **~$3.55 / board assembled** | |
| **All-in / 100 boards** | | **~$0.53 / board assembled** |

The 100-unit run drops per-board cost into the giveaway range (workshop kits at $0.53 cost + kit-bag parts ~$3 = ~$3.50 total per kit). Order 100 if running >3 workshops or one big maker-faire event.

**KiCad project layout:** standard 6-file project (`.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, `fp-lib-table`, `sym-lib-table`, `.kicad_prl`). All footprints from JLCPCB Library Loader. Net naming convention follows the BBQ20 daughterboard project in `../bb20/refs/`. Place the project under `radio-header-board/kicad/` when scaffolded.

## 12. Reconciliation with workshop docs

The 4-slot design supersedes the 2-slot daughter-PCB described in:

- [`../workshops/03-main-build.md`](../workshops/03-main-build.md) — BOM line "Workshop daughter-PCB (CC1101 socket + spare radio header + USB-A breakout) ... $5" needs the price bump to $8 and the description update to "4-slot radio header board (this doc)"
- [`../workshops/04-radio-applications.md`](../workshops/04-radio-applications.md) — SPI bus map table is now stale on three rows:
  - `CE1 (GPIO 7) = CC1101 CS` ✓ unchanged
  - `GPIO 25 = CC1101 GDO0` → **NOW GPIO 5** (moved to free GPIO 25 for Slot C RESET, Adafruit-compatible)
  - `GPIO 24 = CC1101 GDO2` → **NOW GPIO 6** (moved to free GPIO 24 for Slot C DIO2)
  - "Spare radio header" pinout table needs replacement with §5.3 above
  - Compatible modules table grows by RFM95/69 (Slot B) and nRF24L01+ (Slot D)

Workshop reconciliation is a follow-up commit, NOT folded into this design doc commit. The workshops were written assuming the older 2-slot board; updating them is a separate scope question (does the workshop add the new radio demos? do we keep a "minimum kit" variant with only the CC1101 slot populated? etc.). Flagged for a separate decision.

## 13. References

Upstream sources cited in this document — links current as of 2026-05-20.

- [Adafruit LoRa Radio Bonnet for Raspberry Pi — pinout guide](https://learn.adafruit.com/adafruit-radio-bonnets/pinouts) — authoritative for the Slot C / Adafruit-compatible pin map (CE1, GPIO 25 RESET, GPIO 22 DIO0, GPIO 23 DIO1, GPIO 24 DIO2)
- [LSatan/SmartRC-CC1101-Driver-Lib](https://github.com/LSatan/SmartRC-CC1101-Driver-Lib) — CC1101 driver, canonical hardware-wiring table for the 1×8 module variant; full README copied to `refs/SmartRC-CC1101-README.md`
- [Adafruit_CircuitPython_RFM9x](https://github.com/adafruit/Adafruit_CircuitPython_RFM9x) — RFM95W/LoRa driver, default pin map
- [Adafruit_CircuitPython_RFM69](https://github.com/adafruit/Adafruit_CircuitPython_RFM69) — RFM69HCW driver, default pin map
- [Adafruit_CircuitPython_NRF24L01](https://github.com/2bndy5/CircuitPython_nRF24L01) — nRF24L01+ Python driver
- [Ebyte E07-M1101D-TH product page](https://www.cdebyte.com/products/E07-M1101D-TH) — CC1101 module datasheet, mechanical drawing, electrical specs
- [HopeRF RFM95W datasheet](https://www.hoperf.com/modules/lora/RFM95.html) — 16-pin SMD castellated footprint, electrical & RF specs
- [Nordic nRF24L01+ Product Spec v1.0](https://www.nordicsemi.com/Products/nRF24L01P) — register map, pinout, current draw
- [`../05-networking-radio.md`](../05-networking-radio.md) — full radio buyer's guide for the cyberdeck project; LoRa band / Meshtastic context
- [`../workshops/03-main-build.md`](../workshops/03-main-build.md) — workshop that uses this board as the deck's radio infrastructure
- [`../workshops/04-radio-applications.md`](../workshops/04-radio-applications.md) — workshop using the radios this board exposes
- [`../bb20/BBQ20-DAUGHTERBOARD.md`](../bb20/BBQ20-DAUGHTERBOARD.md) — the BBQ20 keyboard carrier design doc, this board's sister deliverable

## 14. Status

- 2026-05-20: design doc v1 published. KiCad project not yet scaffolded; gerbers / pick-and-place not yet generated. Reviewable for design choices before any board is sent for fab.
- Pending: KiCad schematic + PCB layout, BOM CSV for JLCPCB upload, workshop doc reconciliation, photos / hero render for the project README.
