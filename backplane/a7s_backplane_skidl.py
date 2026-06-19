#!/usr/bin/env python3
"""
A7S cyberdeck backplane — SKiDL netlist generator.
Encodes SCHEMATIC.md. Produces a KiCad netlist (a7s_backplane.net).

Run (native, this box):
    skidl-python a7s_backplane_skidl.py        # -> a7s_backplane.net

STATUS: GENERATES CLEAN — 0 errors with skidl 2.2.1 + KiCad 10 symbols (auto-discovered from the nix
store; KICAD8 reader parses the .kicad_sym). Net connectivity validated against SCHEMATIC.md.
Still placeholders for the PLACE/layout stage (not netlist-affecting):
  - U2 = generic 6-pin stand-in for the TPS22918 load switch (pin map 1=VIN 2=GND 3=ON 6=VOUT in
    comments) — swap for a real symbol when assigning footprints.
  - A1 = generic 1x23 for the RP2040-Zero; pins connected by sequential index — set the real
    castellation pin order in the custom footprint `a7s:RP2040_Zero`.
  - Footprints listed are intended assignments; fp-lib-table warning is benign for netlist gen.
"""
import os, glob
from skidl import Part, Pin, Net, generate_netlist, set_default_tool, KICAD8, SKIDL, lib_search_paths

# KiCad 8/9/10 share the .kicad_sym S-expr format; use skidl's KICAD8 reader.
set_default_tool(KICAD8)
_symdir = os.environ.get("KICAD8_SYMBOL_DIR")
if not _symdir or not os.path.exists(os.path.join(_symdir, "Device.kicad_sym")):
    for c in (glob.glob("/nix/store/*kicad-symbols*/share/kicad/symbols")
              + ["/run/current-system/sw/share/kicad/symbols", "/usr/share/kicad/symbols"]):
        if os.path.exists(os.path.join(c, "Device.kicad_sym")):
            _symdir = c; break
if _symdir:
    lib_search_paths["kicad8"].insert(0, _symdir)
    print("symbols:", _symdir)

# ---------- footprint shorthands (THT / hand-solder ONLY — no SMD, no pick-and-place) ----------
RTHT  = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal"
CDISC = "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm"      # 0.1uF / 1uF ceramic disc
CRAD  = "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm"          # 470uF electrolytic
PFUSE = "Fuse:Fuse_Bourns_MF-RG300"                       # radial THT polyfuse

def R(val, ref=None): return Part("Device", "R", ref=ref, value=val, footprint=RTHT)
def C(val, fp=CDISC, ref=None): return Part("Device", "C", ref=ref, value=val, footprint=fp)

# ---------- global power nets ----------
# A7S provides BOTH rails natively on the 30-pin header: pin1/17 = +3V3, pin2/4 = +5V.
# No on-board regulator or load switch (THT/hand-solder, near-passive backplane).
GND       = Net("GND")
V5_IN     = Net("+5V_IN")     # header 5V tap (pins 2/4)
V5        = Net("+5V")        # after polyfuse F1 -> RP2040 + TFT
V3_IN     = Net("+3V3_IN")    # header 3V3 tap (pins 1/17)
V3        = Net("+3V3")       # after polyfuse F2 -> radios / touch / I2C
RP_3V3    = Net("RP_3V3")     # RP2040 onboard 3V3 out -> joystick/encoder refs

# ---------- signal nets ----------
n = lambda s: Net(s)
SPI_SCK, SPI_MOSI, SPI_MISO = n("SPI_SCK"), n("SPI_MOSI"), n("SPI_MISO")
TFT_CS, TFT_DC, TFT_RST, TFT_BL = n("TFT_CS"), n("TFT_DC"), n("TFT_RST"), n("TFT_BL")
TOUCH_CS, TOUCH_IRQ = n("TOUCH_CS"), n("TOUCH_IRQ")
I2C_SDA, I2C_SCK = n("I2C_SDA"), n("I2C_SCK")
UART3_TX, UART3_RX = n("UART3_TX"), n("UART3_RX")
A7S_U2TX, A7S_U2RX = n("A7S_U2TX"), n("A7S_U2RX")   # A7S UART2; RP2040 GP0/GP1 connect directly
R1CS, R1FA, R1FB, R1AUX = n("RADIO1_CS"), n("RADIO1_FLEXA"), n("RADIO1_FLEXB"), n("RADIO1_AUX")
R2CS, R2FA, R2FB, R2AUX = n("RADIO2_CS"), n("RADIO2_FLEXA"), n("RADIO2_FLEXB"), n("RADIO2_AUX")
SPARE0, SPARE1, SPARE2, SPARE3 = n("SPARE0"), n("SPARE1"), n("SPARE2"), n("SPARE3")
BTN1, BTN2, BTN3, BTN4, BTN5, BTN6 = (n(f"BTN{i}") for i in range(1, 7))
JOY_X, JOY_Y, JOY_SW = n("JOY_X"), n("JOY_Y"), n("JOY_SW")
ENC_A, ENC_B, ENC_SW = n("ENC_A"), n("ENC_B"), n("ENC_SW")
CONSOLE_TX, CONSOLE_RX = n("CONSOLE_TX"), n("CONSOLE_RX")

