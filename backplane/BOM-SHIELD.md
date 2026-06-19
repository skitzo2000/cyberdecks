# Shield BOM — A7S Cyberdeck Backplane

Parts to populate the **backplane PCB itself**. Derived from the live netlist
(`a7s_backplane.net`) — all through-hole, no SMD, no ICs, no resistors.

- **No prices here** — this is a parts list to start sourcing from.
- **Sourcing links are options for review, not picks.** Each links a search/category or a
  canonical product page so you can choose the exact part. Confirm pitch, pin count, and
  (for the headers) pin-1 orientation against the board before buying.
- Off-board input *modules* (thumbstick, encoder, aux buttons) and the *radio modules* live in
  the **[deck BOM](./BOM-DECK.md)** — the shield only carries their headers/sockets.

## PCB

| Item | Spec | Qty | Sourcing options |
|---|---|--:|---|
| Backplane PCB | 2-layer, ~86 × 74 mm, THT, custom outline | 1 | [JLCPCB](https://jlcpcb.com/) · [PCBWay](https://www.pcbway.com/) · [OSH Park](https://oshpark.com/) |

## Connectors that mate the A7S

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| J1 | Female header 2×15 (30-pin) | 2.54 mm, THT | 1 | [LCSC](https://www.lcsc.com/search?q=2x15%20female%20header%202.54) · [DigiKey](https://www.digikey.com/en/products/result?keywords=2x15%20female%20header%202.54mm) · [Amazon](https://www.amazon.com/s?k=2x15+female+pin+header+2.54mm) |
| J2 | Female header 1×15 (15-pin) | 2.54 mm, THT | 1 | [LCSC](https://www.lcsc.com/search?q=1x15%20female%20header%202.54) · [DigiKey](https://www.digikey.com/en/products/result?keywords=1x15%20female%20header%202.54mm) · [Amazon](https://www.amazon.com/s?k=1x15+female+pin+header+2.54mm) |

> J1/J2 are the sockets that press onto the A7S male GPIO headers — verify pin length and **pin-1 end** before ordering (see `refs/MECH-DATUMS.md`).

## Radio sockets (the "8+1")

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| J5, J6 | Female header 2×4 (8-pin socket) | 2.54 mm, THT | 2 | [LCSC](https://www.lcsc.com/search?q=2x4%20female%20header%202.54) · [DigiKey](https://www.digikey.com/en/products/result?keywords=2x4%20female%20header%202.54mm) · [Amazon](https://www.amazon.com/s?k=2x4+8pin+female+header+2.54mm) |
| J5b, J6b | Female header 1×1 (AUX / pin 9) | 2.54 mm, THT | 2 | [LCSC](https://www.lcsc.com/search?q=1x1%20female%20header%202.54) · [Amazon](https://www.amazon.com/s?k=single+pin+female+header+2.54mm) |

## Display

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| J3 | 2.8" SPI TFT, ILI9341 + XPT2046 resistive touch | 14-pin SPI module | 1 | [AliExpress](https://www.aliexpress.com/w/wholesale-2.8-inch-SPI-TFT-ILI9341-touch.html) · [Amazon](https://www.amazon.com/s?k=2.8+inch+SPI+TFT+ILI9341+XPT2046+touch) |
| — | Female header 1×14 *(only if socketing the TFT)* | 2.54 mm, THT | 1 | [LCSC](https://www.lcsc.com/search?q=1x14%20female%20header%202.54) · [Amazon](https://www.amazon.com/s?k=1x14+female+header+2.54mm) |

## Input MCU

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| A1 | Waveshare RP2040-Zero | castellated module, soldered | 1 | [Waveshare](https://www.waveshare.com/rp2040-zero.htm) · [Amazon](https://www.amazon.com/s?k=Waveshare+RP2040-Zero) · [AliExpress](https://www.aliexpress.com/w/wholesale-RP2040-Zero.html) |

> Confirm the RP2040-Zero **row spacing (assumed 15.24 mm)** against the footprint before fab.

## On-board buttons

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| SW1–SW4 | Tactile push button, 6 mm | THT, 4-leg | 4 | [LCSC](https://www.lcsc.com/search?q=6mm%20tactile%20switch%20through%20hole) · [DigiKey](https://www.digikey.com/en/products/result?keywords=6mm%20tactile%20switch%20tht) · [Amazon](https://www.amazon.com/s?k=6mm+tactile+push+button+through+hole) |

## Off-board input headers (solder fields — modules in the deck BOM)

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| J8 | Header 1×5 (analog joystick) | 2.54 mm, THT | 1 | [LCSC](https://www.lcsc.com/search?q=1x5%20header%202.54) · [Amazon](https://www.amazon.com/s?k=1x5+pin+header+2.54mm) |
| J10 | Header 1×4 (rotary encoder) | 2.54 mm, THT | 1 | [LCSC](https://www.lcsc.com/search?q=1x4%20header%202.54) · [Amazon](https://www.amazon.com/s?k=1x4+pin+header+2.54mm) |
| J11 | Header 1×4 (aux buttons 5/6) | 2.54 mm, THT | 1 | [LCSC](https://www.lcsc.com/search?q=1x4%20header%202.54) · [Amazon](https://www.amazon.com/s?k=1x4+pin+header+2.54mm) |

> Pick male pins or female sockets to match how you wire the casing-mounted parts.

## Flipper expansion header

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| J12 | Pin header 1×8 + 1×10 (Flipper GPIO, 17.78 mm gap) | 2.54 mm, THT | 1 set | [LCSC](https://www.lcsc.com/search?q=male%20header%202.54%20single%20row) · [DigiKey](https://www.digikey.com/en/products/result?keywords=breakaway%20header%202.54mm) · [Amazon](https://www.amazon.com/s?k=2.54mm+single+row+pin+header+breakaway) |

> Gender (male pins vs female socket) must match your Flipper-ecosystem accessory.

## Passives

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| C1, C2 | Ceramic capacitor, radio 3V3 decoupling (≈0.1 µF; add 1–10 µF if desired) | THT radial (D5 mm) | 2 | [LCSC](https://www.lcsc.com/search?q=0.1uF%20ceramic%20capacitor%20through%20hole) · [DigiKey](https://www.digikey.com/en/products/result?keywords=0.1uF%20ceramic%20capacitor%20radial) |
| F1, F2 | Resettable polyfuse (PPTC), F1 = 5 V rail, F2 = 3V3 rail (≈0.5 A hold — confirm vs radio draw) | THT radial (Bourns MF-R) | 2 | [DigiKey](https://www.digikey.com/en/products/result?keywords=bourns%20MF-R%20polyfuse%20radial) · [Mouser](https://www.mouser.com/c/?q=MF-R%20polyfuse) · [LCSC](https://www.lcsc.com/search?q=PPTC%20resettable%20fuse%20through%20hole) |

## Misc / mechanical

| Ref | Item | Spec / package | Qty | Sourcing options |
|---|---|---|--:|---|
| TP1, TP2 | Test point / 1×1 header (UART console) *(optional)* | 2.54 mm, THT | 2 | [LCSC](https://www.lcsc.com/search?q=test%20point%20pad) · [Amazon](https://www.amazon.com/s?k=PCB+test+point+pin) |
| H1–H4 | M2.5 standoff + screw set (shield ↔ A7S, 43.8 mm square) | nylon/brass | 4 | [Amazon](https://www.amazon.com/s?k=M2.5+standoff+kit) · [DigiKey](https://www.digikey.com/en/products/result?keywords=M2.5%20standoff) |
