# Cyberdeck Chassis, Enclosures, and Pre-Built Decks — 2026 Buyer's Guide

The chassis is the most defining decision in a cyberdeck build. It dictates form factor, thermals, weight budget, antenna placement, and most of all what the thing looks like. This guide covers the eight buying paths the r/cyberDeck and Hackaday communities use in 2026, plus a decision framework at the end.

All prices are USD, observed roughly May 2026.

## 1. Open-Source 3D-Printable Designs (Community Classics)

| Design | Designer / Source | Target Compute | Filament | Status (2026) | Notes |
|---|---|---|---|---|---|
| **Penkesu Computer** | Penk Chen — [penkesu.computer](http://penkesu.computer/), [GitHub](https://github.com/penk/penkesu) | RPi Zero 2 W | ~$5 | Active, widely remixed | 7.9" widescreen clamshell, GBA SP hinges, ortholinear 48-key MX. The reference "homebrew laptop." |
| **Decktility** | jspark311 — [Hackaday.io](https://hackaday.io/project/172078-3d-printed-cyberdeck) | RPi CM4 | ~$10 | Active; STLs + STEP shared | Palm-III/HC-4500 vibe, 3.5" IPS, custom power board. |
| **tinyDeck / Mini-Deck** | wallcomputer — [Hackster](https://www.hackster.io/wallcomputer/tinydeck-667c1f) | RPi Zero 2 W | ~$3 | Stable, niche | Pocket "brick" console-mode deck. |
| **Cyberboy 1.0** | Rubfer — [Hackster](https://www.hackster.io/news/rubfer-s-3d-printed-cyberboy-1-0-puts-a-raspberry-pi-5-in-the-palm-of-your-hand-abfa930f15e7) | RPi 5 8 GB | ~$8 | Active 2025–2026 | 4.3" 800×480 + small QWERTY; rare palm-sized RPi 5 build with sane thermals. |
| **HAMDECK** | sjm4306 — [Hackaday.io](https://hackaday.io/project/191890-hamdeck-cyberdeck/details) | RPi 4/5 + SDR | ~$15 | Active, ham-focused | SDR pass-throughs + antenna ports. |
| **Vecdec** | svenscore — [Hackaday writeup](https://hackaday.com/2024/11/19/the-vecdec-cyberdeck-is-more-than-a-pretty-case/) | RPi 4/5 | ~$12 | Active 2024–2026 | Slanted-keyboard slab, permissive license. |
| **TechNIK's Cyberdeck** | Nik Reitmann — [Printables](https://www.printables.com/model/551922-techniks-cyberdeck) | RPi 4 | ~$10 | Stable | Most-downloaded clean slab STL. |
| **Modular OTS Cyberdeck Kit** | bigCATdesigns — [Hackaday.io](https://hackaday.io/project/187584-modular-ots-cyberdeck-creation-kit) | RPi 4/5, ITX | ~$25 | Active | Printable shell around OTS KB + hub; clip-on modules. |
| **Keigen7 2024** | Keigen7 — [Hackster](https://www.hackster.io/news/keigen7-s-sleek-3d-printed-raspberry-pi-4-cyberdeck-rings-in-2024-in-style-4f81c6c29d2a) | RPi 4 + ultrawide | ~$18 | Active | Two-half "friction-welded" body. |
| **Pip-Boy 3000 Mark IV** | Ytec3D — [ytec3d.com/pip-boy-3000-mark-iv](https://ytec3d.com/pip-boy-3000-mark-iv/) | RPi Zero/Pico + LEDs | ~$25 | Active, defining wearable | Three sizes; de facto Pip-Boy reference. |
| **Predicta-style CRT decks** | various — see [Hackaday CRT writeup](https://hackaday.com/2026/03/20/portable-crt-tv-becomes-retro-cyberdeck/) | RPi + HDMI→RF | varies | Active novelty | Around Predicta/Panasonic TR-545 CRTs. |

**Likely abandoned in 2026:** ZeroDeck, Brutus, Z-Cyber, ANubis — repos last updated 2022–2023; files print but assume no support.

Browse: [Printables /tag/cyberdeck](https://www.printables.com/tag/cyberdeck), [Hackaday.io cyberdecks list](https://hackaday.io/list/180088-cyberdecks).

## 2. Surplus / Rugged Commercial Cases (Donor Builds)

| Case | Interior (in) | Weight | Material | Fits | Street Price | Pros / Cons |
|---|---|---|---|---|---|---|
| **Pelican 1150** | 8.1×4.7×3.4 | 1.4 lb | Copolymer PP | RPi + 5" display + battery | $50–65 | Smallest "real" Pelican. // Tight for keyboards. |
| **Pelican 1200** | 9.3×7.0×4.1 | 2.2 lb | Copolymer PP | 7" display + 60% KB | $65–85 | Sweet spot. // Lid eats display real estate. |
| **Pelican 1300** | 9.2×7.0×6.1 | 2.9 lb | Copolymer PP | Deep — battery + ITX | $75–95 | Vertical depth for stacks. // Bulky. |
| **Pelican 1400** | 11.8×8.9×5.2 | 4.0 lb | Copolymer PP | 10" display + full KB | $115–145 | Classic mid-size deck shell. // Heavy. |
| **Pelican 1450** | 14.6×10.2×4.9 | 5.0 lb | Copolymer PP | 11.6" laptop + KB | $135–170 | Briefcase deck reference. // Bag-dominant. |
| **Pelican Storm iM2050** | 9.5×7.5×4.3 | 2.6 lb | HPX | 7" display + KB | $75–100 | Press-pull latches, IP67. |
| **Apache 2800** | 11.6×7.0×3.4 | 2.3 lb | PP | 7" deck w/ KB | **$30** [Harbor Freight](https://www.harborfreight.com/2800-weatherproof-protective-case-medium-black-64551.html) | Cheap Pelican clone, IP65. |
| **Apache 3800** | 14.6×8.0×4.9 | 3.4 lb | PP | Full clamshell, 10" | **$40** HF | Best $/L on this list. |
| **Apache 4800** | 18.0×13.0×6.8 | 5.6 lb | PP | Full KB + 13" | **$60** [HF](https://www.harborfreight.com/4800-weatherproof-protective-case-x-large-green-56863.html) | Rolling/large. // Impractical hand-carry. |
| **Nanuk 905** | 9.4×7.4×5.5 | 2.6 lb | NK-7 | 7" deck + battery | $80–100 [nanuk.com](https://nanuk.com/products/nanuk-905) | PowerClaw latches. // Premium price. |
| **Nanuk 910** | 10.2×7.0×3.7 | 1.9 lb | NK-7 | Slim 7" deck | $75–95 [nanuk.com](https://nanuk.com/products/nanuk-910) | Slimmer than 905. |
| **Plano 1404** | 13.6×8.3×4.6 | ~3 lb | PP | 10" mid deck | $30–45 | Cheapest "looks-the-part." // Foam crumbles. |
| **MTM Survivor** | 7.3×4.8×3.0 | 1.2 lb | PP | Tiny RPi Zero deck | $20–30 | Pocket-sized waterproof. |
| **Maxpedition Mini Pocket Organizer** | 8×6×3 (soft) | 0.7 lb | Cordura | Soft handhelds, Beepy-class | $35–55 | Light, MOLLE-compatible. // No impact protection. |

**Display sizing rule of thumb:** a 7" 1024×600 needs ~7.0×4.5" of lid; a 10.1" needs ~9.5×6.3". Allow ~0.3" for HDMI display + driver, ~0.5" for Pi + heatsink, ~0.7"+ for 18650 pack.

## 3. Surplus Military / Industrial Enclosures

| Case | Approx Size | Weight | Sources | Price | Notes |
|---|---|---|---|---|---|
| **M.U.L.E. transit case** | varies | 8–25 lb | eBay, [GovDeals](https://www.govdeals.com), [GovPlanet](https://www.govplanet.com/) | $40–150 | Aluminum shipping cases for radios/optics. |
| **PRC-77/PRC-25 radio cases** | ~12×10×4 | 4 lb empty | eBay, hamfests | $30–80 | Iconic OD-green. Often missing batt sleds. |
| **Hardigg / Pelican-Hardigg shipping** | many | 5–40 lb | GovDeals, eBay | $50–300 | Roto-molded. Hardigg merged into Pelican 2008. |
| **Pre-Pelican Storm Case** | mid | 2–5 lb | eBay, surplus | $30–70 | Identical to current iM-series, cheaper. |
| **Surplus Tek/HP instrument covers** | varies | varies | eBay, hamfests | $20–100 | Mil-aluminum boxes, rackmount-style decks. |

**Sourcing tips:** eBay search "rugged transit case empty," "AN/PRC case," "Pelican-Hardigg." GovDeals / GovPlanet auction in lots. Hamfests have the best radio cases.

## 4. Kit / Semi-Finished Cyberdeck Chassis

| Kit | Vendor | Includes | Price (2026) | Status |
|---|---|---|---|---|
| **Penkesu kit** | community (Tindie/Etsy) | Printed shell, hinges, MX plate | $90–140 | Sporadic, no official Penk Chen kit |
| **Tinydeck kit** | Hackster sellers | Printed shell + screen mount | $40–80 | Niche hobbyist |
| **HackberryPi Q10/Q20/9900** | ZitaoTech via [Tindie](https://www.tindie.com/products/zitaotech/hackberrypi-cyberdeck-handheld-with-q20-keyboard/) / [Elecrow](https://www.elecrow.com/hackberrypi-zero-with-bbq20-keyboard.html) | Shell, PCB, BB KB, 4" display | $125–160 | **Elecrow now primary channel** |
| **Pi Slate (assembled)** | [Carbon Computers](https://carboncomputers.us/collections/cyberdeck) | RPi 5, 5" 1280×720, RGB KB, 10Ah | $424–707 | In stock |
| **CyberDeck Pi** | Carbon Computers | RPi 5 8GB + KB + display + NVMe | $399–599 | In stock |
| **MNT Pocket Reform** | [MNT shop](https://shop.mntre.com/products/mnt-pocket-reform) | Assembled, PCB-modular | €1,399 | Active |

**Bondi/Pajaro Forge note:** No consistent retail listing in May 2026. Verify the seller is the actual designer before buying — counterfeits and remixed STLs are common.

## 5. Pre-Built Deck-Like Computers ("Buy Not Build")

| Product | Form Factor | CPU | Display | Price (2026) | Status | Source |
|---|---|---|---|---|---|---|
| **ClockworkPi uConsole (CM4 Lite)** | Slab w/ thumb-KB | RPi CM4 | 5" 1280×720 | $249 | In stock | [clockworkpi.com](https://www.clockworkpi.com/uconsole) |
| **ClockworkPi uConsole (CM5)** | Same | RPi CM5 | 5" | ~$299 + module | Community-supported, heat caveats | [forum thread](https://forum.clockworkpi.com/t/cm5-is-here-just-released/14961) |
| **ClockworkPi DevTerm A06** | Wedge typewriter | RK3399 hex | 6.86" 1280×480 + thermal printer | $399 | **Out of stock May 2026** | [A06](https://www.clockworkpi.com/product-page/devterm-kit-a06-series) |
| **DevTerm A04** | Wedge | RK3399 quad | Same | $339 | **Out of stock** | [A04](https://www.clockworkpi.com/product-page/devterm-kit-a0402) |
| **DevTerm R-01** | Wedge | Allwinner D1 RISC-V | Same | $239 | **Out of stock; experimental** | [R-01](https://www.clockworkpi.com/product-page/devterm-kit-r01) |
| **MNT Reform (classic)** | OSHW laptop | RK3588/iMX8MQ modules | 12.5" | $1,099+ | Active, hand-built in Berlin | [shop.mntre.com](https://shop.mntre.com/products/mnt-reform) |
| **MNT Pocket Reform** | 7" subnotebook | RK3588 module | 7" | €1,399 (~$1,500) | Active | [Pocket Reform](https://shop.mntre.com/products/mnt-pocket-reform) |
| **MNT Reform Next** | 12.5" laptop, more modular | RK3588 8-core + Mali G610 | 12.5" | $1,099 / $1,399 / $1,599 | Crowd Supply, ships **June 5 2026** | [Crowd Supply](https://www.crowdsupply.com/mnt/mnt-reform-next) |
| **Mecha Comet (i.MX 8M Plus)** | Modular AMOLED handheld | i.MX 8M Plus quad A53 | 3.92" AMOLED 441 ppi | $189 early-bird | Ships May/June 2026 | [mecha.so/comet](https://mecha.so/comet) |
| **Mecha Comet (i.MX 95)** | Same | i.MX 95 6×A55 | Same | $269 | Ships Sept 2026 | Same |
| **Beepy (BeepBerry)** | Palm pager w/ BB KB | RPi Zero/2 W (user) | 2.7" Sharp Memory LCD | $79 board, ~$120 built | Kit | [beepy.sqfmi.com](https://beepy.sqfmi.com/) |
| **HackberryPi Q20** | Palm w/ BB Q20 KB | RPi Zero 2 W | 4" 720×720 | $127 | Active via Elecrow | [Tindie](https://www.tindie.com/products/zitaotech/hackberrypi-cyberdeck-handheld-with-q20-keyboard/) |
| **M5Stack Cardputer Adv** | Credit-card form | ESP32-S3 | 1.14" LCD | $30 | In stock | [M5Stack](https://shop.m5stack.com/products/m5stack-cardputer-adv-version-esp32-s3) |
| **Anbernic RG35XX H/Pro** | Retro handheld (Linux) | Allwinner H700 quad A53 | 3.5" IPS 640×480 | $60–80 | In stock | [anbernic.com](https://anbernic.com/products/rg35xx-h) |
| **Pi Slate** | 5" slab | RPi 5 | 5" 1280×720 touch | $424–707 | In stock | [CNX](https://www.cnx-software.com/2026/05/11/pi-slate-a-raspberry-pi-5-handheld-linux-cyberdeck-with-a-5-inch-1280x720-touchscreen-display/) |

## 6. CAD / Fabrication Services for Custom Shells

| Service | Sweet Spot | Min | ~200×150 mm aluminum shell, 2 mm |
|---|---|---|---|
| **[SendCutSend](https://sendcutsend.com/)** | 2D laser-cut + CNC bending, US runs | $30/part | $60–120 per panel |
| **[PCBWay CNC](https://www.pcbway.com/rapid-prototyping/cnc-machining/)** | 3-axis CNC, ~25 finishes | $45–75 auto-quote | Full enclosure $257–334 ([Hackaday case study](https://hackaday.io/project/190831/log/224322-a-pcbway-cnc-fabrication-costs-usd257-334)) |
| **JLCPCB CNC** | Was cheap; **2025 price hike** ([EEVblog](https://www.eevblog.com/forum/manufacture/huge-increase-in-jlcpcb-cnc-prices/)) | ~$100 | Comparable to PCBWay now |
| **[Xometry](https://www.xometry.com/)** | US, fast turn, ISO certs | $100+ practical | $300–600 small case |
| **[Ponoko](https://www.ponoko.com/)** | Laser-cut sheet panels, flat only | ~$20 | $40–80 face plate |
| **Shapeways** | Back as Manuevo BV ([recap](https://www.voxelmatters.com/shapeways-files-for-bankruptcy/)) | $25 | SLS nylon $80–200 |

**Realistic aluminum-shell budget** for a 4-piece bent CNC case w/ cutouts: $180–350 at PCBWay or SendCutSend, ready to anodize. +$40 for bead-blast + anodize. +$50–100 for engraved Ponoko face plate.

## 7. Filament for Cyberdeck Cases

| Filament | Tg | Print difficulty | Best Use | Avoid When |
|---|---|---|---|---|
| **PLA** | ~60 °C | Easy | Photo props, test prints | Sealed case w/ RPi 5 |
| **PETG** | ~80 °C | Easy | Default 90% pick — handles 40–60 °C interior | Sustained 100% CPU, no fan |
| **PETG-CF** | ~85 °C | Easy w/ hardened nozzle | Stiffer, hides layers | Need transparency / food-safe |
| **ASA** | ~105 °C | Hard, warps | Outdoor / UV / RV-grade | Open-frame printers |
| **ABS** | ~105 °C | Hard, fumes | Acetone-smoothing aesthetic | No ventilation |
| **PC** | ~110–120 °C | Very hard | Mil-spec deck w/ N100 or fanless x86 | Casual hobbyist |
| **PC-CF / PA6-CF** | ~110–150 °C | Very hard, dry-storage critical | Premium aerospace-grade | Anything less than Bambu X1C / Voron / Prusa XL |

**Practical 2026 recommendation:** PETG for 90% of builds; PETG-CF for matte finish; ASA for outdoor; PC only above 80 °C. Quality brands: Polymaker, Prusament, Bambu Lab, Atomic Filament. Avoid unbranded eBay/Amazon PETG.

## 8. Mounting / Hardware Miscellanea

**Heat-set inserts (essential):**
- **Ruthex** RX-M3x5.7 (~$15/100) — community standard. [ruthex.de](https://www.ruthex.de/) / [Amazon](https://www.amazon.com/ruthex-Threaded-Insert/dp/B09ZT574SV)
- **Ruthex RX-M2.5x5.7** (~$15/70) — for display bezels
- **Ruthex assortment box** (~$45)
- **Voxelab/generic on AliExpress** ($5–8/100) — fine for non-load-bearing

**Standoffs:** M2.5 M-F brass/nylon from McMaster, Adafruit, or AliExpress assortment ($15–25/270pc). RPi mounting hole is M2.5.

**Hinges:**
- **Penkesu uses GBA SP hinges** — AliExpress "GBA SP hinge replacement" (~$3/pair) or [iFixit](https://www.ifixit.com/Parts/Game_Boy_Advance_SP)
- **7" laptop hinges** — AliExpress "mini laptop hinge 7 inch" / "netbook hinge"; Acer Aspire One / Eee PC pulls $5–12/pair
- **Continuous (piano)** — McMaster 1597A series for milled aluminum

**Latches:** Sugatsune toggle ($8–15 ea); Southco draw ($4–10).

**Gaskets:** EPDM 1–2 mm strip (~$10/10 m AliExpress); Pelican replacement O-rings direct.

**Antenna pass-throughs (critical for metal chassis):**
- SMA bulkhead connectors ($2–5)
- U.FL→RP-SMA pigtails ($3–8 Adafruit/Digi-Key)
- **Always plan a non-metallic window** — even a plastic insert in one corner saves Wi-Fi.

---

## How to Choose

### Build-vs-Buy Decision Tree
1. Want to design or use? "Use" → §5; uConsole CM4, Pocket Reform, or Mecha Comet are the three most pragmatic 2026 buys.
2. Own a 3D printer? No → §2 surplus case. Yes → §1 community STL + Ruthex.
3. Appearance over function? Yes → §6 CNC aluminum, $200–400. No → Apache 3800 + RPi 5, $80.
4. Outdoor/field? ASA/PC printed or Nanuk; never PLA, never bare aluminum without gasket.
5. Wearable? Pip-Boy 3000 Mark IV STL or Mecha Comet w/ wrist strap.

### Form-Factor Archetypes

| Archetype | Examples | Typical Mass | Strengths | Weaknesses |
|---|---|---|---|---|
| Slab | TechNIK, Vecdec, Cyberboy | 600–1,200 g | Cheap, easy, photogenic | No tilt, fragile screen |
| Clamshell | Penkesu, Pocket Reform, DevTerm | 700–1,500 g | Protects screen, real typing | Hinge failures |
| Handheld | uConsole, HackberryPi, Beepy, Comet | 200–500 g | Pocketable, one-handed | Small screen, thermal-limited |
| Wearable | Pip-Boy, wrist Mecha | 300–700 g | Always-with-you | Heat on skin, awkward typing |
| Briefcase | Pelican 1400/1450 | 2–5 kg | Indestructible, antenna-friendly | Heavy, cable-drawer vibe |
| Rackmount | Hardigg, surplus instrument | 5–15 kg | Modular, big screen/battery | Not portable |

### Heat Management
Even passive RPi 5 hits 70 °C in a sealed PETG case under load.
- **Heatsinks:** Geekworm full-aluminum P15/P165 ($10–15) for RPi 4/5
- **Fans:** 30 mm 5 V Noctua NF-A4x10 5V ($15) — only fan worth using
- **Ventilation:** louvered side + opposite intake; stack effect
- **CPU choice:** N100 produces 4–6× the heat of RPi 5 — fan required
- **Thermal pads, not paste**, between SoC and chassis if case is the heatsink

### Antenna Pass-Through
Aluminum/copper/steel kill Wi-Fi/BT/cellular. Three fixes: (1) external SMA bulkhead, (2) plastic window, (3) internal antenna in a printed sub-shell protruding through. Skipping this is the #1 reason a beautiful aluminum cyberdeck has terrible Wi-Fi.

### Weight Budget
- Pocket: <350 g (Beepy, Cardputer, small HackberryPi)
- Sling: 350–1,200 g (most slabs/clamshells)
- Backpack: 1.2–3 kg (Pelican 1200/1300)
- Desk-only: 3 kg+ (Pelican 1450, mil cases, rackmount)

Rule: heavier than a 14" laptop (~1.4 kg) → must do something a laptop can't.

## TL;DR Recommendations
- **First build, low budget:** Apache 3800 ($40) + RPi 5 + 7" HDMI. Under $200.
- **First build, pretty:** Print Vecdec or Cyberboy 1.0 in PETG-CF, ~$30 filament + Pi 5.
- **Skip building:** ClockworkPi uConsole CM4 Lite ($249) — best price/experience of any 2026 finished deck.
- **Power user:** MNT Pocket Reform (€1,399) or Reform Next ($1,099+).
- **Pocketable hacker tool:** Beepy ($79 kit), Cardputer Adv ($30), or HackberryPi Q20 ($127).
- **Wearable / cosplay:** Ytec3D Pip-Boy 3000 Mark IV + RPi Zero.
- **Field deck:** Pelican 1200 or Nanuk 905 + RPi CM4 carrier, SMA antenna passthroughs.

## Sources
- [Penkesu Computer](http://penkesu.computer/) · [GitHub](https://github.com/penk/penkesu) · [MagPi feature](https://magazine.raspberrypi.com/articles/penkesu-computer)
- [Decktility](https://hackaday.io/project/172078-3d-printed-cyberdeck) · [Liliputing writeup](https://liliputing.com/raspberry-pi-based-decktility-cyberdeck-is-inspired-by-a-love-of-90s-handhelds/)
- [tinyDeck](https://www.hackster.io/wallcomputer/tinydeck-667c1f) · [Vecdec on Hackaday](https://hackaday.com/2024/11/19/the-vecdec-cyberdeck-is-more-than-a-pretty-case/) · [TechNIK Printables](https://www.printables.com/model/551922-techniks-cyberdeck) · [HAMDECK](https://hackaday.io/project/191890-hamdeck-cyberdeck/details) · [Modular OTS Kit](https://hackaday.io/project/187584-modular-ots-cyberdeck-creation-kit) · [Cyberboy 1.0](https://www.hackster.io/news/rubfer-s-3d-printed-cyberboy-1-0-puts-a-raspberry-pi-5-in-the-palm-of-your-hand-abfa930f15e7) · [Ytec3D Pip-Boy](https://ytec3d.com/pip-boy-3000-mark-iv/)
- [Pelican cases](https://www.pelican.com/us/en/products/cases) · [Apache 2800](https://www.harborfreight.com/2800-weatherproof-protective-case-medium-black-64551.html) · [Apache 4800](https://www.harborfreight.com/4800-weatherproof-protective-case-x-large-green-56863.html) · [Nanuk 905](https://nanuk.com/products/nanuk-905)
- [uConsole](https://www.clockworkpi.com/uconsole) · [CM5 forum thread](https://forum.clockworkpi.com/t/cm5-is-here-just-released/14961) · [DevTerm A06](https://www.clockworkpi.com/product-page/devterm-kit-a06-series)
- [MNT Reform](https://shop.mntre.com/products/mnt-reform) · [Pocket Reform](https://shop.mntre.com/products/mnt-pocket-reform) · [Reform Next](https://www.crowdsupply.com/mnt/mnt-reform-next) · [Tom's Hardware on Reform Next](https://www.tomshardware.com/laptops/mnt-reform-next-open-source-modular-laptop-crowdfunder-goes-live-for-usd1-099)
- [Mecha Comet](https://mecha.so/comet) · [CNX writeup](https://www.cnx-software.com/2026/01/25/mecha-comet-is-an-open-source-hardware-modular-linux-handheld-computer/)
- [Beepy](https://beepy.sqfmi.com/) · [Hackaday review](https://hackaday.com/2023/08/07/review-beepy-a-palm-sized-linux-hacking-playground/) · [HackberryPi Q20 Tindie](https://www.tindie.com/products/zitaotech/hackberrypi-cyberdeck-handheld-with-q20-keyboard/) · [ZitaoTech GitHub](https://github.com/ZitaoTech/Hackberry-Pi_Zero)
- [Cardputer Adv](https://shop.m5stack.com/products/m5stack-cardputer-adv-version-esp32-s3) · [Anbernic RG35XX H](https://anbernic.com/products/rg35xx-h) · [Pi Slate CNX](https://www.cnx-software.com/2026/05/11/pi-slate-a-raspberry-pi-5-handheld-linux-cyberdeck-with-a-5-inch-1280x720-touchscreen-display/) · [Carbon Computers](https://carboncomputers.us/collections/cyberdeck)
- [SendCutSend](https://sendcutsend.com/) · [PCBWay CNC](https://www.pcbway.com/rapid-prototyping/cnc-machining/) · [Hackaday PCBWay case study](https://hackaday.io/project/190831/log/224322-a-pcbway-cnc-fabrication-costs-usd257-334) · [JLCPCB price hike](https://www.eevblog.com/forum/manufacture/huge-increase-in-jlcpcb-cnc-prices/) · [Shapeways bankruptcy](https://www.voxelmatters.com/shapeways-files-for-bankruptcy/)
- [Prusament PETG-CF](https://www.prusa3d.com/product/prusament-petg-carbon-fiber-black-1kg-nfc/) · [Ruthex M3](https://www.ruthex.de/) · [Ruthex Amazon](https://www.amazon.com/ruthex-Threaded-Insert/dp/B09ZT574SV) · [iFixit GBA SP parts](https://www.ifixit.com/Parts/Game_Boy_Advance_SP)
- [GovDeals](https://www.govdeals.com) · [GovPlanet](https://www.govplanet.com/) · [Hackaday cyberdeck tag](https://hackaday.com/tag/cyberdeck/) · [Printables /tag/cyberdeck](https://www.printables.com/tag/cyberdeck)