# ---------- A7S host headers ----------
J1 = Part("Connector_Generic", "Conn_02x15_Odd_Even", ref="J1",
          footprint="Connector_PinSocket_2.54mm:PinSocket_2x15_P2.54mm_Vertical")
J2 = Part("Connector_Generic", "Conn_01x15", ref="J2",
          footprint="Connector_PinSocket_2.54mm:PinSocket_1x15_P2.54mm_Vertical")

# J1 (2x15)  — pin:net  (NC pins omitted)
for p, net in {
    1: V3_IN, 2: V5_IN, 3: UART3_RX, 4: V5_IN, 5: UART3_TX, 6: GND,
    7: A7S_U2TX, 8: CONSOLE_TX, 9: GND, 10: CONSOLE_RX, 11: A7S_U2RX,
    14: GND, 16: R1CS, 17: V3_IN, 18: R1FB, 19: SPI_MOSI, 20: GND,
    21: SPI_MISO, 23: SPI_SCK, 24: TFT_CS, 25: GND, 26: TFT_DC,
    27: I2C_SDA, 28: I2C_SCK, 29: TFT_RST, 30: GND,
}.items():
    J1[p] += net

# J2 (1x15)  — PB4 (pin6) was load-switch enable; now a plain spare (no load switch)
for p, net in {
    1: R1FA, 2: TOUCH_CS, 3: TOUCH_IRQ, 4: GND, 5: TFT_BL, 6: SPARE3,
    7: R2FA, 8: R2CS, 9: GND, 10: R2FB, 11: R1AUX, 12: R2AUX,
    13: SPARE0, 14: SPARE1, 15: SPARE2,
}.items():
    J2[p] += net

# ---------- power (THT, near-passive: native A7S rails + polyfuses + bulk/decoupling) ----------
# NO LDO, NO load switch. +3V3 comes straight from the A7S header (pins 1/17).
# SLIM: native A7S rails already have bulk caps; no 470uF electrolytics here, just disc decoupling.
# Self-resetting PPTC polyfuses (no replacement; trip on short, auto-reset on cooldown).
# Same 0.5A-hold part for both rails = single SKU (Bourns MF-R050 / Littelfuse 30R050 / TE RUEF050).
F1 = Part("Device", "Polyfuse", ref="F1", value="MF-R050 0.5A", footprint=PFUSE)   # 5V tap (RP2040+TFT)
F2 = Part("Device", "Polyfuse", ref="F2", value="MF-R050 0.5A", footprint=PFUSE)   # 3V3 tap (radios)
# RP2040-Zero + TFT modules self-decouple onboard -> no on-shield caps for them.
C8 = C("0.1uF"); C9 = C("0.1uF")          # radio1 / radio2 decoupling (bare nRF24/CC1101 benefit)

V5_IN += F1[1]; V5 += F1[2]               # 5V: header -> F1 -> RP2040 + TFT
V3_IN += F2[1]; V3 += F2[2]               # 3V3: header -> F2 -> radios + touch + I2C

# ---------- TFT (J3) ----------
J3 = Part("Connector_Generic", "Conn_01x14", ref="J3",
          footprint="a7s:TFT_2p8")   # real 2.8" landscape body 86x50, header on left edge
for p, net in {
    1: V5, 2: GND, 3: TFT_CS, 4: TFT_RST, 5: TFT_DC, 6: SPI_MOSI, 7: SPI_SCK,
    8: TFT_BL, 10: SPI_SCK, 11: TOUCH_CS, 12: SPI_MOSI, 13: SPI_MISO, 14: TOUCH_IRQ,
}.items():
    J3[p] += net
# J3.9 (SDO) -> no-connect (write-only)

# ---------- radio sockets ----------
def radio(ref, cs, fa, fb):
    global GND, V3, SPI_SCK, SPI_MOSI, SPI_MISO
    J = Part("Connector_Generic", "Conn_02x04_Odd_Even", ref=ref,
             footprint="Connector_PinSocket_2.54mm:PinSocket_2x04_P2.54mm_Vertical")
    GND += J[1]; V3 += J[2]; fa += J[3]; cs += J[4]
    SPI_SCK += J[5]; SPI_MOSI += J[6]; SPI_MISO += J[7]; fb += J[8]
    return J
J5 = radio("J5", R1CS, R1FA, R1FB)
J6 = radio("J6", R2CS, R2FA, R2FB)
J5b = Part("Connector_Generic", "Conn_01x01", ref="J5b", footprint="Connector_Pin:Pin_D1.0mm_L10.0mm")
J6b = Part("Connector_Generic", "Conn_01x01", ref="J6b", footprint="Connector_Pin:Pin_D1.0mm_L10.0mm")
R1AUX += J5b[1]; R2AUX += J6b[1]
V3 += C8[1], C9[1]; GND += C8[2], C9[2]

