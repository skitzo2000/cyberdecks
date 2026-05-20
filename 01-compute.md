# Cyberdeck Compute: 2026 Buyer's Guide

A cyberdeck lives or dies by its compute board. The right pick balances power draw against the battery you can physically fit, ISA against the software you actually want to run, and physical form factor against your chassis. This guide surveys the 2026 landscape across seven categories.

---

## How to Choose

### ARM vs x86 vs RISC-V

- **ARM (Cortex-A76, RK3588, Apple-class etc.)** gets you 2–10 W idle, fanless-capable, and a mature Linux story. Trade-offs: closed-source GPU/video stacks on Rockchip/Amlogic, no Wine for arbitrary x86 binaries (FEX/Box64 work for many things but not all), and Windows-on-ARM is unsupported on these chips.
- **x86 (Intel N-series, Ryzen U/HS)** is the only path if you need Steam, Adobe, full Wine compatibility, or arbitrary Windows binaries. Modern Alder Lake-N (N100/N97/N305) and Hawk Point Ryzen are surprisingly efficient — 6 W idle, 15–28 W under load — and run mainline Linux flawlessly.
- **RISC-V** is for tinkerers and educators in 2026. The SpacemiT K1 (BPI-F3) is the first chip with an actually-shipping desktop-class user experience, but you should still expect rebuilding from source, missing accelerated video, and patchy distro support. Don't pick this if you want to "just use the deck."

### Battery vs performance

Rule of thumb: a 10000 mAh / 37 Wh power bank gives ~10 hours on a Pi 5 at 3 W average, ~4 hours on an N100 mini-PC mainboard at 8 W, and ~1.5 hours on a Ryzen AI 9 at 25 W. Closed chassis with no airflow throttle hot chips back hard — a Ryzen HX 370 in a 3D-printed sealed shell will often perform worse than an N100 with a heatsink.

### Cyberdeck-friendliness checklist
- **Single 5 V or USB-PD input** — easier to power from packs and solar
- **Low-profile, single-PCB form factor** — easier to mount
- **M.2 NVMe** — fast, robust storage that fits inside the chassis
- **HDMI/DP/MIPI-DSI** — at least one option matching your display
- **Exposed GPIO (40-pin or compatible)** — lets you hang sensors, e-ink, SDR, LoRa modules off the deck
- **Mainline kernel support** — vendor BSPs go stale fast; mainline means the deck still boots in 5 years

---

## 1. ARM SBCs

The Raspberry Pi 5 family and the RK3588-based competition dominate. Pi has the ecosystem and HAT compatibility; Rockchip wins on raw performance, RAM ceilings, and M.2.

