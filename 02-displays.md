# Cyberdeck Displays: 2026 Buyer's Guide

The display is arguably the single most defining component of a cyberdeck build. It dictates case footprint, drives a meaningful slice of the power budget, and sets the visual personality of the deck. This guide walks through the 2026 market across seven categories with current street prices, interface notes, and tradeoffs for portable battery-powered builds.

---

## 1. Small Primary LCD/IPS Panels (5"–10")

This is the bread and butter of cyberdeck primary displays — cheap, well-documented interfaces, and bright enough for indoor and shaded-outdoor use.

| Model | Size | Resolution | Interface | Touch | Panel | Brightness | Power | Price (USD, ~2026) |
|---|---|---|---|---|---|---|---|---|
| [Raspberry Pi Touch Display 2 (7")](https://www.raspberrypi.com/products/touch-display-2/) | 7" | 1280×720 | DSI | Cap 5-pt | IPS | ~400 nits | ~2.5 W | **$60** |
| [Raspberry Pi Touch Display 2 (5")](https://www.cnx-software.com/2025/08/18/raspberry-pi-touch-display-2-gets-40-5-inch-variant-with-1280x720-resolution/) | 5" | 1280×720 | DSI | Cap 5-pt | IPS | ~400 nits | ~2 W | **$40** |
| [Waveshare 5" DSI LCD (B)](https://www.waveshare.com/5inch-dsi-lcd-b.htm) | 5" | 800×480 | DSI | Cap 5-pt | IPS | 500 nits | ~1.8 W | **$35–48** |
| [Waveshare 5-DSI-TOUCH-A](https://www.waveshare.com/5-dsi-touch-a.htm) | 5" | 720×1280 | DSI | Cap 5-pt | IPS (alloy case) | 400 nits | ~2.5 W | **~$70** |
| [Waveshare 7" DSI LCD (C)](https://www.waveshare.com/7inch-dsi-lcd-c.htm) | 7" | 1024×600 | DSI | Cap 5-pt | IPS | 350 nits | ~3 W | **$55–70** |
| [Waveshare 7" HDMI LCD (H)](https://www.waveshare.com/7inch-hdmi-lcd-h.htm) | 7" | 1024×600 | HDMI + USB (touch) | Cap 5-pt | IPS | 350 nits | ~3.5 W | **$60–80** |
| [Waveshare 8" 8DP-CAPLCD](https://www.waveshare.com/8dp-caplcd.htm) | 8" | 1280×800 | HDMI + USB | Cap 5-pt | IPS (optical-bonded) | 450 nits | ~4 W | **~$110** |
| [Waveshare 10.1" DSI LCD (C)](https://www.waveshare.com/10.1inch-dsi-lcd-c.htm) | 10.1" | 1280×800 | DSI | Cap 5-pt | IPS | 400 nits | ~5 W | **$85–110** |
| [Waveshare 10.1" HDMI LCD (E)](https://www.amazon.com/waveshare-10-1inch-Capacitive-Compatible-Raspberry/dp/B0BFQH27KB) | 10.1" | 1024×600 | HDMI + USB | Cap 5-pt | IPS optical-bonded | 400 nits | ~5 W | **~$100** |
| [Geekworm 7" 1024×600 IPS](https://geekworm.com/products/raspberry-pi-7-inch-1024x600-ips-capacitive-touch-screen) | 7" | 1024×600 | HDMI + USB | Cap | IPS | 300 nits | ~3 W | **$50–65** |
| [Eviciv 7" RPi Display](https://www.amazon.com/EVICIV-Raspberry-Dual-Speaker-Compatible-Drive-Free/dp/B07L6WT77H) | 7" | 1024×600 | HDMI + microUSB | Cap | IPS, dual speakers | 350 nits | ~3 W | **$60–75** |
| [Elecrow CrowVi 13.3" Touch](https://www.elecrow.com/crowvi-13-3inch-portable-usb-c-monitor-touchscreen.html) | 13.3" | 1920×1080 | USB-C alt-mode + mini-HDMI | Cap 10-pt | IPS | 300 nits | ~7 W | **$150–180** |
| [Elecrow CrowView 14" (laptop extender)](https://www.amazon.com/ELECROW-Extender-Portable-CrowView-Compatible/dp/B0CKN8R6NN) | 14" | 1920×1080 | USB-C alt-mode + mini-HDMI | No | IPS, 72% NTSC | 400 nits | ~6 W | **~$115** |
| [Magedok T101A 10.1"](https://store.magedok.com/products/10-1-inch-2k-ips-qhd-usb-c-capacitive-touch-portable-monitort101a) | 10.1" | 2560×1600 | USB-C alt-mode + mini-HDMI | Cap 10-pt | IPS QHD | ~350 nits | ~8 W | **$169–239** |
| [ASUS ZenScreen Go MB16AHP](https://www.asus.com/us/displays-desktops/monitors/zenscreen/zenscreen-go-mb16ahp/) | 15.6" | 1920×1080 | USB-C + micro-HDMI | No | IPS, 7800 mAh battery | 220 nits | ~7 W | **$240–290** |
| [GeChic On-Lap 1503i](https://www.amazon.com/Gechic-15-6-Inch-Portable-Touchscreen-Monitor/dp/B01M9CXOTV) | 15.6" | 1920×1080 | HDMI + VGA + USB power | Cap 10-pt | IPS | 250 nits | ~7 W | **$300–400** |

**Interface guidance.** For a Raspberry Pi, DSI options give the cleanest install — no HDMI port consumed, no full-size plug protruding, and 1–2 W less than equivalent HDMI panels. The downside is they're Pi-only and often tied to specific Pi generations. HDMI options work with any SBC, mini-PC, or x86 board at the cost of an extra cable plus 5 V USB for backlight/touch. USB-C alt-mode is the cleanest single-cable solution **if your compute board supports DisplayPort alt-mode on USB-C** — Pi 5 does **not**; Framework mainboards, recent NUCs, and most x86 mini-PCs do.

---

## 2. Widescreen / Unusual Aspect Ratios

Bar-shaped panels are why the modern cyberdeck went from "Pelican case with a tablet" to "slim wedge that fits under a keyboard." A 320×1480 strip tucks a usable display into a 1U-tall slab.

| Model | Size | Resolution | Interface | Touch | Panel | Brightness | Power | Price (USD, ~2026) |
|---|---|---|---|---|---|---|---|---|
| [Waveshare 11.9" HDMI LCD](https://www.waveshare.com/11.9inch-hdmi-lcd.htm) | 11.9" stretched | 320×1480 | HDMI + USB | Cap 5-pt | IPS, 6H glass | 300 nits | ~4 W | **$100–125** |
| [Waveshare 11.9" Side Monitor (touch)](https://www.waveshare.com/11.9inch-side-monitor.htm) | 11.9" stretched | 320×1480 | HDMI, alloy case, speakers | Cap optional | IPS | 300 nits | ~5 W | **$130–160** |
| [Waveshare 11.9" DSI LCD](https://www.amazon.com/waveshare-11-9inch-Capacitive-Compatible-DSI/dp/B0B4S8W5GB) | 11.9" stretched | 320×1480 | DSI | Cap 5-pt | IPS | 300 nits | ~3.5 W | **$100–120** |
| [Waveshare 7.9" HDMI LCD](https://www.waveshare.com/7.9inch-hdmi-lcd.htm) | 7.9" stretched | 400×1280 | HDMI + USB | Cap 5-pt | IPS | 300 nits | ~3 W | **$85–100** |
| [Waveshare 7.9" DSI LCD](https://www.waveshare.com/7.9inch-dsi-lcd.htm) | 7.9" stretched | 400×1280 | DSI | Cap 5-pt | IPS | 300 nits | ~3 W | **$80–95** |
| [Waveshare 8.8" Side Monitor](https://www.waveshare.com/8.8inch-side-monitor.htm) | 8.8" bar | 1920×480 | HDMI, HiFi speakers | No | IPS, CNC alloy | 350 nits | ~6 W | **$110–140** |
| [Waveshare 8.8" DSI](https://www.waveshare.com/8.8inch-dsi-lcd.htm) | 8.8" bar | 480×1920 | DSI | Cap 10-pt | IPS optical-bonded | 350 nits | ~5 W | **$110–135** |
| [Waveshare 8.8" USB Monitor](https://www.amazon.com/waveshare-USB-Monitor-Resolution-Secondary/dp/B0D4YTTRVJ) | 8.8" bar | 1920×480 | USB-C secondary (AIDA64/spectrum) | No | IPS | 300 nits | ~5 W | **$90–120** |

**Pros:** the 11.9" 320×1480 is the most popular cyberdeck panel ever shipped — exactly the right width to span a 60% keyboard with room for a working terminal or status pane. Portrait orientation works fine after a single `display_rotate=` line. **Cons:** awkward resolution for traditional desktops; expect to live in `tmux`, dwm, river, sway, or a custom dashboard. Many builders pair one of these with a small secondary OLED rather than running a full DE.

---

## 3. eInk / ePaper Displays

eInk gets you zero idle power and direct-sunlight readability. The downside is refresh rate — even "fast" eInk monitors top out at 15–40 Hz with ghosting.

| Model | Size | Resolution | Interface | Touch | Refresh | Price (USD, ~2026) |
|---|---|---|---|---|---|---|
| [Waveshare 4.2" e-Paper Module](https://www.waveshare.com/epaper) | 4.2" | 400×300 | SPI | No | ~2 s full | **$25–40** |
| [Waveshare 7.5" e-Paper (G)](https://www.waveshare.com/7.5inch-e-paper-g.htm) | 7.5" | 800×480 | SPI | No | ~3 s full | **$50–75** |
| [Waveshare 7.5" HAT (B) 3-color](https://www.waveshare.com/7.5inch-e-paper-hat-b.htm) | 7.5" | 800×480 R/B/W | SPI HAT | No | ~16 s color | **$60–85** |
| [Waveshare 10.3" HDMI e-Paper](https://www.waveshare.com/10.3inch-hdmi-e-paper.htm) | 10.3" | 1872×1404 | HDMI + USB | Yes (option) | 15 Hz | **$540–600** |
| [Waveshare 10.3" e-Paper Raw (parallel)](https://www.waveshare.com/10.3inch-e-paper.htm) | 10.3" | 1872×1404 | Parallel | No | ~1 s | **$300–380** |
| [Waveshare 13.3" e-Paper HAT+ (E) Spectra 6](https://www.waveshare.com/13.3inch-e-paper-hat-plus-e.htm) | 13.3" | 1600×1200 color | SPI | No | ~30 s color | **$330–410** |
| [DASUNG Paperlike HD-FT](https://shop.dasung.com/products/dasung-e-ink-paperlike-hd-front-light-and-touch-13-3-monitor) | 13.3" | 2200×1650 | HDMI + USB-C | Yes | ~40 Hz | **$649–699** |
| [DASUNG Paperlike 13K (mono)](https://shop.dasung.com/products/dasung-paperlike-13k-the-worlds-first-37hz-3k-e-ink-monitor) | 13.3" | 3200×1800 | HDMI + USB-C | Yes | ~37 Hz | **$679** |
| [DASUNG Paperlike 13K Color](https://shop.dasung.com/products/dasung-paperlike-13k-the-worlds-first-37hz-color-e-ink-monitor) | 13.3" | 3200×1800 Kaleido 3 | HDMI + USB-C | Yes | ~37 Hz | **$749** |
| [Boox Mira 13.3"](https://shop.boox.com/products/boox-mira-pro) | 13.3" | 2200×1650 | HDMI + USB-C | Yes | ~25 Hz | **$799** |
| [Boox Mira Pro 25.3" (mono)](https://onyxboox.com/boox_mirapro) | 25.3" | 3200×1800 | HDMI / DP / mini-DP / USB-C | No | ~25 Hz | **$1,599** |
| [Boox Mira Pro 25.3" Color](https://shop.boox.com/products/boox-mira-procolor-version) | 25.3" | 3200×1800 Kaleido 3 | HDMI / DP / USB-C | No | ~25 Hz | **$1,899** |
| [PineNote (Community Edition)](https://pine64.com/product/pinenote-community-edition-coming-soon/) | 10.3" | 1404×1872 | Standalone Linux tablet (RK3566) | Wacom EMR + cap | ~25 Hz | **$399** |

**Refresh tradeoff.** Sub-$100 SPI panels are batch-update only — fine for a status display showing weather, battery, RSS, or a Pi-Hole counter. DASUNG and Boox monitors are full HDMI replacements but cost as much as the rest of the deck combined. PineNote is a self-contained Linux tablet, so it can *be* the entire cyberdeck.

---

## 4. OLED Panels

Per-pixel contrast and zero black-state power, but smaller sizes than LCD and higher unit cost. There's effectively one mainstream "main display" OLED plus a huge selection of small status OLEDs.

| Model | Size | Resolution | Interface | Touch | Brightness | Power | Price (USD, ~2026) |
|---|---|---|---|---|---|---|---|
| [Waveshare 5.5" HDMI AMOLED](https://www.waveshare.com/5.5inch-hdmi-amoled.htm) | 5.5" | 1080×1920 | HDMI + USB | Cap 5-pt | 350 nits typ. | ~3.5 W | **$118–125** |
| [Waveshare 5.5" AMOLED w/ Case](https://www.waveshare.com/5.5inch-hdmi-amoled-with-case.htm) | 5.5" | 1080×1920 | HDMI + USB | Cap 5-pt | 350 nits | ~3.5 W | **$120–135** |
| [Crystalfontz CFAL12856A0 (Transparent OLED)](https://www.crystalfontz.com/product/cfal12856a00151b-128x56-transparent-oled-screen) | 1.51" | 128×56, ~70% transparent | SPI / I²C / 8-bit parallel | No | Light-blue pixels | ~0.3 W | **$21–28** |
| [Adafruit 0.96" 128×64 mono (SSD1306)](https://www.adafruit.com/product/326) | 0.96" | 128×64 | I²C/SPI | No | Bright mono | ~0.05 W | **$18–20** |
| [Adafruit 1.3" 128×64 mono (SH1106G)](https://www.adafruit.com/product/5228) | 1.3" | 128×64 | SPI | No | Bright mono | ~0.06 W | **$15–17** |
| [Adafruit 1.5" 128×128 RGB OLED (SSD1351)](https://www.adafruit.com/product/1431) | 1.5" | 128×128 16-bit color | SPI | No | RGB | ~0.2 W | **$40–45** |
| [Waveshare 2.42" OLED Module](https://www.waveshare.com/2.42inch-oled-module.htm) | 2.42" | 128×64 | SPI/I²C | No | Mono | ~0.1 W | **$25–30** |

**Pros:** the Waveshare 5.5" AMOLED is the dream main display for a small handheld cyberdeck — 1080p in 5.5" is iPhone-class sharpness with genuine OLED contrast. **Cons:** at $120 it's 2–3× equivalent IPS, and OLED burn-in is real if you live in `tmux` with a stationary status bar.

---

## 5. Secondary / Status / Accent Displays

Small panels embedded alongside the main display for CPU stats, battery state, SDR waterfall, or aesthetic flavor. Most are SPI/I²C and consume <1 W.

| Model | Size | Resolution | Interface | Touch | Type | Price (USD, ~2026) |
|---|---|---|---|---|---|---|
| [Pimoroni HyperPixel 4.0](https://shop.pimoroni.com/en-us/products/hyperpixel-4) | 4.0" | 800×480 | GPIO (DPI, parallel RGB) | Cap optional | IPS, 60 fps | **$75–82** |
| [Pimoroni HyperPixel 4.0 Square](https://shop.pimoroni.com/products/hyperpixel-4-square) | 4.0" sq | 720×720 | GPIO (DPI) | Cap optional | IPS | **$70–80** |
| [Adafruit PiTFT Plus 2.8" Capacitive](https://www.adafruit.com/product/2423) | 2.8" | 320×240 | SPI (HAT) | Cap | TFT | **$45–50** |
| [Adafruit PiTFT 3.5" Resistive](https://www.adafruit.com/product/2097) | 3.5" | 480×320 | SPI (HAT) | Resistive | TFT | **$45–50** |
| [Adafruit 3.5" Breakout HX8357D](https://www.adafruit.com/product/2050) | 3.5" | 480×320 | SPI | Resistive | TFT | **$32–38** |
| [Waveshare 1.3"–3.5" SPI TFTs](https://www.waveshare.com/product/displays.htm) | 1.3"–3.5" | 240×240–480×320 | SPI | Optional | TFT | **$10–35** |
| [HD44780 16×2 I²C character LCD](https://www.adafruit.com/product/181) | 16×2 char | n/a | I²C / parallel | No | STN/blue backlight | **$2–10** |
| [HD44780 20×4 I²C character LCD](https://www.adafruit.com/product/198) | 20×4 char | n/a | I²C / parallel | No | STN/blue backlight | **$4–15** |
| [Noritake GU-3000 / CU20029](https://www.noritake-elec.com/products/vfd-display-module) | 20×2–512×32 | varies | SPI / parallel / RS-232 / USB | No | VFD | **$60–250** |
| Adafruit 7-/14-segment backpacks | 4 digits | n/a | I²C | No | LED seg | **$10–18** |
| IN-12 / IN-14 Nixie tube kits (eBay / Tindie) | 6 digits | n/a | SPI / parallel | No | Nixie | **$80–250** |

**Picks.** HyperPixel 4.0 uses the Pi's parallel DPI lines rather than HDMI or DSI — a single Pi can run HyperPixel + an HDMI main display simultaneously without a hub. For ultra-low-effort status panels, an SSD1306 0.96" OLED on I²C costs $4 from AliExpress and draws ~50 mW. For aesthetics, Noritake VFDs are the cyberpunk pick — Blade Runner-blue with that distinctive segmented glow no LCD reproduces.

---

## 6. Cannibalized Portable Monitors / Donor Panels

For a 1080p+ display under $50, the cheapest path is rescuing an LCD from a dead laptop, broken iPad, or scrap pile and pairing it with a universal driver board.

**Common donor panels worth hunting:**
- **iPad LCDs (LP097QX1, LTL097QL01)** — 2048×1536 9.7" IPS. Driver boards on eBay/AliExpress (~$40) convert to HDMI.
- **MacBook Retina (LP133WQ1, LSN133KL01)** — 2560×1600. Needs eDP driver board (~$60).
- **Generic laptop 15.6" 1080p (LP156WF6, B156HAN, N156HCA)** — extremely cheap as scrap; accept generic M.NT68676.
- **Surface/tablet displays (LTN097QL01, LP094WX2)** — high-DPI portrait, great for vertical decks.

**Driver/controller boards:**

| Board | Inputs | Output | Resolution Cap | Price (USD, ~2026) |
|---|---|---|---|---|
| [M.NT68676.2A](https://www.amazon.com/NJYTouch-M-NT68676-2A-Controller-LP156WF4-SLB1-LP156WF1-TLC1/dp/B01FAJMCVU) | HDMI + DVI + VGA + audio | 30-pin LVDS | up to 2048×1152 | **$20–35** kit |
| [52Pi NT68676 (HDMI+VGA+DVI)](https://52pi.com/) | HDMI + VGA + DVI | LVDS | varies | **$30–50** kit |
| RTD2660 generic AliExpress kits | HDMI + VGA | 30/40-pin LVDS | up to 1920×1200 | **$15–25** kit |
| RTD2556 (eDP variant) | HDMI / mini-DP | eDP 30/40-pin | up to 4K | **$30–60** kit |
| ITE IT6251 / R8821AS | HDMI | eDP | up to 4K | **$25–50** kit |

**Process:** identify the panel's model number on its sticker, cross-reference at [panelook.com](https://www.panelook.com/), and order the matching board variant. You'll also need a 12 V / 3 A barrel-jack PSU for the controller; controller + backlight inverter can pull 10–15 W.

**Pros:** $30–60 total for a 1920×1080 panel that costs $150+ from Waveshare. **Cons:** mechanical packaging is on you, backlight inverter wiring is fiddly, and LVDS cables aren't interchangeable.

---

## 7. HDMI-to-DSI / MIPI Adapters and Driver Boards

When a panel's input doesn't match your board's output, these bridges fill the gap.

| Adapter | Direction | Use Case | Price (USD, ~2026) |
|---|---|---|---|
| [Geekworm X630 / C779](https://geekworm.com/products/x630) | HDMI → MIPI CSI-2 (Pi cam port) | Capture HDMI as a camera (Pi KVM, recorder) | **$30–45** |
| [Geekworm X1300 HDMI to CSI-2](https://geekworm.com/products/x1300) | HDMI → CSI-2 (Pi 5) | Same, Pi 5 specific | **$35–50** |
| [Auvidea B101](https://auvidea.eu/b101-hdmi-to-csi-2-bridge-15-pin-fpc/) | HDMI → CSI-2 (15-pin FPC) | Higher-quality (Toshiba TC358743) | **$95–130** |
| [Auvidea B102](https://auvidea.eu/b102-hdmi-to-csi-2-bridge-22-pin-fpc/) | HDMI → CSI-2 (22-pin FPC) | Same, 22-pin Pi 5 connector | **$145–170** |
| [Waveshare CM4-IO-Base-Acce A](https://www.waveshare.com/cm4-io-base-acce-a.htm) | DSI ← HDMI source | Drive DSI panel from non-Pi HDMI source | **$25–40** |
| Generic HDMI → MIPI DSI (TC358775) | HDMI → MIPI DSI | Drive raw MIPI panels (iPad, custom) from HDMI | **$30–80** AliExpress |
| eDP → HDMI converter (RTD2556) | HDMI → eDP | Drive laptop eDP panels from HDMI | **$25–50** |

**Important distinction:** HDMI-to-CSI bridges (Geekworm/Auvidea) are **input** bridges — they let a Pi *capture* an external HDMI source, not drive a display. For the reverse (Pi HDMI → MIPI panel), TC358775-based boards are the path; they require EDID/timing tuning but enable iPad-panel cyberdecks.

---

## How to Choose

### Interface Tradeoffs

| Interface | Pros | Cons | Best For |
|---|---|---|---|
| **DSI (Pi flat-flex)** | No HDMI/USB consumed; low power; clean | Pi-only; ~20 cm cable limit; needs `dtoverlay` | Pi-based decks |
| **HDMI + USB (touch)** | Universal; long cable runs OK; widest selection | Two cables; bulky connector; higher power | x86 / mini-PC builds |
| **USB-C alt-mode** | Single cable for video + power + touch | Source must support DP alt-mode (Pi 5 does NOT) | Framework, Steam Deck, NUC, mini-PC |
| **SPI / I²C** | Trivially driven from any GPIO; ultra-low power | Slow; small panels only; CPU-bound | Status displays, accents |
| **Parallel DPI (HyperPixel)** | Frees HDMI for a second display; 60 fps | Eats 28 GPIO; no HAT stacking | Single-Pi multi-display decks |
| **eDP/LVDS (donor panels)** | Cheapest path to high-DPI; huge selection | Mechanical packaging on you; 12 V PSU needed | Builders comfortable with controllers |

### Power Budget (rough, at ~75% brightness)
- 5" IPS: 1.5–2.5 W
- 7" IPS: 3–4 W
- 8.8" / 11.9" widescreen IPS: 4–6 W
- 10.1" IPS: 5–7 W
- 13.3"–15.6" portable monitor: 6–10 W
- 15.6" donor panel + controller: 10–15 W
- 5.5" AMOLED: 2–4 W (content-dependent)
- eInk active: 2–5 W; passive: 0 W
- Small OLED status (0.96"–2.4"): 50–200 mW
- HD44780 character LCD: 20–80 mW

A typical 50 Wh battery driving a 7" IPS + Pi 5 lasts 4–6 hours; an 11.9" widescreen costs about an hour. eInk-primary decks routinely last 12+ hours.

### Driver-Board Availability for Donor Panels
Look up the panel model at [panelook.com](https://www.panelook.com/). Rules of thumb:
- **30-pin LVDS** → M.NT68676 fits 90%+
- **40-pin LVDS HD/FHD** → "LVDS 40pin" RTD2660 kits
- **eDP (30/40-pin)** → RTD2556 / RT2796 / ITE IT6251
- **MIPI DSI** (iPad, Surface) → TC358775 boards, far harder to source

When in doubt, message the AliExpress seller with the exact panel part number — they ship the matching cable harness.

### Sunlight Readability
1. **eInk** — best sunlight, terrible refresh.
2. **Transflective TN** — niche, 2–3× transmissive cost, excellent outdoor.
3. **High-nit IPS (500+ nits)** — adequate in shade, marginal in direct sun. Most Waveshare panels claim 300–400 nits, fine indoors but washes out at noon.
4. **Anti-glare coatings** — help with reflection but don't add brightness.

A genuine 1000+ nit transflective LCD from [Crystalfontz's sunlight-readable line](https://www.crystalfontz.com/c/sunlight-readable-displays/38) costs 3–5× a standard IPS — only worth it for marine/field-deck builds.

### Touch vs. Non-Touch
Touch adds $10–30 and either a USB cable (HDMI panels) or an I²C line (DSI panels). Genuinely useful for handheld tablet-style decks but rarely used on keyboard-driven decks. Resistive touch has aged badly compared to a good trackpoint. **Skip touch on keyboard-driven decks; include capacitive (never resistive) on handheld/tablet-form decks.**

---

## Quick Picks by Build Style

- **Classic Pi 4/5 wedge deck, ~$60 display budget:** Raspberry Pi Touch Display 2 (7") — DSI, official, $60.
- **Slim "keyboard slab" deck:** Waveshare 11.9" 320×1480 HDMI or DSI — $100–125.
- **Handheld pocket deck, OLED look:** Waveshare 5.5" AMOLED — $120, 1080×1920 portrait.
- **Long-runtime field/research deck:** PineNote at $399 (standalone), or Waveshare 10.3" HDMI eInk at $540+.
- **Donor-panel budget build (15.6" 1080p for ~$60 total):** scrap laptop LCD + M.NT68676.2A kit.
- **Multi-display dashboard deck:** HyperPixel 4.0 ($80) on parallel DPI + any HDMI panel simultaneously.
- **x86 / Framework mainboard deck:** Magedok T101A USB-C 2K touchscreen at $169.
- **Aesthetic / "retro-future terminal" deck:** Noritake GU-3000 VFD or Crystalfontz transparent OLED ($21–28) as secondary, paired with any IPS primary.

---

## Sources

- [Waveshare Displays catalog](https://www.waveshare.com/product/displays.htm)
- [Waveshare e-Paper category](https://www.waveshare.com/epaper)
- [Raspberry Pi Touch Display 2 announcement](https://www.raspberrypi.com/news/raspberry-pi-touch-display-2-on-sale-now-at-60/)
- [Pi Touch Display 2 (5") release, CNX Software](https://www.cnx-software.com/2025/08/18/raspberry-pi-touch-display-2-gets-40-5-inch-variant-with-1280x720-resolution/)
- [DASUNG Paperlike 13K, NotebookCheck](https://www.notebookcheck.net/Mobile-e-ink-touchscreen-monitor-with-colors-and-37Hz-Dasung-presents-the-Paperlike-13K-Color.1007535.0.html)
- [Boox Mira Pro Color, Tom's Hardware](https://www.tomshardware.com/monitors/boox-debuts-23-5-inch-color-e-ink-monitor-with-1800p-resolution-and-usd1-900-price-tag)
- [Pimoroni HyperPixel 4.0](https://shop.pimoroni.com/en-us/products/hyperpixel-4)
- [Adafruit PiTFT category](https://www.adafruit.com/category/804)
- [Crystalfontz sunlight-readable displays](https://www.crystalfontz.com/c/sunlight-readable-displays/38)
- [Auvidea HDMI-CSI bridges](https://auvidea.eu/bridge/)
- [Geekworm Raspberry Pi displays](https://geekworm.com/collections/raspberry-pi/display)
