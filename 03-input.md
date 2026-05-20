# The 2026 Cyberdeck Input-Device Buyer's Guide

A cyberdeck lives or dies by its input. The chassis dictates how much keyboard real estate you have, the build philosophy dictates how much rework you'll tolerate, and the pointing device often decides whether the deck is a desk-only "field-luggable" or a true lap-and-knee daily driver. This guide covers eight categories of input hardware that show up most often in 2026 cyberdeck builds, with current street prices, footprints, and the integration tradeoffs that matter when you're stuffing a keeb into a 3D-printed shell next to a Raspberry Pi 5 or Framework mainboard.

## How to Choose

**Form factor tradeoffs.** A 60% (e.g., RK61, Anne Pro 2) is the safest starting point: arrow-key muscle memory still works via Fn layers, and the unit fits in most laptop-class decks. A 40% (Planck, Vortex Core, NIU Mini) buys ~25% chassis depth back but forces a multi-layer learning curve of two to four weeks before you regain pre-deck WPM. Ortholinear and ortho-staggered layouts (Planck, Preonic, NIU40) pack rectangularly into tight cases far better than staggered rows — that's why they're disproportionately represented in handheld builds. Split keyboards (Corne, Sofle, Glove80) are fantastic ergonomics but rarely fit a single-shell deck; you typically run them tethered externally or design a clamshell that opens to two halves. A Kinesis Advantage360 or Moonlander is almost never inside a cyberdeck — it *is* the cyberdeck's external dock.

**Wired vs wireless in metal enclosures.** Aluminum, steel, and even carbon-fiber shells will brutally attenuate 2.4 GHz and Bluetooth radios. If you must go wireless inside a metal chassis, plan an antenna cutout (a plastic or acrylic window), route a u.FL pigtail to an external SMA, or simply choose wired. Many builders run TRRS/USB-C between the deck's internal MCU and the host SBC over a short cable — wired is also lower latency and avoids the [8 kHz polling vs battery-life tradeoff](https://mechkeys.com/blogs/news/keychron-expands-mechanical-keyboard-lineup-with-q-ultra-and-v-ultra-series-at-ces-2026) that Keychron and others now advertise.