| Board | Price (USD) | CPU | RAM | Storage | Idle / Load (W) | I/O | OS | Notes |
|---|---|---|---|---|---|---|---|---|
| [Raspberry Pi 5 (4/8/16 GB)](https://www.raspberrypi.com/news/16gb-raspberry-pi-5-on-sale-now-at-120/) | $60 / $80 / $120 | BCM2712 4×A76 @ 2.4 GHz | LPDDR4X | microSD + PCIe 2.0 x1 (M.2 via HAT+) | 2–3 / 8–10 | 2×4K HDMI, 2×USB3, GbE, 40-pin GPIO | Mainline Linux, Pi OS | The default. Needs 5 V/5 A PD PSU under load. |
| [Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) | $15 | RP3A0 4×A53 @ 1 GHz | 512 MB | microSD | 0.6 / 2 | mini-HDMI, microUSB, WiFi 4 | Pi OS Lite | Tiny, throttles under sustained load; perfect for nethunter/SDR decks. |
| [Pi CM5 + IO Board](https://www.raspberrypi.com/news/compute-module-5-on-sale-now/) | $45–95 module + $20–60 carrier | BCM2712 | 2/4/8/16 GB | optional eMMC 0–64 GB | 2 / 9 | depends on carrier; official IO has 2×PCIe, 2×HDMI | Pi OS | Carrier-board flexibility = cyberdeck gold. Many 3rd-party CM5 carriers (TV stick, dual-NVMe, LTE). |
| [Radxa Rock 5B / 5B+](https://radxa.com/products/rock5/5bp/) | $110–190 | RK3588 8-core (4×A76 + 4×A55) @ 2.4 GHz, 6 TOPS NPU | up to 32 GB LPDDR5 | M.2 NVMe + eMMC | 3 / 12 | 2×HDMI, HDMI-in, 2.5GbE, 40-pin | Debian/Armbian | Highest-end RK3588 board, mature mainline kernel work. |
| [Radxa Rock 5C](https://forum.radxa.com/t/announcing-the-rock-5c-power-performance-and-versatility-for-just-30/20429) | $30–90 | RK3588S2 | 2/4/8/16 GB LPDDR4X | microSD + M.2 (E-key) | 2.5 / 10 | HDMI 2.1, GbE, 40-pin | Debian/Ubuntu | Cheap RK3588S in Pi-shaped form factor. Best ARM perf-per-dollar. |
| [Radxa Rock 5T](https://liliputing.com/rock-5t-is-a-rk3588-single-board-pc-with-up-to-32gb-ram-two-m-2-sockets-and-plenty-of-i-o/) | $114–220 | RK3588 | up to 32 GB LPDDR5 | 2× M.2 + microSD + eMMC | 3 / 13 | triple-display, 2.5GbE | Debian | Built for I/O-heavy decks; dual NVMe is unusual at this price. |
| [Orange Pi 5 Plus (4/8/16/32 GB)](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5-plus.html) | $99 / $129 / $149 / $179 | RK3588 | LPDDR4X | M.2 NVMe + eMMC | 3 / 12 | 2× HDMI-out, HDMI-in, dual 2.5GbE, M.2 E-key WiFi | Debian/Armbian/Ubuntu | Cheapest 32 GB RK3588 board. HDMI-in is rare and useful. |
| [Orange Pi 5 Max (4/8/16 GB)](https://www.techspot.com/news/103884-orange-pi-5-max-6-tops-npu-up.html) | $75 / $95 / $125 | RK3588 | LPDDR5 | M.2 NVMe | 2.5 / 11 | 2× HDMI 2.1, 2.5GbE, WiFi 6E | Debian/Ubuntu | LPDDR5 + WiFi 6E for less than a Pi 5 16 GB. Aggressive value pick. |
| [Khadas VIM4](https://www.khadas.com/vim4) | $200 | Amlogic A311D2 (4×A73 + 4×A53), 3.2 TOPS NPU | 8 GB LPDDR4X | 32 GB eMMC | 2 / 9 | HDMI-out + HDMI-in (rare), WiFi 6, MIPI-CSI | Ubuntu/Android | Premium build, 9–20 V wide input is friendly to battery packs. |
| [NanoPi M6](https://www.electronics-lab.com/nanopi-m6-rk3588s-soc-based-sbc-with-mali-g610-gpu-8k-video-support-and-lpddr5-ram-options/) | $70 (4 GB) – $150 (32 GB) | RK3588S | up to 32 GB LPDDR5 | microSD + eMMC | 2.5 / 10 | HDMI 2.1, dual MIPI-DSI, 40-pin | FriendlyWrt / Ubuntu | Metal case + optional 3.5" touchscreen — nearly a deck out of the box. |
| [NanoPi R6S](https://liliputing.com/nanopi-r6s-is-a-single-board-pc-with-rk3588s-8gb-ram-and-three-ethernet-ports-for-119/) | $119 | RK3588S | 8 GB LPDDR4X | 32 GB eMMC | 3 / 10 | 2× 2.5GbE + GbE, HDMI 2.1 | FriendlyWrt / Debian | Router-shaped but viable as networking-focused deck core. |
| [LibreComputer Sweet Potato (S905X-CC-V2)](https://www.notebookcheck.net/Libre-Computer-Sweet-Potato-launches-with-PoE-capability-for-US-35.747491.0.html) | $35 | Amlogic S905X 4×A53 @ 1.5 GHz | 2 GB | microSD | 1.5 / 5 | HDMI, USB 3, PoE-capable, 40-pin Pi-compatible | Raspbian/Ubuntu | Pi-pin-compatible at half the price; underpowered but cheap and mainline. |
| [Pine64 ROCKPro64](https://pine64.org/devices/rockpro64/) | $60–80 | RK3399 (2×A72 + 4×A53) | 2 / 4 GB | microSD + eMMC + PCIe x4 | 2 / 8 | HDMI 2.0a, USB3, GbE, full PCIe x4 slot | Manjaro/Armbian | Old but the only ARM SBC with a real PCIe x4 slot — fits an actual GPU or 10 G NIC. |
| [Pine64 Quartz64 Model B](https://hothardware.com/news/pine64s-quartz64-now-available-as-a-rock-solid-alternative-to-raspberry-pi) | $60–80 | RK3566 4×A55 @ 1.8 GHz | up to 8 GB | microSD + eMMC + M.2 | 1.5 / 5 | HDMI, GbE | Mainline Linux | Lower-perf than RK3588 boards but well-supported. |

**Pros (ARM general):** low power, fanless options, GPIO ecosystem, mature Pi-OS-style distros.
**Cons:** no Windows compatibility, RK3588 video/3D acceleration still rough on mainline kernels, vendor BSPs lock you to old kernels.

---

## 2. RISC-V SBCs

In 2026 RISC-V has crossed from "absolute pain" to "usable for daily light tasks if you're patient." None of these run Steam, Discord, or Chromium with hardware video accel cleanly.

| Board | Price | CPU | RAM | Power | OS | Notes |
|---|---|---|---|---|---|---|
| [Milk-V Mars](https://milkv.io/mars) | $50–90 | StarFive JH7110 4× U74 @ 1.5 GHz | 2 / 4 / 8 GB LPDDR4 | 2 / 5 W | Debian RISC-V, Armbian | Pi-3-compatible footprint. Mature-ish JH7110. |
| [StarFive VisionFive 2](https://www.cnx-software.com/2025/08/07/visionfive-2-lite-low-cost-risc-v-sbc/) | $50–120 | JH7110 | 2 / 4 / 8 GB | 2 / 5 W | Debian | The reference RISC-V SBC for desktop experimentation. |
| [VisionFive 2 Lite](https://www.kickstarter.com/projects/starfive/visionfive-2-lite-unlock-risc-v-sbc-at-199) | $20–40 | JH7110S @ 1.25 GHz | 2 / 4 / 8 GB | 1.5 / 4 W | Debian | Cheapest 64-bit RISC-V SBC available. |
| [Banana Pi BPI-F3](https://www.bpi-shop.com/products/anana-pi-bpi-f3-design-with-spacemit-k1-8-core-risc-v-chip.html) | $65–95 | SpacemiT K1 8-core RVA22, 2 TOPS NPU | 2/4/8/16 GB DDR | 3 / 9 W | Bianbu (Ubuntu fork) | The first RISC-V SBC that feels like a real desktop. RVA22 vector extensions = real software compatibility. |
| [Milk-V Pioneer](https://liliputing.com/milk-v-pioneer-is-a-64-core-risc-v-workstation-for-1199-and-up-crowdfunding/) | $1,199+ | SOPHON SG2042 64-core @ 2 GHz | DDR4 ECC | 70–120 W | Debian/Fedora | mATX workstation board. Not realistic for a deck unless you build a desktop-class luggable. |

**Pros:** novel architecture, fully open ISA, RVA22 chips are usable. **Cons:** no GPU acceleration in mainline, video decode is software-only, expect to rebuild a lot from source.

---

## 3. x86 SBCs and Mini-Mainboards

These are the cyberdeck sweet spot when you need Windows or Steam compatibility. Alder Lake-N is the modern N100/N97/N305 — surprisingly efficient at idle.

| Board | Price | CPU | RAM | Storage | Idle / Load (W) | I/O | Notes |
|---|---|---|---|---|---|---|---|
| [LattePanda Mu](https://www.tomshardware.com/raspberry-pi/lattepanda-mu-review) | $139 module; ~$190 with Lite Carrier | Intel N100 4-core | 8 GB LPDDR5 | 64 GB eMMC + M.2 via carrier | 4 / 12 | depends on carrier | SO-DIMM-style compute module. Best modular x86 for cyberdecks. |
| [LattePanda 3 Delta](https://www.lattepanda.com/lattepanda-3-delta) | $279–329 | Intel N5105 4-core | 8 GB LPDDR4 | 64 GB eMMC + M.2 | 5 / 15 | HDMI + DP, 2.5GbE, M.2 ×2, Arduino co-processor | Onboard ATmega32u4 for GPIO/Arduino sketches. |
| [LattePanda Sigma](https://www.lattepanda.com/lattepanda-sigma) | $579 barebones – $900 | Intel Core i5-1340P 12-core | up to 32 GB LPDDR5 dual-channel | 3× M.2 NVMe | 8 / 28 | TB4, dual 2.5GbE, dual HDMI 2.1 + DP | Most powerful x86 SBC in this list. Onboard Arduino. |
| [ODROID-H4](https://www.hardkernel.com/shop/odroid-h4/) | $99 | Intel N97 4-core @ 3.6 GHz | up to 48 GB DDR5 SO-DIMM | M.2 + eMMC | 5 / 12 | HDMI 2.0, 2× DP, 2× 2.5GbE | Real DDR5 SO-DIMM — upgrade-friendly. |
| [ODROID-H4+](https://www.hardkernel.com/shop/odroid-h4-plus/) | $139 | N97 | DDR5 SO-DIMM | 4× SATA + M.2 + eMMC | 6 / 13 | adds 4× SATA | NAS-deck builds. |
| [ODROID-H4 Ultra](https://www.hardkernel.com/shop/odroid-h4-ultra/) | $220 | Intel Core i3-N305 8-core | DDR5 SO-DIMM | M.2 + 4× SATA | 7 / 20 | as H4+ | 8 cores in 15 W TDP — best perf-per-watt x86 deck core under $250. |
| [AAEON UP 7000](https://www.aaeon.com/en/product/detail/up-7000-boards) | $179–329 | Intel N50/N97/N100/N200 | up to 16 GB LPDDR5 | M.2 + eMMC | 5 / 12 | HDMI, GbE, 40-pin HAT, USB 3.2 | Credit-card-sized x86 with a Pi-style HAT header. |
| [AAEON UP Squared Pro 7000](https://www.aaeon.com/en/product/detail/up-board-up-squared-pro-7000) | $300–650 | Intel N97/N305/Atom x7000E | 16 GB LPDDR5 | M.2 ×3 + SATA | 6 / 20 | 2× 2.5GbE, USB-C DP-alt | Industrial 4"×4" board, multiple M.2 slots. |
| [Framework Laptop 13 Mainboard (Ryzen AI 300)](https://frame.work/products/mainboard-amd-ai300?v=FRANTE0009) | $449+ | Ryzen AI 9 HX 370 / AI 5 340 (Zen 5) | DDR5 SO-DIMM ×2 to 96 GB | M.2 2280 | 6 / 35 | USB-C ×4 (Framework expansion cards) | Most cyberdeck-relevant of all — wide community of mods, modular USB-C "cards." |
| [Framework Laptop 13 Mainboard (Intel Core Ultra Series 2)](https://frame.work/marketplace/mainboards) | $499+ | Intel Lunar Lake Core Ultra | LPDDR5x soldered | M.2 2280 | 4 / 30 | USB-C ×4 | Lower power; preferable for fanless or battery-heavy decks. |
| [Framework Laptop 16 Mainboard (Ryzen AI 300)](https://frame.work/products/laptop16-mainboard-amd-ai300?v=FRAKKE0009) | $699+ | Ryzen AI HX 370 | DDR5 SO-DIMM | M.2 ×2 | 8 / 55 | USB-C, MXM-style dGPU support | For luggable-class decks with a discrete GPU bay. |
| [Framework Desktop Mainboard (Strix Halo)](https://frame.work/products/framework-desktop-mainboard-amd-ryzen-ai-max-300-series?v=FRAFMK0002) | $799–1,699 | Ryzen AI Max+ 395 16-core + Radeon 8060S | 64/128 GB LPDDR5x soldered | 2× M.2 2280 | 15 / 120 | Mini-ITX, full I/O panel | Strix Halo in mini-ITX. Power-hungry — needs a real PSU. |

**Pros:** runs anything (Windows, Steam, Wine), excellent mainline Linux, SO-DIMM upgradeability on ODROID/Framework.
**Cons:** higher idle power than ARM, fans usually required, larger PCBs.

---

## 4. Mini PCs as Deck Cores

Gut a mini PC; mount the mainboard in the chassis.

| Mini PC | Price | CPU | RAM/Storage | Idle / Load (W) | Notes |
|---|---|---|---|---|---|
| [Beelink SER8](https://www.bee-link.com/products/beelink-ser8-8745hs) | $499–629 | Ryzen 7 8845HS, Radeon 780M, 16 TOPS NPU | 32 GB DDR5 / 1 TB NVMe | 8 / 65 | Strong all-rounder; mainboard ~12×12 cm. |
| [Beelink SER9 / SER9 Pro](https://www.bee-link.com/products/beelink-ser9-ai-9-hx-370) | $799–999 | Ryzen AI 9 HX 370 12C Zen 5, Radeon 890M, 80 TOPS | 32 GB LPDDR5X / 1 TB | 10 / 80 | Top-tier; thermals are challenging in a closed deck. |
| [Minisforum UM890 Pro](https://store.minisforum.com/products/minisforum-um890pro-mini-pc) | $463 (sale) – $579 | Ryzen 9 8945HS | 32 GB DDR5 / 1 TB | 8 / 65 | Two USB4 ports + dual 2.5GbE. |
| [Minisforum MS-01](https://store.minisforum.com/) | $423–700+ | Intel Core i9-12900H / 13900H | DDR5 SO-DIMM, 3× M.2 | 10 / 65 | Workstation-class I/O including 10GbE SFP+. |
| [Minisforum MS-A2](https://videocardz.com/newz/minisforum-launches-ms-a2-mini-workstation-with-ryzen-9-9955hx-price-starts-at-799) | $439–919 | Ryzen 9 7945HX / 9955HX | DDR5 SO-DIMM, M.2 ×3 | 12 / 110 | "ITX in a brick." Too hot for sealed decks. |
| [GMKtec NucBox K8 / K8 Plus](https://www.gmktec.com/products/amd-ryzen-7-8845hs-mini-pc-nucbox-k8-plus) | $359–399 | Ryzen 7 8845HS | 32 GB DDR5 / 1 TB | 8 / 60 | Cheapest 8845HS unit. Common donor. |
| [MeLE Quieter 4C](https://store.mele.cn/products/mele-quieter-4c-n100-3-4ghz-fanless-mini-computer-lpddr4x-win11-hdmi-4k-wi-fi-5-bt-5-1-usb-3-2-2-usb-2-0-1-type-c-1) | $140–330 | Intel N100/N150 | 8–32 GB LPDDR5 / up to 1 TB | 4 / 10 | **Fanless.** Ideal for silent sealed-chassis decks. |
| [ASUS NUC 14 Pro / Pro+](https://www.asus.com/us/displays-desktops/nucs/nuc-mini-pcs/asus-nuc-14-pro/) | $650–1,100 | Intel Core Ultra 5/7/9 (Meteor Lake) | DDR5 SO-DIMM, M.2 ×2 | 7 / 60 | Modular NUC successor. 4×4" board ports well to handheld chassis. |
| [ASUS NUC 14 Pro AI](https://www.asus.com/us/displays-desktops/nucs/nuc-mini-pcs/asus-nuc-14-pro-ai/) | $899+ | Core Ultra Series 2 (Lunar Lake) | LPDDR5x soldered | 4 / 30 | <0.6 L volume. Soldered RAM tradeoff. |

**Pros:** complete working system; unbox, gut, mount. **Cons:** original cooling doesn't fit the new chassis; PSU brick is bulky.

---

## 5. Handheld x86 Devices as Deck Cores

Pre-built portable computers — chassis donors or starting points.

| Device | Price | CPU | Display | Battery | Notes |
|---|---|---|---|---|---|
| [Steam Deck OLED](https://www.steamdeck.com/) | $399 (512 GB) / $649 (1 TB) | AMD Aerith Plus + RDNA 2 8 CU | 7.4" 1280×800 OLED 90 Hz | 50 Wh | Best deck-base. Complete Linux device with SteamOS. |
| [Lenovo Legion Go 2 (SteamOS)](https://www.engadget.com/gaming/pc/lenovo-reveals-a-steamos-variant-of-the-legion-go-2-at-ces-010000852.html) | $1,200 (June 2026) | Ryzen Z2 Extreme | 8.8" OLED | 70+ Wh | Detachable controllers + larger screen — donor for "wider" cyberdeck layouts. |
| [GPD Pocket 4](https://www.indiegogo.com/en/projects/gpdhk/gpd-pocket-4-modular-full-featured-handheld-ai-pc) | $899–1,500 | Ryzen AI 9 HX 370 | 8.8" 144 Hz | 45 Wh | Modular port system. Already cyberdeck-shaped. |
| [OneXPlayer / OneXFly Apex](https://liliputing.com/amd-strix-halo-handheld-gaming-pc-spec-shoot-out-ayaneo-next-ii-vs-gpd-win-5-vs-onexfly-apex/) | $1,200–1,800 | Ryzen AI Max+ 395 (Strix Halo) | varies | varies | Strix Halo in a handheld — overkill but possible. |
| [AYANEO Slide / Air](https://www.ayaneo.com/) | $700–1,200 | Ryzen 7 7840U / 8840U | 6–7" | 47 Wh | Slide-out keyboard is already cyberdeck-aesthetic. |
| [AYANEO Pocket S Mini](https://www.notebookcheck.net/AyaNeo-Pocket-S-Mini-revealed-as-new-compact-handheld-with-4-3-display-and-Snapdragon-G3x-Gen-2.1118494.0.html) | ~$400 (Mar 2026) | Snapdragon G3x Gen 2 (ARM) | 4:3 display | — | Android-native, unique 4:3 form factor candidate. |

**Pros:** screen, battery, controls, thermals already engineered. **Cons:** opening voids warranty; odd-shaped mainboards; soldered storage.

---

## 6. Compute Modules and SOMs

| Module | Price | Compute | Notes |
|---|---|---|---|
| [Raspberry Pi CM5](https://www.raspberrypi.com/products/compute-module-5/) | $45–95 | Pi 5 silicon in 55×40 mm | Dominant SOM for cyberdecks in 2026 — Geekworm X1500 / dual-NVMe carriers popular. |
| [Radxa CM5 / CM5 Lite](https://radxa.com/products/cm/cm5/) | $95–200 | RK3588S2, up to 32 GB LPDDR4X + 128 GB eMMC, 56×41 mm | Faster than Pi CM5. |
| [Jetson Orin Nano Super Dev Kit](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/) | $249 | 6-core A78AE + 1024 CUDA Ampere, 67 TOPS, 8 GB LPDDR5 | Cheapest realistic on-device LLM platform. 7–25 W. Pi-5-sized carrier. |
| [Jetson Orin NX 8/16 GB](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) | $499–799 (modules) | 6/8-core A78AE + 1024 CUDA, 100–157 TOPS | For AI-heavy decks. 10–25 W. Needs 3rd-party carrier. |
| [Coral Dev Board Mini](https://www.coral.ai/products/dev-board-mini) | $99.99 | MediaTek 8167S + Edge TPU 4 TOPS | Mostly out-of-stock since 2022. Second-hand only. |
| [MNT Reform Mainboard / RCM modules](https://shop.mntre.com/t/hardware/reform) | €220–€600 | i.MX 8M Plus, LS1028A, or RK3588 RCM | Fully open-source. RK3588 RCM is the performance pick. |

---

## 7. Cyberdeck-Native and -Adjacent Products

| Product | Price | Compute | Display | Notes |
|---|---|---|---|---|
| [ClockworkPi uConsole](https://www.clockworkpi.com/uconsole) | $139–209 | RPi CM4 Lite, A-04, A-06 (RK3399), or R-01 RISC-V | 5" 1280×720 LCD | Tilt-up screen, 74-key kbd, 2× 18650 batteries, optional 4G modem. Canonical "buy a cyberdeck" product. |
| [ClockworkPi DevTerm](https://www.clockworkpi.com/devterm) | $239–339 | same module options as uConsole | 6.86" 1280×480 ultrawide LCD | Terminal-form-factor with thermal printer dock. |
| [MNT Pocket Reform](https://shop.mntre.com/products/mnt-pocket-reform) | €1,399 | i.MX 8M Plus or RK3588 RCM | 7" 1920×1200 | Tiny open-hardware laptop; mainboard available standalone. |
| [MNT Reform Next](https://www.crowdsupply.com/mnt/mnt-reform-next) | €1,500–2,000 | swappable RCM | 12.5" 1920×1080 | Larger laptop/luggable. |
| [Framework Laptop 16 (donor)](https://frame.work/laptop16) | $1,400+ | Ryzen AI 300 series | 16" 165 Hz | Expansion bay is a frequent cyberdeck mod target. |
| [Pi Slate (community design)](https://www.cnx-software.com/2026/05/11/pi-slate-a-raspberry-pi-5-handheld-linux-cyberdeck-with-a-5-inch-1280x720-touchscreen-display/) | DIY ~$200 BOM | Pi 5 | 5" touchscreen | Reference design for Pi-5 handheld cyberdecks. |

---

## Quick Recommendations

- **Cheapest "real" cyberdeck core (under $80):** Raspberry Pi 5 8 GB or Radxa Rock 5C 8 GB.
- **Best ARM perf-per-dollar:** Orange Pi 5 Max 16 GB at $125 or NanoPi M6 16 GB at ~$100.
- **Best x86 deck core (under $250):** ODROID-H4 Ultra ($220, 8-core N305, 15 W TDP).
- **Best modular x86 platform:** Framework Laptop 13 Mainboard (Ryzen AI 300 or Lunar Lake).
- **On-device AI / LLM-capable deck:** Jetson Orin Nano Super Dev Kit at $249.
- **Buy-don't-build cyberdeck:** ClockworkPi uConsole A-06 ($209).
- **Donor handheld:** Steam Deck OLED at $399.
- **Tinker-flex pick:** Pi CM5 + dual-NVMe carrier (Geekworm X1500-class).

---

## Sources

### ARM SBCs
- [Raspberry Pi 5 (4/8/16 GB)](https://www.raspberrypi.com/news/16gb-raspberry-pi-5-on-sale-now-at-120/) · [Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) · [Pi CM5 + IO Board](https://www.raspberrypi.com/news/compute-module-5-on-sale-now/)
- [Radxa Rock 5B / 5B+](https://radxa.com/products/rock5/5bp/) · [Radxa Rock 5C](https://forum.radxa.com/t/announcing-the-rock-5c-power-performance-and-versatility-for-just-30/20429) · [Radxa Rock 5T](https://liliputing.com/rock-5t-is-a-rk3588-single-board-pc-with-up-to-32gb-ram-two-m-2-sockets-and-plenty-of-i-o/)
- [Orange Pi 5 Plus](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5-plus.html) · [Orange Pi 5 Max](https://www.techspot.com/news/103884-orange-pi-5-max-6-tops-npu-up.html)
- [Khadas VIM4](https://www.khadas.com/vim4)
- [NanoPi M6](https://www.electronics-lab.com/nanopi-m6-rk3588s-soc-based-sbc-with-mali-g610-gpu-8k-video-support-and-lpddr5-ram-options/) · [NanoPi R6S](https://liliputing.com/nanopi-r6s-is-a-single-board-pc-with-rk3588s-8gb-ram-and-three-ethernet-ports-for-119/)
- [LibreComputer Sweet Potato](https://www.notebookcheck.net/Libre-Computer-Sweet-Potato-launches-with-PoE-capability-for-US-35.747491.0.html)
- [Pine64 ROCKPro64](https://pine64.org/devices/rockpro64/) · [Pine64 Quartz64 Model B](https://hothardware.com/news/pine64s-quartz64-now-available-as-a-rock-solid-alternative-to-raspberry-pi)

### RISC-V SBCs
- [Milk-V Mars](https://milkv.io/mars) · [Milk-V Pioneer](https://liliputing.com/milk-v-pioneer-is-a-64-core-risc-v-workstation-for-1199-and-up-crowdfunding/)
- [StarFive VisionFive 2](https://www.cnx-software.com/2025/08/07/visionfive-2-lite-low-cost-risc-v-sbc/) · [VisionFive 2 Lite](https://www.kickstarter.com/projects/starfive/visionfive-2-lite-unlock-risc-v-sbc-at-199)
- [Banana Pi BPI-F3](https://www.bpi-shop.com/products/anana-pi-bpi-f3-design-with-spacemit-k1-8-core-risc-v-chip.html)

### x86 SBCs / Mini-Mainboards
- [LattePanda Mu review (Tom's Hardware)](https://www.tomshardware.com/raspberry-pi/lattepanda-mu-review) · [LattePanda 3 Delta](https://www.lattepanda.com/lattepanda-3-delta) · [LattePanda Sigma](https://www.lattepanda.com/lattepanda-sigma)
- [ODROID-H4](https://www.hardkernel.com/shop/odroid-h4/) · [ODROID-H4+](https://www.hardkernel.com/shop/odroid-h4-plus/) · [ODROID-H4 Ultra](https://www.hardkernel.com/shop/odroid-h4-ultra/)
- [AAEON UP 7000](https://www.aaeon.com/en/product/detail/up-7000-boards) · [AAEON UP Squared Pro 7000](https://www.aaeon.com/en/product/detail/up-board-up-squared-pro-7000)
- [Framework Laptop 13 Mainboard (Ryzen AI 300)](https://frame.work/products/mainboard-amd-ai300?v=FRANTE0009) · [Framework 13 (Intel Core Ultra)](https://frame.work/marketplace/mainboards) · [Framework Laptop 16 Mainboard](https://frame.work/products/laptop16-mainboard-amd-ai300?v=FRAKKE0009) · [Framework Desktop Mainboard (Strix Halo)](https://frame.work/products/framework-desktop-mainboard-amd-ryzen-ai-max-300-series?v=FRAFMK0002)

### Mini PCs
- [Beelink SER8](https://www.bee-link.com/products/beelink-ser8-8745hs) · [Beelink SER9 / SER9 Pro](https://www.bee-link.com/products/beelink-ser9-ai-9-hx-370)
- [Minisforum UM890 Pro](https://store.minisforum.com/products/minisforum-um890pro-mini-pc) · [Minisforum MS-01](https://store.minisforum.com/) · [Minisforum MS-A2](https://videocardz.com/newz/minisforum-launches-ms-a2-mini-workstation-with-ryzen-9-9955hx-price-starts-at-799)
- [GMKtec NucBox K8 / K8 Plus](https://www.gmktec.com/products/amd-ryzen-7-8845hs-mini-pc-nucbox-k8-plus)
- [MeLE Quieter 4C](https://store.mele.cn/products/mele-quieter-4c-n100-3-4ghz-fanless-mini-computer-lpddr4x-win11-hdmi-4k-wi-fi-5-bt-5-1-usb-3-2-2-usb-2-0-1-type-c-1)
- [ASUS NUC 14 Pro / Pro+](https://www.asus.com/us/displays-desktops/nucs/nuc-mini-pcs/asus-nuc-14-pro/) · [ASUS NUC 14 Pro AI](https://www.asus.com/us/displays-desktops/nucs/nuc-mini-pcs/asus-nuc-14-pro-ai/)

### Handheld x86 / Donor Devices
- [Steam Deck OLED](https://www.steamdeck.com/) · [Lenovo Legion Go 2 SteamOS (Engadget)](https://www.engadget.com/gaming/pc/lenovo-reveals-a-steamos-variant-of-the-legion-go-2-at-ces-010000852.html)
- [GPD Pocket 4 (Indiegogo)](https://www.indiegogo.com/en/projects/gpdhk/gpd-pocket-4-modular-full-featured-handheld-ai-pc) · [OneXFly Apex (Liliputing)](https://liliputing.com/amd-strix-halo-handheld-gaming-pc-spec-shoot-out-ayaneo-next-ii-vs-gpd-win-5-vs-onexfly-apex/)
- [AYANEO Slide / Air](https://www.ayaneo.com/) · [AYANEO Pocket S Mini (NotebookCheck)](https://www.notebookcheck.net/AyaNeo-Pocket-S-Mini-revealed-as-new-compact-handheld-with-4-3-display-and-Snapdragon-G3x-Gen-2.1118494.0.html)

### Compute Modules / SOMs
- [Raspberry Pi CM5](https://www.raspberrypi.com/products/compute-module-5/) · [Radxa CM5 / CM5 Lite](https://radxa.com/products/cm/cm5/)
- [Jetson Orin Nano Super Dev Kit](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/) · [Jetson Orin NX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/)
- [Coral Dev Board Mini](https://www.coral.ai/products/dev-board-mini)
- [MNT Reform mainboards / RCM modules](https://shop.mntre.com/t/hardware/reform)

### Cyberdeck-Native and -Adjacent Products
- [ClockworkPi uConsole](https://www.clockworkpi.com/uconsole) · [ClockworkPi DevTerm](https://www.clockworkpi.com/devterm)
- [MNT Pocket Reform](https://shop.mntre.com/products/mnt-pocket-reform) · [MNT Reform Next (Crowd Supply)](https://www.crowdsupply.com/mnt/mnt-reform-next)
- [Framework Laptop 16](https://frame.work/laptop16)
- [Pi Slate community design (CNX Software)](https://www.cnx-software.com/2026/05/11/pi-slate-a-raspberry-pi-5-handheld-linux-cyberdeck-with-a-5-inch-1280x720-touchscreen-display/)