# ---------- RP2040-Zero (A1) ----------
# Inline part whose PIN NUMBERS == the footprint a7s:RP2040_Zero pad names (5V/GND/3V3/GPnn),
# standard Waveshare pinout. Connect by pad name -> robust, matches the footprint exactly.
RP_PADS = ["5V","GND","3V3","GP29","GP28","GP27","GP26","GP15","GP14",
           "GP0","GP1","GP2","GP3","GP4","GP5","GP6","GP7","GP8",
           "GP9","GP10","GP11","GP12","GP13"]
A1 = Part(tool=SKIDL, name="RP2040_Zero", ref="A1", value="RP2040-Zero",
          footprint="a7s:RP2040_Zero",
          pins=[Pin(num=nm, name=nm, func=Pin.types.PASSIVE) for nm in RP_PADS])
# A1 GP0/GP1 wire DIRECTLY to the A7S UART2 (cross-over): RP TX(GP0)->A7S RX, RP RX(GP1)<-A7S TX.
# No series resistors (3.3V<->3.3V; A7S UART has internal bias). No pull-ups (UART is push-pull).
RP = {"5V": V5, "GND": GND, "3V3": RP_3V3,
      "GP0": A7S_U2RX, "GP1": A7S_U2TX, "GP2": BTN1, "GP3": BTN2, "GP4": BTN3, "GP5": BTN4,
      "GP6": BTN5, "GP7": BTN6, "GP8": JOY_SW, "GP9": ENC_A, "GP10": ENC_B, "GP11": ENC_SW,
      "GP26": JOY_X, "GP27": JOY_Y}
for name, net in RP.items():
    A1[name] += net   # pad name -> net (unused GP pads left open: GP12-15,28,29)

# ---------- buttons SW1-4 (to GND, RP2040 internal pull-ups) ----------
for ref, net in [("SW1", BTN1), ("SW2", BTN2), ("SW3", BTN3), ("SW4", BTN4)]:
    SW = Part("Switch", "SW_Push", ref=ref, footprint="Button_Switch_THT:SW_PUSH_6mm")
    net += SW[1]; GND += SW[2]

# ---------- off-board input SEGMENTS (separate, opposite edges; ambidextrous via 180deg flip) ----------
# Joystick and encoder live on opposite edges of the deck; flipping the whole deck 180deg
# swaps which hand they're on. Each is its own labeled solder segment (NOT one crammed field).
J8 = Part("Connector_Generic", "Conn_01x05", ref="J8", value="JOY",
          footprint="Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical")
for p, net in {1: RP_3V3, 2: GND, 3: JOY_X, 4: JOY_Y, 5: JOY_SW}.items():
    J8[p] += net

J10 = Part("Connector_Generic", "Conn_01x04", ref="J10", value="ENC",
           footprint="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical")
for p, net in {1: ENC_A, 2: ENC_B, 3: ENC_SW, 4: GND}.items():
    J10[p] += net

J11 = Part("Connector_Generic", "Conn_01x03", ref="J11", value="BTN5_6",
           footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical")
for p, net in {1: BTN5, 2: BTN6, 3: GND}.items():
    J11[p] += net

# ---------- I2C: NO external pull-ups ----------
# The A7S enables INTERNAL pull-ups on the TWI pins in its device tree
# (twi2_pins_default { pins="PD16","PD17"; bias-pull-up; }). The I2C bus is available on the
# A7S header (J1 pins 27/28) for breadboard jumpering; no on-board connector or pull-ups needed.

# ---------- Flipper-Zero-compatible 18-pin header (J-FLIP, above the screen) ----------
# Standard Flipper GPIO pinout so Flipper-ecosystem add-ons plug in. Taps existing buses:
# SPI1 (shared) + UART3 (free) + TWI2 (I2C) + the 4 spare A7S GPIO (PG3/4/5, PB4) + power.
# SWD pins (10,12) are Flipper-internal STM32 debug -> NC here. Uses ALL remaining spares.
JF = Part("Connector_Generic", "Conn_01x18", ref="J12", value="FLIPPER",
          footprint="a7s:FLIPPER-GPIO-18")   # Flipper's REAL footprint: 1x8 (pins1-8) + 1x10 (pins9-18), 17.78mm gap
for p, net in {
    1: V5, 2: SPI_MOSI, 3: SPI_MISO, 4: SPARE0, 5: SPI_SCK, 6: SPARE1, 7: SPARE2,
    8: GND, 9: V3, 11: GND, 13: UART3_TX, 14: UART3_RX, 15: I2C_SDA, 16: I2C_SCK,
    17: SPARE3, 18: GND,
}.items():                              # pins 10 (SWC) + 12 (SIO) = NC
    JF[p] += net

# ---------- console test points ----------
TP1 = Part("Connector", "TestPoint", ref="TP1", footprint="TestPoint:TestPoint_Pad_D1.0mm")
TP2 = Part("Connector", "TestPoint", ref="TP2", footprint="TestPoint:TestPoint_Pad_D1.0mm")
CONSOLE_TX += TP1[1]; CONSOLE_RX += TP2[1]

generate_netlist(file_="a7s_backplane.net")
