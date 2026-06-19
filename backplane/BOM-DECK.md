# Deck BOM — A7S Cyberdeck (full system)

Everything to build the whole deck around the A7S. The **backplane shield** is one line here;
its own parts are in **[BOM-SHIELD.md](./BOM-SHIELD.md)**.

- **No prices** — parts list to start sourcing from.
- **Sourcing links are options for review, not picks.** They point at searches or canonical
  product pages so a human can choose the exact item.

## Core compute

| Item | Spec / notes | Qty | Sourcing options |
|---|---|--:|---|
| Radxa Cubie A7S | Allwinner A733 SBC (the host) | 1 | [Radxa](https://radxa.com/products/cubie/a7s/) · [Allnet/Arace distributors](https://www.google.com/search?q=Radxa+Cubie+A7S+buy) |
| Boot storage | microSD (A1/A2) **or** NVMe SSD (M.2 2230/2242 via the A7S FPC) | 1 | microSD: [Amazon](https://www.amazon.com/s?k=A2+microSD+card) · NVMe: [Amazon](https://www.amazon.com/s?k=M.2+2242+NVMe+SSD) |

## Power

| Item | Spec / notes | Qty | Sourcing options |
|---|---|--:|---|
| USB-C power bank / battery | Powers the A7S via its **power-only USB-C** port; shield taps 5V/3V3 from the header | 1 | [Amazon](https://www.amazon.com/s?k=USB-C+power+bank+PD) |
| USB-C cable | Power feed to the A7S | 1 | [Amazon](https://www.amazon.com/s?k=USB-C+cable) |

> No separate shield battery — all shield power comes through the A7S header.

## The shield

| Item | Spec / notes | Qty | Sourcing |
|---|---|--:|---|
| A7S Cyberdeck Backplane | Built per **[BOM-SHIELD.md](./BOM-SHIELD.md)** | 1 | this project |

## Radio modules (swappable — up to 2 at once)

| Item | Band / type | Qty | Sourcing options |
|---|---|--:|---|
| nRF24L01+ | 2.4 GHz transceiver (anchor pinout) | 0–2 | [Amazon](https://www.amazon.com/s?k=nRF24L01+module) · [AliExpress](https://www.aliexpress.com/w/wholesale-nRF24L01.html) |
| nRF24L01+PA+LNA (SMA) | 2.4 GHz long-range | 0–2 | [Amazon](https://www.amazon.com/s?k=nRF24L01+PA+LNA+SMA) · [AliExpress](https://www.aliexpress.com/w/wholesale-nRF24L01-PA-LNA.html) |
| CC1101 | sub-GHz (433 / 868 / 915 MHz) | 0–2 | [Amazon](https://www.amazon.com/s?k=CC1101+module+spi) · [AliExpress](https://www.aliexpress.com/w/wholesale-CC1101-module.html) |
| CC2500 | 2.4 GHz (CC1101 twin) | 0–2 | [AliExpress](https://www.aliexpress.com/w/wholesale-CC2500-module.html) |
| ESP-01 / ESP-01S *(via AUX + jumpers)* | WiFi (UART) | 0–1 | [Amazon](https://www.amazon.com/s?k=ESP-01S) · [AliExpress](https://www.aliexpress.com/w/wholesale-ESP-01S.html) |
| Antenna + pigtail | for SMA radio variants | as needed | [Amazon](https://www.amazon.com/s?k=2.4GHz+antenna+SMA+pigtail) |

## Off-board inputs (casing-mounted, wired to the shield headers)

| Item | Spec / notes | Connects to | Qty | Sourcing options |
|---|---|---|--:|---|
| Analog thumbstick | 2-axis + push (PSP-style breakout) | J8 (1×5) | 1 | [Amazon](https://www.amazon.com/s?k=PSP+analog+joystick+breakout+module) · [AliExpress](https://www.aliexpress.com/w/wholesale-joystick-breakout-module.html) |
| Rotary encoder | EC11 with push switch | J10 (1×4) | 1 | [Amazon](https://www.amazon.com/s?k=EC11+rotary+encoder+module) · [LCSC](https://www.lcsc.com/search?q=EC11%20rotary%20encoder) |
| Tactile buttons (aux 5/6) | off-board, your choice of cap | J11 (1×4) | 2 | [Amazon](https://www.amazon.com/s?k=tactile+push+button) · [LCSC](https://www.lcsc.com/search?q=tactile%20switch) |

## Prototyping (optional, per design intent)

| Item | Spec / notes | Qty | Sourcing options |
|---|---|--:|---|
| Mini solderless breadboard | casing-mounted, for UART/jumper modules off the AUX/breakout pins | 1–2 | [Amazon](https://www.amazon.com/s?k=mini+solderless+breadboard+170) |

## Enclosure & mechanical

| Item | Spec / notes | Qty | Sourcing options |
|---|---|--:|---|
| Chassis / enclosure | 3D-printed cyberdeck shell or case (your design) | 1 | [Cyberdeck designs](https://www.google.com/search?q=cyberdeck+3d+print+stl) · see repo `06-chassis-and-prebuilt.md` |
| Standoffs + screws | M2.5 (shield ↔ A7S, 43.8 mm hole square) | 1 kit | [Amazon](https://www.amazon.com/s?k=M2.5+nylon+standoff+kit) |
| Display mount / bezel | for the 2.8" TFT | 1 | printed / [Amazon](https://www.amazon.com/s?k=2.8+inch+TFT+bezel) |

## Wiring & consumables

| Item | Spec / notes | Qty | Sourcing options |
|---|---|--:|---|
| Hookup wire | 24–28 AWG silicone, stranded | 1 set | [Amazon](https://www.amazon.com/s?k=24+AWG+silicone+hookup+wire+kit) |
| Heat-shrink / Dupont jumpers | as needed for off-board parts | 1 set | [Amazon](https://www.amazon.com/s?k=heat+shrink+assortment) · [Dupont jumpers](https://www.amazon.com/s?k=dupont+jumper+wire) |