**QMK / VIA / ZMK matters more in a deck than at a desk.** When you have 40–60 keys and no row of F-keys, layering becomes the only way to reach the full ASCII space, much less media controls and window management. [QMK](https://qmk.fm) is mature, C-based, and the default for AVR/RP2040. [VIA](https://www.caniusevia.com) is the GUI overlay that lets you remap without recompiling. [ZMK](https://zmk.dev) is the dominant choice for wireless splits using Nordic nRF52840. [KMK](https://github.com/KMKfw/kmk_firmware) is the CircuitPython alternative — slightly heavier but lets you script in Python on the keyboard itself.

**Pointing-device integration is the hard part.** Trackballs and trackpads consume volume disproportionate to their surface area. The cleanest integrations are (a) a Cirque 35 mm/40 mm pad embedded into the right-thumb area of a custom PCB; (b) a salvaged ThinkPad TrackPoint nub wired into a custom controller; or (c) a Ploopy Nano PCB inset under a domed shell. Avoid full-size desktop trackballs inside a deck — keep those external.

**TrackPoint salvage workflow.** Strip a ThinkPad X220, T420, T430, or T460 keyboard FFC ribbon, breakout the sensor with [a custom carrier PCB](https://github.com/alonswartz/trackpoint-extended-mod), and feed PS/2 data into a microcontroller running QMK with the [`PS2_MOUSE_ENABLE`](https://docs.qmk.fm/#/feature_ps2_mouse) feature. The T430-era cap is the community favorite for feel; X220-era is more compact. Expect 4–8 hours of soldering and firmware tweaking, but the result is a buttonless pointing device that costs $5–15 in donor parts.

---

## 1. Off-the-Shelf Compact Mechanical Keyboards

| Model | Price (USD 2026) | Layout | Switches | Wireless | QMK/VIA | Footprint |
|---|---|---|---|---|---|---|
| [Vortex Core / Core Plus](https://vortexgear.store/products/core-plus) | $119–$129 | 40% (47–50 keys) | Cherry MX / Kailh low-profile | BT (Plus only) | Proprietary firmware, layers via Fn | ~245 × 95 mm |
| [Vortexgear Race 3](https://www.amazon.com/Mechanical-Keyboard-Vortexgear-Mx-Brown-Aluminium/dp/B071J5WTT6) | $129–$159 | 75% | Cherry MX | Wired | Proprietary, programmable | ~339 × 124 mm |
| Planck EZ | EOL 2023, ~$200–$300 used | 40% ortho | Kailh hot-swap | Wired | [QMK/Oryx](https://configure.zsa.io) | ~235 × 89 mm |
| [Preonic MX Kit V3](https://olkb.com/collections/preonic) | $220–$300 (with caps/switches) | 50% ortho | hot-swap MX | Wired | QMK/VIA | ~245 × 109 mm |
| NIU Mini 40 (KBDfans) | $90–$130 when in stock | 40% ortho | Soldered MX | Wired | QMK/VIA | ~230 × 90 mm |
| [GMMK Compact / GMMK 2 65%](https://www.bestbuy.com/site/glorious-gmmk-prebuilt-rgb-compact-wired-mechanical-keyboard-black/6519212.p) | $110–$140 | 60% / 65% | Glorious hot-swap | Wired | QMK on GMMK 2 | ~295 × 105 mm |
| [Keychron K2 / K7 Max](https://www.keychron.com/collections/mini-keyboards) | $100–$160 | 75% / 65% | Gateron hot-swap | BT + 2.4 GHz | QMK/VIA on Max line | ~306 × 124 mm |
| [Keychron Q1/Q3/Q6 Ultra (2026)](https://mechkeys.com/blogs/news/keychron-expands-mechanical-keyboard-lineup-with-q-ultra-and-v-ultra-series-at-ces-2026) | $229.99–$239.99 | 75% / TKL / full | Gateron hot-swap | 2.4 GHz 8 kHz + BT | QMK/VIA | varies |
| [RK Royal Kludge RK61 / RK68](https://www.amazon.com/RK-ROYAL-KLUDGE-Stand-Alone-Hot-Swappable/dp/B08G52MB1J) | $40–$70 | 60% / 65% | Hot-swap | BT + 2.4 GHz | QMK/VIA (RK61 wired Pro) | ~293 × 102 mm |
| Anne Pro 2 | $80–$110 (Obinslab) | 60% | Gateron / Kailh BOX | BT | Proprietary "Obinskit" | ~285 × 100 mm |
| Akko 3061 / 3068 / 3068B | $70–$120 | 60% / 65% | Akko / Cherry / Gateron | Wired or BT (B) | Mostly proprietary | ~295 × 106 mm |
| Ducky One 3 Mini | $109–$129 | 60% | Cherry / Kailh | Wired | Proprietary (DIP layers) | ~302 × 108 mm |
| Magicforce 68 | $45–$70 (mostly EOL) | 65% | Outemu / Gateron | Wired | None | ~316 × 105 mm |
| [HHKB Professional Hybrid Type-S](https://hhkeyboard.us/hhkb/pro-hybrid-type-s) | $299 (sale) / $385 list | 60% HHKB | Topre 45g | BT + USB | DIP switches only | ~294 × 120 mm |

**Pros / cons.** Vortex Core wins the cyberpunk aesthetic crown and is the most-photographed deck keyboard ever, but its proprietary firmware is dated. Royal Kludge is the price/QMK sweet spot under $60. HHKB is the connoisseur pick — topre switches, sane minus-arrow layout — but you'll never love it inside a metal deck because the case is plastic for radio reasons. Keychron Q-line is overbuilt aluminum and probably too heavy for portable decks; reach for K Max or V instead.

---

## 2. Ortholinear / 40%-Class Kits

For builders willing to solder, ortho gives you the tightest possible footprint per usable key.

| Kit | Price (USD 2026) | Layout | Switches | QMK/VIA | Notes |
|---|---|---|---|---|---|
| [OLKB Planck Rev 7](https://olkb.com/collections/planck) | $200–$280 (kit with caps) | 4×12 ortho | hot-swap MX | QMK/VIA | The canonical 40%; community is huge |
| OLKB Preonic V3 | $220–$300 | 5×12 ortho | hot-swap MX | QMK/VIA | Extra number row helps the learning curve |
| MNT Pocket Reform keyboard | ~$130 standalone via [shop.mntre.com](https://shop.mntre.com/products/mnt-reform-keyboard-40) | 60-key ortho | Kailh Choc low-profile | QMK | Designed for cyberdeck-class portables; OLED option |
| JJ40 (KPRepublic) | $55–$90 PCB+plate | 4×12 ortho | Soldered MX | QMK | Cheapest entry to a Planck-like build |
| BM40 RGB (KPRepublic) | $65–$110 PCB | 4×12 ortho | Soldered or hotswap MX | QMK/VIA | Underglow, AVR-based |
| [KBD8X Mini](https://kbdfans.com) | $180–$240 case+PCB | 75% (not ortho) | Hot-swap MX | QMK/VIA | Heavy aluminum, often a "dock" keyboard |

**Pros / cons.** JJ40/BM40 are the dollar-per-keystroke winners but you commit to soldered switches. The MNT Pocket Reform keyboard is purpose-built for a cyberdeck-class portable and works standalone — the only commercial 60-key ortho with a published low-profile case from a single open-source vendor.

---

## 3. Split Keyboards

Splits rarely fit inside a single-shell deck, but they're the gold standard for ergonomic external pairing or clamshell builds. **Bus / wiring note:** classic Corne/Sofle/Lily58 use TRRS (3.5 mm) between halves with serial or I²C signaling. Modern ZMK splits use BLE pairing between halves (no inter-half cable). When integrating into a deck, leave room for the TRRS jack or design a custom cable run; never bus power and data on USB-Cs that aren't designed for it.

| Kit | Price (USD 2026) | Layout | Switches | Wireless | QMK/VIA/ZMK |
|---|---|---|---|---|---|
| [Corne (CRKBD) hotswap v3/v4](https://www.littlekeyboards.com/products/corne-mx-hotswap-kit) | $90–$160 PCB kit / $180–$260 fully built | 3×6+3 split | MX hotswap or Choc | Wired (TRRS) or wireless variants | QMK/VIA, ZMK |
| Sofle V2 / Aurora Sofle | $120–$220 kit ([splitkb.com](https://splitkb.com/collections/keyboard-kits)) | 6×6+5 with encoders | MX hotswap | Wired | QMK/VIA |
| [Lily58 / Aurora Lily58](https://boardsource.xyz/products/lily58) | $120–$210 kit | 5×6+4 split | MX hotswap | Wired | QMK/VIA, ZMK |
| Iris (Keebio) | $150–$240 kit | 4×6+5 split | MX hotswap | Wired | QMK/VIA |
| ErgoDox EZ | ~$295–$350 | columnar 6+7 thumb cluster | hot-swap | Wired | QMK/Oryx |
| [ZSA Moonlander](https://www.zsa.io/moonlander) | $365 | columnar tented | Kailh hot-swap | Wired | QMK/Oryx |
| [Glove80](https://www.moergo.com) | $370 | concave columnar | Choc low-profile | BT (ZMK) | ZMK |
| Kinesis Advantage360 | $480 | concave bowl | Gateron Brown | BT optional | QMK on the Pro |

**Pros / cons.** Corne is the most popular DIY cyberdeck split because of its tiny footprint and abundant 3D-printable cases. Glove80 is the king of typing comfort but its bowl shape makes it the antithesis of "fits in a deck." ErgoDox/Moonlander remain desk-only — they belong in your home office dock, not on top of a Pelican case.

---

## 4. Ultra-Compact / Handheld

| Device | Price (USD 2026) | Layout | Notes |
|---|---|---|---|
| [Solder Party BBQ20KBD](https://www.tindie.com/products/arturo182/bb-q20-keyboard-with-trackpad-usbi2cpmod/) | $44–$55 | BlackBerry Q20 QWERTY + optical trackpad | USB / I²C / PMOD; the de facto handheld deck keyboard |
| Beepy / Beepberry keyboard | $79–$99 (kit including PiZero carrier) | Same BBQ20 module repackaged | RasPi Zero 2 W cyberdeck reference design |
| [M5Stack CardKB v1.1](https://shop.m5stack.com/products/cardkb-mini-keyboard-programmable-unit-v1-1-mega8a) | $13–$18 | 50-key membrane QWERTY | I²C, ATMega8A; credit-card-size; great for esp32 decks |
| [M5Stack Cardputer v1.1](https://shop.m5stack.com/products/m5stack-cardputer-kit-w-m5stamps3) | $29.90 | 56-key membrane | Self-contained ESP32-S3 computer; lower 160 gf actuation in 2026 refresh |
| TG3 mil-spec membrane (e.g., CK-82) | $250–$600 | Compact membrane | Sealed, sunlight-readable; appears in field deck builds |
| GameSir handheld pads (G7/X4 etc.) | $40–$110 | Gamepad + on-screen text | Not a keyboard per se; pairs with virtual KB |
| Adafruit Cardputer / Macropad RP2040 keypads | $35–$80 | 4×4 / 3×4 macro | Augments a touch deck with physical keys |

**Pros / cons.** BBQ20KBD is the answer for true pocket-class decks — hardware trackpad on-board, USB-HID with no driver, and trivial I²C integration with a CircuitPython host. CardKB is unbeatable per dollar but lacks a pointing device. Skip TG3 unless rugged certification is actually load-bearing.

---

## 5. Pointing Devices

| Device | Price (USD 2026) | Type | Wireless | Open / QMK |
|---|---|---|---|---|
| [Ploopy Adept Trackball](https://ploopy.co/shop/adept-trackball-fully-assembled/) | $79–$84 USD assembled | 44 mm finger trackball | Wired (BT model exists) | Open hardware, QMK |
| [Ploopy Nano 2](https://ploopy.co/shop/nano-2-trackball/) | $52–$57 USD | tiny finger trackball | Wired | Open / QMK |
| Ploopy Classic | $129–$149 | Palm trackball (Kensington Expert-style) | Wired | Open / QMK |
| Ploopy Mini | $89–$99 | Thumb-operated | Wired | Open / QMK |
| Kensington SlimBlade Pro | ~$100 | 55 mm palm | BT/2.4 GHz | Driver only |
| Kensington Expert Mouse | $90–$110 | 55 mm palm | Wired/wireless variants | Driver only |
| Kensington Orbit | $40–$60 | 40 mm finger | Wired | Driver only |
| [Logitech ERGO M575 / M575S](https://www.logitech.com/en-us/shop/p/m575-ergo-wireless-trackball) | $49.99 | Thumb | BT + Logi receiver | Driver only |
| Logitech MX Ergo (S) | $99.99–$119 | Thumb tilted | BT + receiver | Logi Options+ |
| Elecom HUGE / HUGE Plus | $79–$110 | 52 mm index-finger | 2.4 GHz / BT (Plus) | Driver only |
| Elecom Bitra | $59–$80 | Tiny travel index-finger | BT or 2.4 GHz | Driver only |
| Sanwa Supply trackballs (MA-TB44/45) | $40–$80 (import) | Small thumb/index | Wired/BT | Driver only |
| ThinkPad TrackPoint salvage (X220/T430 FRU) | $5–$15 donor + custom PCB | Nub | n/a | QMK PS/2 driver |
| [Tex Yoda II](https://drop.com/buy/tex-yoda-ii-mechanical-keyboard-kit) | $280–$399 | TrackPoint in 60% MX board | Wired | QMK |
| FrogPad / TrackPoint adapter boards (e.g., 33buttons) | $25–$60 | Carrier PCB only | n/a | QMK |
| [Cirque GlidePoint 35 mm / 40 mm trackpad](https://www.cirque.com/glidepoint-circle-trackpads) | $25–$45 per pad / $99 Gen6 dev kit | Capacitive touchpad | I²C/SPI/USB | QMK has driver |
| Synaptics laptop trackpad salvage | free–$10 | PS/2 or SMBus | n/a | Painful; rarely worth it |

**Pros / cons.** Ploopy Nano 2 is the cyberdeck pointing-device default — small enough to embed, fully QMK-aware, and its firmware lives in the same codebase as your keyboard. Cirque pads are the cleanest *integrated* option for a custom PCB. A TrackPoint salvage is the highest-effort/highest-cool result. Avoid embedding any palm trackball inside a deck — they're external dock peripherals.

---

## 6. DIY Keyboard Components for Integration

| Component | Typical 2026 Price | Notes |
|---|---|---|
| Cherry MX2A Red/Brown/Blue | $0.30–$0.55 per switch | Stratified by tier — Core is the bargain MX2A |
| Gateron Pro / Oil King / Yellow | $0.20–$0.45/switch | ~30–40% cheaper than Cherry, often smoother out of box |
| Kailh BOX, Speed, Polia | $0.30–$0.70/switch | BOX White is a clicky favorite |
| Outemu (budget) | $0.10–$0.20/switch | Acceptable for prototypes; replace before shipping a hero build |
| [Kailh Choc V1 low-profile](https://www.kailh.net/products/kailh-switch-set) | $0.45–$0.65/switch | The standard for low-profile cyberdeck builds; 3.0 mm travel |
| Kailh Choc V2 / Sunset | $0.55–$0.90/switch | MX-compatible stems, lower profile, fewer keycap options |
| MX hotswap PCBs (Kailh sockets) | sockets $4–$8/100 | Almost always worth it — hotswap is non-negotiable in a deck |
| Pro Micro (ATmega32U4) clone | $5–$12 | Original keyboard MCU; 28 KB flash — becoming tight for modern QMK |
| [Elite-Pi (RP2040)](https://keeb.io/products/elite-pi-usb-c-pro-micro-replacement-rp2040) | $15–$20 | Drop-in Pro Micro replacement, 2 MB flash, USB-C |
| Elite-C | $20–$28 | ATmega32U4 with USB-C; legacy compatibility |
| Raw RP2040 / Adafruit KB2040 | $5–$15 | DIY-friendly, runs QMK/KMK |
| Nice!Nano (nRF52840) | $25–$35 | The ZMK wireless standard |
| Seeed XIAO BLE / nRF52840 | $10–$15 | Cheapest ZMK option |

**Firmware notes.** [QMK](https://qmk.fm) is the bedrock — write in C, flash via dfu-util. [VIA](https://www.caniusevia.com) is the runtime layout editor; if you build, make sure your `keyboard.json` includes a VIA definition. [ZMK](https://zmk.dev) is mandatory for wireless splits — its low-power-aware C/devicetree pipeline runs on Nordic chips, supports BLE 5.x, and is rapidly closing the feature gap with QMK. [KMK](https://github.com/KMKfw/kmk_firmware) is the CircuitPython firmware — pick it if you want to live-edit on the keyboard's USB drive.

---

## 7. Niche / Themed Inputs

| Device | Price (USD 2026) | Notes |
|---|---|---|
| IBM Model M Space Saver (1391472 / 1392464 vintage) | $200–$600 used (collector market) | Iconic, *loud*, buckling springs; needs a USB Soarer's Converter or a Hagstrom KE-USB36 |
| Unicomp Mini M (modern Model M) | ~$104–$129 | Buckling springs, current production, USB |
| [Topre Realforce R3S](https://mechanicalkeyboards.com/products/topre-realforce-r3s-tkl-wired) | $155.99–$180 | Topre electrocapacitive, slim form, USB |
| [iKey SLK-101 / PM-81](https://ikey.com/collections/keyboards) | $250–$900+ | Mil-spec rugged, sealed silicone, IP-rated |
| Hope Industrial / Stealth panel keyboards | $400–$1200+ | Panel-mount industrial; for "true field" decks |
| [CharaChorder One](https://www.charachorder.com) | $249 ($199–$211 with code) | 3D switch chording; 250+ WPM potential after weeks of practice |
| [CharaChorder Lite](https://www.amazon.com/CharaChorder-Lite/dp/B0BW2LD8SL) | $169–$199 | Familiar split layout with chording layered in |
| [Twiddler 3](https://www.amazon.com/Twiddler3-Chording-Keyboard-Bluetooth-Rechargeable/dp/B0CD2XG7Q7) | $199 (often discounted) | One-handed chorded; BT + USB |
| [Twiddler 4](https://www.mytwiddler.com/) | $229–$269 | Replaces joystick with optical trackpad; USB-C |

**Pros / cons.** Model M boards are loud enough to disqualify themselves from any portable deck — they're for stationary "battle station" builds. Realforce R3S is the cyberpunk-aesthetic Topre option that doesn't need an SBC to read its protocol. CharaChorder is for the obsessive — wonderful in theory, learning curve in months. Twiddler is the one-handed pick for sci-fi handheld decks.

---

## 8. Touchscreen / Virtual Input

When the deck has a touchscreen (Waveshare, Pimoroni HyperPixel, Raspberry Pi Touch Display, a salvaged Surface panel) you may be able to skip a physical keyboard entirely — at the cost of typing speed.

| Stack | Cost | Notes |
|---|---|---|
| [Steam Deck virtual keyboard](https://store.steampowered.com/steamdeck) (SteamOS) | n/a (included) | Gamepad-driven on-screen KB; works surprisingly well with thumbsticks |
| [Onboard](https://launchpad.net/onboard) for Linux | free | The classic accessibility OSK; lives in any X11/Wayland deck running GNOME or XFCE |
| [Squeekboard](https://gitlab.gnome.org/World/Phosh/squeekboard) | free | Wayland-native, used by Phosh/PinePhone; better for touch decks |
| GNOME on-screen keyboard / KDE Virtual Keyboard | free | Built-in to most distros |
| Wlroots `wvkbd` | free | Minimalist Wayland OSK for tiling-wm decks |
| Florence | free | Hands-free options (dwell-click) for accessibility builds |
| Steam Input + GameSir / 8BitDo Pro 2 | $40–$50 controller | Pair a gamepad with Steam Input's "Mode shift" for chorded text entry |

**Pros / cons.** Virtual keyboards win on chassis space and lose on speed; budget ~20 WPM with a thumbstick on-screen keyboard versus ~70+ WPM on a physical 40%. The best touchscreen-only decks pair an OSK with a physical macropad (Adafruit Macropad RP2040 or a 3×4 QMK board) for the half-dozen keystrokes you need most often. If you're going OSK-only, design a kickstand: holding a deck and tapping a virtual keyboard with two thumbs only works ergonomically when the device sits at ~30°.

---

## Final Buyer's Cheat Sheet

- **Cheapest viable deck keeb under $60:** RK Royal Kludge RK61 (60%, hot-swap, BT).
- **Best handheld:** Solder Party BBQ20KBD or M5Stack Cardputer.
- **Best ortho for tight chassis:** OLKB Planck Rev 7 or a JJ40 if you're soldering.
- **Best 40% aesthetic flex:** Vortex Core Plus.
- **Best pointing device for embedding:** Ploopy Nano 2 (open hardware, QMK).
- **Best touchpad for integration:** Cirque 35 mm GlidePoint module.
- **Best splurge:** HHKB Hybrid Type-S or Topre Realforce R3S.
- **Best ergonomic external dock for the deck:** ZSA Moonlander or Glove80.
- **Most cyberpunk for the dollar:** A TrackPoint-salvaged Corne running QMK on an Elite-Pi.

---

## Sources

### Off-the-Shelf Compact Keyboards
- [Vortex Core / Core Plus](https://vortexgear.store/products/core-plus) · [Vortexgear Race 3 (Amazon)](https://www.amazon.com/Mechanical-Keyboard-Vortexgear-Mx-Brown-Aluminium/dp/B071J5WTT6)
- [GMMK Compact (Best Buy)](https://www.bestbuy.com/site/glorious-gmmk-prebuilt-rgb-compact-wired-mechanical-keyboard-black/6519212.p)
- [Keychron mini lineup](https://www.keychron.com/collections/mini-keyboards) · [Keychron Q/V Ultra CES 2026 release](https://mechkeys.com/blogs/news/keychron-expands-mechanical-keyboard-lineup-with-q-ultra-and-v-ultra-series-at-ces-2026)
- [RK Royal Kludge RK61 (Amazon)](https://www.amazon.com/RK-ROYAL-KLUDGE-Stand-Alone-Hot-Swappable/dp/B08G52MB1J)
- [HHKB Professional Hybrid Type-S](https://hhkeyboard.us/hhkb/pro-hybrid-type-s)

### Ortholinear / 40%-Class Kits
- [OLKB Planck Rev 7](https://olkb.com/collections/planck) · [OLKB Preonic V3](https://olkb.com/collections/preonic)
- [MNT Pocket Reform Keyboard 40](https://shop.mntre.com/products/mnt-reform-keyboard-40)
- [KBDfans (KBD8X Mini)](https://kbdfans.com)

### Split Keyboards
- [Corne (CRKBD) hotswap kit](https://www.littlekeyboards.com/products/corne-mx-hotswap-kit) · [splitkb.com kits (Sofle, Aurora)](https://splitkb.com/collections/keyboard-kits) · [Lily58 / Aurora Lily58](https://boardsource.xyz/products/lily58)
- [ZSA Moonlander](https://www.zsa.io/moonlander) · [QMK/Oryx configurator](https://configure.zsa.io)
- [Glove80 (MoErgo)](https://www.moergo.com)

### Ultra-Compact / Handheld
- [Solder Party BBQ20KBD (Tindie)](https://www.tindie.com/products/arturo182/bb-q20-keyboard-with-trackpad-usbi2cpmod/)
- [M5Stack CardKB v1.1](https://shop.m5stack.com/products/cardkb-mini-keyboard-programmable-unit-v1-1-mega8a) · [M5Stack Cardputer v1.1](https://shop.m5stack.com/products/m5stack-cardputer-kit-w-m5stamps3)

### Pointing Devices
- [Ploopy Adept Trackball](https://ploopy.co/shop/adept-trackball-fully-assembled/) · [Ploopy Nano 2](https://ploopy.co/shop/nano-2-trackball/)
- [Logitech ERGO M575 / M575S](https://www.logitech.com/en-us/shop/p/m575-ergo-wireless-trackball)
- [Cirque GlidePoint Circle trackpads](https://www.cirque.com/glidepoint-circle-trackpads)
- [Tex Yoda II (Drop)](https://drop.com/buy/tex-yoda-ii-mechanical-keyboard-kit)
- [TrackPoint extended-mod carrier PCB (GitHub)](https://github.com/alonswartz/trackpoint-extended-mod) · [QMK PS2_MOUSE_ENABLE docs](https://docs.qmk.fm/#/feature_ps2_mouse)

### DIY Components / MCUs / Firmware
- [Kailh switch product set](https://www.kailh.net/products/kailh-switch-set)
- [Elite-Pi USB-C Pro Micro replacement (Keeb.io)](https://keeb.io/products/elite-pi-usb-c-pro-micro-replacement-rp2040)
- Firmware: [QMK](https://qmk.fm) · [VIA](https://www.caniusevia.com) · [ZMK](https://zmk.dev) · [KMK](https://github.com/KMKfw/kmk_firmware)

### Niche / Themed Inputs
- [Topre Realforce R3S](https://mechanicalkeyboards.com/products/topre-realforce-r3s-tkl-wired)
- [iKey rugged keyboards](https://ikey.com/collections/keyboards)
- [CharaChorder One](https://www.charachorder.com) · [CharaChorder Lite (Amazon)](https://www.amazon.com/CharaChorder-Lite/dp/B0BW2LD8SL)
- [Twiddler 3 (Amazon)](https://www.amazon.com/Twiddler3-Chording-Keyboard-Bluetooth-Rechargeable/dp/B0CD2XG7Q7) · [Twiddler 4](https://www.mytwiddler.com/)

### Touchscreen / Virtual Input
- [Steam Deck virtual keyboard](https://store.steampowered.com/steamdeck)
- [Onboard](https://launchpad.net/onboard) · [Squeekboard (GNOME)](https://gitlab.gnome.org/World/Phosh/squeekboard)
