# Cyberdeck Networking & Radio: 2026 Buyer's Guide

A cyberdeck without RF is just a laptop. This guide covers the wireless gear that defines the category: WiFi auditing, software-defined radio, GPS, mesh radio, cellular, ham, RFID, and the antennas to make it all work. All prices are USD street, approximate Q2 2026.

> **Disclaimer:** This document is informational and not legal advice. Transmit power limits, frequency allocations, and licensing requirements vary by country. Receiving is generally permissive; transmitting on amateur, cellular, or ISM bands typically requires a license or compliance check. Verify your local regulator (FCC, Ofcom, BNetzA, etc.) before keying up.

---

## 1. WiFi Adapters: Monitor Mode & Packet Injection

Chipset matters far more than brand: the same chassis label can ship with different silicon across revisions.

| Model | Chipset | Bands | Interface | Price | Driver Status (Linux 6.x) |
|---|---|---|---|---|---|
| Alfa AWUS036ACH | RTL8812AU | 2.4/5 GHz | USB 3.0 A | ~$50 | Out-of-tree (aircrack-ng/morrownr DKMS) |
| Alfa AWUS036ACHM | MT7610U | 2.4/5 GHz | USB 2.0 A | ~$45 | In-kernel mt76 — works out of box |
| Alfa AWUS036ACM | MT7612U | 2.4/5 GHz | USB 3.0 A | ~$55 | In-kernel mt76 — preferred for AC |
| Alfa AWUS1900 | RTL8814AU | 2.4/5 GHz quad-ant | USB 3.0 A | ~$70 | Out-of-tree DKMS, finicky |
| Alfa AWUS036AXML | MT7921AU | 2.4/5/6 GHz (WiFi 6E) | USB 3.0 C | ~$80–95 | mt7921u in-kernel; injection improving but **still partial** on 6 GHz |
| Panda PAU09 | RT5572 | 2.4/5 GHz | USB 2.0 A | ~$35 | In-kernel rt2800usb — rock solid |
| Panda PAU0F | RTL8812AU | 2.4/5 GHz | USB 3.0 A | ~$40 | Same DKMS story as ACH |
| TP-Link TL-WN722N **v1 ONLY** | Atheros AR9271 | 2.4 GHz | USB 2.0 A | ~$15–25 used | ath9k_htc in-kernel, the classic |
| TP-Link TL-WN722N v2/v3 | RTL8188EUS | 2.4 GHz | USB 2.0 A | ~$10 | **No monitor mode without patched fork — avoid** |
| Comfast CF-958AC | RTL8814AU | 2.4/5 GHz | USB 3.0 A | ~$30–40 | DKMS; cheap RTL8814AU option |
| Comfast CF-953AX / CF-951AX | MT7921AU | WiFi 6E | USB 3.0 C | ~$25–35 | mt7921u; budget AXML alternative |
| Alfa Tube-UNA | MT7612U | 2.4/5 GHz | USB + PoE | $80+ | mt76, for fixed-mount |

**Picks:**
- **Best dual-band workhorse (2026):** Alfa AWUS036ACM — in-kernel, no DKMS pain, proven injection.
- **WiFi 6E:** AWUS036AXML. Driver matured 2024–25; 6 GHz injection still partial.
- **Budget / Pwnagotchi:** TL-WN722N v1 (genuine stock) or PAU09.
- **Avoid:** any "TL-WN722N" not explicitly v1; RTL8814AU unless you tolerate DKMS.

---

## 2. WiFi 6 / 6E / 7 — Internal M.2 Cards

| Model | Chipset | Standard | Interface | Price | Linux |
|---|---|---|---|---|---|
| Intel AX200 | Intel | WiFi 6 (no 6 GHz) | M.2 2230 | ~$15–25 | iwlwifi — monitor 2.4/5 |
| Intel AX210 | Intel | WiFi 6E | M.2 2230 | ~$20–30 | iwlwifi — **6 GHz blocked by regulatory lockout** |
| Intel AX211 | Intel | WiFi 6E (CNVio2) | M.2 2230 | ~$20 | Requires 12th-gen+ Intel host |
| Intel BE200 / BE201 | Intel | WiFi 7 | M.2 2230 | ~$30–45 | iwlwifi 6.6+; AMD BIOS quirks |
| MediaTek MT7922 | MediaTek | WiFi 6E | M.2 2230 | ~$15–22 | mt7921e — no 6 GHz lockout |
| MediaTek MT7925 | MediaTek | WiFi 7 | M.2 2230 | ~$25–35 | mt7925e mainlined 6.7+ |
| Qualcomm WCN6855 / NCM865 | Qualcomm | WiFi 6E / 7 | M.2 / PCIe | ~$25–60 | ath11k/ath12k |

**Reality check:** AX210 is everywhere and cheap, but Intel firmware refuses 6 GHz monitor when regulatory domain is UNSET. **MT7922 is the better audit pick in 2026** — same price, more permissive.

---

## 3. Software-Defined Radio (SDR)

| Model | Freq Range | Bandwidth | TX? | Interface | Price | Notes |
|---|---|---|---|---|---|---|
| RTL-SDR Blog V4 | 500 kHz – 1.75 GHz | 2.4 MHz | RX | USB-A | ~$40 (EOL'd) | **Final batch 2026; "V4L Lite" coming** |
| Nooelec NESDR SMArt v5 | 25 MHz – 1.7 GHz | 2.4 MHz | RX | USB-A | ~$35 | RTL2832U, heatsinked |
| HackRF One (genuine) | 1 MHz – 6 GHz | 20 MHz | half-duplex | USB-A | ~$340 | Hacker default; 8-bit ADC |
| HackRF + PortaPack H4M | Same as HackRF | 20 MHz | half-duplex | Standalone | ~$152–165 (clone bundle) | Battery-portable |
| PortaRF (all-in-one) | 1 MHz – 6 GHz | 20 MHz | half-duplex | Standalone | ~$220–285 | Single PCB |
| BladeRF 2.0 micro xA4 | 47 MHz – 6 GHz | 56 MHz, 2×2 MIMO | full duplex | USB 3.0 | ~$520 | 12-bit ADC |
| BladeRF 2.0 micro xA9 | 47 MHz – 6 GHz | 56 MHz | full duplex | USB 3.0 | ~$770 | Larger FPGA |
| LimeSDR Mini 2.0 | 10 MHz – 3.5 GHz | 30.72 MHz | full duplex | USB 3.0 | ~$400 | ECP5 FPGA (open toolchain) |
| Ettus USRP B200mini-i | 70 MHz – 6 GHz | 56 MHz | full duplex | USB 3.0 | ~$985 | GNU Radio first-class |
| Ettus USRP B205mini-i | 70 MHz – 6 GHz | 56 MHz | full duplex | USB 3.0 | ~$1,400 | Larger FPGA than B200mini |
| KrakenSDR | 24 – 1766 MHz | 2.4 MHz ×5 coherent | RX | USB | ~$1,150 | 5-channel DF / passive radar |
| Airspy R2 | 24 – 1800 MHz | 10 MHz | RX | USB | ~$170 | Excellent VHF/UHF dynamic range |
| Airspy HF+ Discovery | 0.5 kHz – 31 / 60–260 MHz | 768 kHz | RX | USB | ~$169 | HF DXing gold standard |
| Airspy Mini | 24 – 1800 MHz | 6 MHz | RX | USB | ~$100 | Compact R2 |
| SDRplay RSP1A | 1 kHz – 2 GHz | 10 MHz | RX | USB | ~$130 | 14-bit, broad coverage |
| SDRplay RSPdx / RSPdx-R2 | 1 kHz – 2 GHz | 10 MHz | RX | USB | ~$235 | HDR mode, BNC + 2× SMA |
| ADALM-PlutoSDR | 70–3.8 GHz (325–6 hack) | 20+ MHz | full duplex | USB | ~$230 | Cheap learning TX/RX |

**Picks:** RTL-SDR V4 + HackRF One covers ~95% of cyberdeck SDR work. KrakenSDR if you need DF. Airspy HF+ for HF.

---

## 4. GPS / GNSS

| Model | Constellations | Interface | Price | Notes |
|---|---|---|---|---|
| u-blox NEO-6M (clone) | GPS only | UART | ~$5–8 | Slow cold-fix |
| u-blox NEO-M8N | GPS+GLONASS+Galileo+BeiDou | UART/I²C | ~$25–40 | Meshtastic-favorite |
| u-blox NEO-M9N | 4 concurrent | UART/I²C | ~$70–100 | Better urban canyons |
| u-blox ZED-F9P | Multi-band L1/L2 RTK | UART/USB/SPI | ~$220–280 | Centimeter accuracy |
| GlobalSat BU-353-S4 | GPS (SiRF Star IV) | USB-A | ~$30–45 | Plug-and-play `gpsd`, mag-mount |
| GlobalSat BU-353N5 | GPS+GLONASS | USB-A | ~$55 | Newer MediaTek chip |
| Adafruit Ultimate GPS | MTK3339 | UART | ~$30 | PPS pin |
| SparkFun GPS-RTK SMA | ZED-F9P L1/L2 | USB-C/UART/Qwiic | ~$275 | Friendly breakout |
| Garmin GPS 18x LVC/USB | GPS | USB/serial | ~$150 | NMEA + PPS marine puck |

**Indoor caveat:** GPS L1 needs sky view. Plan an external active patch antenna on an SMA bulkhead. Multi-band L1/L5 modules tolerate partial obstructions meaningfully better.

---

## 5. LoRa / Meshtastic

**Frequency bands matter:** 902–928 MHz in US/CA, 863–870 MHz in EU, 433 MHz in much of Asia. Cross-band hardware does not interoperate.

| Model | MCU | Radio | Display | GPS | Battery | Price |
|---|---|---|---|---|---|---|
| Heltec WiFi LoRa 32 V3 | ESP32-S3 | SX1262 | 0.96" OLED | No | LiPo header | ~$20–25 |
| LILYGO T-Beam v1.2 | ESP32 | SX1276/1262 | 0.96" OLED | u-blox NEO-M8N | 18650 | ~$35–45 |
| LILYGO T-Beam Supreme | ESP32-S3 | SX1262 | OLED | NEO-M8N | 18650+I²C | ~$55 |
| LILYGO T-Deck | ESP32-S3 + keyboard | SX1262 | 2.8" LCD | optional | 1500 mAh | ~$60–75 |
| LILYGO T-Deck Plus | ESP32-S3 + keyboard | SX1262 | 2.8" LCD | NEO-6M built-in | 2000 mAh | ~$80–95 |
| RAK WisBlock Starter (RAK4631) | nRF52840 | SX1262 | optional | optional | LiPo | ~$45 |
| WisMesh RAK3312 | ESP32-S3 | SX1262 | optional | optional | LiPo | ~$45 |
| Seeed SenseCAP T1000-E | nRF52840 | LR1110 | e-ink | GNSS | 700 mAh | ~$40 |
| Seeed Station G2 | ESP32-S3 | SX1262 + 35 dBm PA | OLED | yes | 18650 | ~$120 |

**T-Deck** is essentially a complete tiny cyberdeck out of the box — keyboard, screen, LoRa, USB-C, battery.

---

## 6. Cellular Modems

| Model | Standard | Form Factor | Price | Notes |
|---|---|---|---|---|
| Quectel EC25-A/E/AF | LTE Cat-4 | M.2 B-key / USB | ~$60–90 | QMI/MBIM well-supported |
| Quectel EM06-E/A | LTE Cat-6 | M.2 B-key | ~$100–130 | CA-capable |
| Quectel EM7565 | LTE-A Pro Cat-12 | M.2 B-key | ~$140–200 | Sierra "swiss army" |
| Quectel RM500Q-GL | 5G Sub-6 NSA/SA | M.2 B-key | ~$280–400 | RM502Q-AE replacement |
| Quectel RM520N-GL | 5G NR Sub-6 R16 | M.2 B-key | ~$350–500 | Current 5G default |
| Sierra Wireless EM9191 | 5G NR R15 | M.2 | ~$400–600 | Enterprise |
| Sixfab 5G Modem Kit for Pi 5 | 5G | Pi 5 HAT | ~$595 kit / $175 HAT only | RM502 EOL — see new dev kit |
| Sixfab 5G Dev Kit (current) | 5G | Pi HAT | ~$650 | Current path |
| Waveshare SIM7600G-H 4G HAT | LTE Cat-4 + GNSS | Pi HAT | ~$80–110 | GPS included |
| Waveshare RM500Q-GL 5G HAT | 5G Sub-6 | Pi HAT | ~$200 | BYO SIM |

ModemManager/QMI on recent kernels generally Just Works. Three SMA bulkheads needed: main + diversity + GNSS.

---

## 7. Ham Radio Integration

| Model | Type | Bands | Price | Notes |
|---|---|---|---|---|
| Baofeng UV-5R | Analog HT | 2 m / 70 cm | ~$30–37 | CHIRP support |
| Quansheng UV-K5(8) | Analog HT + AM RX | 2 m / 70 cm | ~$25–30 | Open firmware (egzumer) |
| Yaesu FT-65R | Rugged HT | 2 m / 70 cm | ~$110 | Better RX than Baofengs |
| Yaesu FT-4X | Compact HT | 2 m / 70 cm | ~$90 | Yaesu build |
| Kenwood TH-D74A (used) | Tri-band + D-STAR + GPS + APRS | 2 m / 1.25 m / 70 cm | ~$500–700 used | Iconic, EOL |
| Anytone AT-D878UV II Plus | DMR + analog + GPS + BT | 2 m / 70 cm | ~$240 | DMR mainstream |
| TYT MD-UV390 | DMR + analog | 2 m / 70 cm | ~$130 | Budget DMR |

**Sound-card / digital-mode interfaces:**

| Interface | Price | Notes |
|---|---|---|
| Digirig Mobile + cables | $60 + $20–30 | Tiny USB-C; the deck answer |
| SignaLink USB | ~$135 + $25 jumper | Bulkier legacy std |
| Masters Communications RA-series | ~$80 | Mid-tier |
| RT Systems cables | ~$25–40 | CHIRP / programming |

---

## 8. Bluetooth & Short-Range

| Device | Standard | Interface | Price | Use |
|---|---|---|---|---|
| TP-Link UB500 / UB5A | BT 5.0/5.3 | USB-A | ~$10–15 | Cheap host BT |
| Sena UD100 | BT 4.0 class 1 | USB-A | ~$45 | Long-range BT |
| Ubertooth One | BT Classic/LE sniff | USB-A | ~$140 | Only true open BT sniffer |
| nRF52840 USB Dongle | BLE/Thread/Zigbee/802.15.4 | USB-A | ~$10–12 | Sniffle firmware |
| Adafruit nRF52840 Feather | BLE dev | USB-C | ~$25 | Hackable coprocessor |
| ESP32-S3/C5 dev board | BLE + 2.4 GHz | USB-C | ~$10–20 | GATT fuzzers |
| Yardstick One | sub-GHz 300–928 MHz | USB-A | ~$110 | RFCat-based ISM TX/RX |

The nRF52840 USB dongle at $10 with Sniffle is the best BLE auditing buy in 2026.

---

## 9. Antennas & RF Plumbing

| Antenna | Type | Connector | Use | Price |
|---|---|---|---|---|
| Diamond RH771 | Dual-band telescoping | BNC | HT upgrade, RX 100–900 MHz | ~$45 |
| Nagoya NA-771 / NA-771G | Whip dual-band | SMA-M / SMA-F | UV-5R/UV-K5 upgrade | ~$10–15 |
| Nagoya NA-320A | Tri-band whip | SMA | 2 m / 1.25 m / 70 cm | ~$20 |
| Comet SMA Telescoping | Adjustable monopole | SMA | Tune to band on the fly | ~$35 |
| Diamond D-130J Discone | Wideband discone | SO-239 | 25–1300 MHz SDR | ~$130 |
| Sirio SD-1300N | Compact discone | N | Wideband alt | ~$95 |
| Tram 1410 Discone | Discone | UHF-F | Budget | ~$60 |
| Active GPS patch | RHCP L1/L5 | SMA / MCX | External GNSS | ~$15–40 |
| LoRa 915 MHz rubber duck 3 dBi | Monopole | SMA / RP-SMA | Meshtastic | ~$5–10 |
| LoRa 915 fiberglass 5.8 dBi | Collinear | N → SMA | Gateway | ~$45 |
| Discovery Dish | LNB-fed dish | F → SMA | L-band sat (Inmarsat, GOES) | ~$120 |

**Plumbing rules:**
- WiFi gear is **RP-SMA**, SDR/ham is **SMA**. They mate mechanically but don't make RF contact. Mark cables.
- Cellular and M.2 cards use **U.FL / IPEX MHF4** — buy quality pigtails (Taoglas, Sucoflex).
- Chassis bulkheads ~$5–8 each.
- HF on the cheap: long wire + 9:1 unun + SDR direct-sampling input ≈ $20.

---

## 10. Niche & RFID/NFC

| Device | Function | Interface | Price |
|---|---|---|---|
| Proxmark3 RDV4.01 | LF + HF RFID/NFC R/W + sniff | USB-C | ~$350–400 |
| Proxmark3 Easy (clone) | LF + HF, less RAM | USB | ~$70 |
| ChameleonUltra | LF + HF emulator | USB-C + BLE | ~$120 |
| ACR122U | NFC reader PC/SC | USB-A | ~$45 |
| Flipper Zero | Multi-tool sub-GHz/NFC/IR | USB-C + BLE | ~$170 |
| Flipper WiFi Devboard (ESP32-S2) | Marauder copro | GPIO | ~$30 |
| Rabbit-Labs Flipper ESP32-C5 board | CC1101 + GPS + WiFi 6 | GPIO | ~$125 |
| CC1101 SPI module | 300–928 MHz | SPI | ~$3–5 |
| CC1352 LaunchPad | Sub-GHz + 2.4 GHz | USB | ~$30 |
| Hak5 USB Rubber Ducky Mk II | HID injection | USB-A | ~$80 |
| Hak5 Bash Bunny Mk II | HID + storage + serial | USB-A | ~$120 |
| Pi Pico W BadUSB DIY | HID injection | USB | ~$7 |
| OMG cable | WiFi C2 implant cable | USB | ~$120–180 |

---

## How to Choose

### Driver reality on Raspberry Pi OS Bookworm (kernel 6.6+, 2026)

Out-of-box monitor mode, no DKMS gymnastics:
- **MT76xx (mt76 driver):** MT7610U, MT7612U, MT7921AU/U, MT7925 — best in-kernel story.
- **Atheros AR9271 (ath9k_htc):** TL-WN722N v1, still flawless.
- **Ralink RT3070/RT5572 (rt2800usb):** Panda PAU09 — boring/reliable.
- **Realtek RTL8812BU / RTL8821CU:** in-kernel, quality varies.

Out-of-tree DKMS (breaks on kernel updates): **RTL8812AU, RTL8814AU, RTL8821AU** — use aircrack-ng/rtl8812au or morrownr forks.

### Chassis material and RF
Metal blocks RF. Aluminum, steel, copper-mesh — all attenuate heavily. Carbon fiber looks like plastic but is RF-opaque. PETG/PLA shells are RF-transparent. **Plan external antennas via chassis bulkheads from day one.**

### USB port budget
A loaded deck eats ports fast: WiFi audit + SDR + GPS + Digirig + cellular + Flipper + keyboard ≈ 7+ ports. Pi 5 has 4 (2× USB 3.0, 2× USB 2.0); Framework has 4 USB-C. Plan a **powered USB 3 hub** — Alfa adapters and RTL-SDRs draw 400–500 mA peak.

### Regulatory caveats (informational, not legal advice)
- **Receiving** RF is generally legal nearly everywhere; re-broadcasting decoded cellular/police content is generally not.
- **WiFi packet injection** is regulated by TX power and band; do it on networks you own/are authorized to test.
- **Ham bands** require a license to TX.
- **ISM bands (433/868/915 MHz)** have country-specific power and duty-cycle limits. Set Meshtastic region presets correctly.
- **Cellular** — rogue cell experimentation (IMSI catchers) is a felony in most jurisdictions.
- In the US, 902–928 MHz LoRa overlaps the amateur 33 cm band; LoRa users coexist under Part 15.

### Balanced 2026 build
- **Host:** Pi 5 or Framework board with internal **MT7922** card
- **WiFi audit:** Alfa AWUS036ACM on bulkhead RP-SMA
- **SDR:** RTL-SDR Blog V4 + HackRF One (powered hub)
- **GPS:** u-blox NEO-M9N on UART or BU-353-S4 on USB
- **Mesh:** Heltec V3 or LILYGO T-Deck as co-device
- **Cellular:** Quectel EM7565 in M.2 or Sixfab Pi HAT
- **Niche:** Flipper Zero in holster; nRF52840 dongle in back USB
- **Antennas:** Discone top-rail, RH771 stowed, 915 LoRa whip, active GPS patch

Total radio BoM: ~$700–1,200 depending on SDR and whether you go cellular.

---

## Sources

- [WirelesSHack — Best Kali Linux USB adapters 2026](https://www.wirelesshack.org/best-kali-linux-compatible-usb-adapter-dongles.html)
- [morrownr/USB-WiFi](https://github.com/morrownr/USB-WiFi)
- [Intel AX210 monitor mode (Issue #426)](https://github.com/morrownr/USB-WiFi/issues/426)
- [RTL-SDR.com — Blog V4 EOL](https://www.rtl-sdr.com/rtl-sdr-blog-v4-end-of-line/)
- [SDRStore — Best SDR for Beginners 2026](https://www.sdrstore.eu/best-sdr-for-beginners-2026-rtl-sdr-hackrf-plutosdr-usrp-compared/)
- [CNX Software — PortaRF](https://www.cnx-software.com/2026/05/14/portarf-single-board-sdr-mixes-hackrf-one-and-portapack-h4m-hardware-adds-ai-voice-control/)
- [Nuand bladeRF 2.0 micro](https://www.nuand.com/product/bladerf-xa4/)
- [KrakenRF KrakenSDR](https://www.krakenrf.com/product-page/krakensdr)
- [SmartnMagic Meshtastic 2026 guide](https://smartnmagic.com/blogs/solutions/meshtastic-hardware-the-complete-guide)
- [Meshtastic Hardware Docs](https://meshtastic.org/docs/hardware/devices/)
- [Sixfab 5G Modem Kit for Pi 5](https://sixfab.com/product/sixfab-5g-modem-kit-for-raspberry-pi-5/)
- [u-blox ZED-F9P](https://www.u-blox.com/en/product/zed-f9p-module)
- [Digirig Baofeng cables](https://digirig.net/product/baofeng-cables/)
- [Lab401 Proxmark3 RDV4](https://lab401.com/products/proxmark-3-rdv4)
- [Hak5 USB Rubber Ducky](https://shop.hak5.org/products/usb-rubber-ducky)
- [Diamond D-130J](https://www.diamondantenna.net/d130j.html)
