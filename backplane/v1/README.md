# A7S Backplane — v1 ARCHIVE (do not fabricate)

Superseded boards, kept for reference and diff only. **The current board is [v2](../README.md)** in the
parent folder.

Everything here shares the same electrical design (netlist/schematic/BOM) as v2 — see the shared docs in
the parent: [`../SCHEMATIC.md`](../SCHEMATIC.md), [`../BACKPLANE-DESIGN.md`](../BACKPLANE-DESIGN.md),
[`../BOM-SHIELD.md`](../BOM-SHIELD.md).

## Why these are dead

Both v1 boards mated the A7S GPIO headers **mirrored** (shield socket pin 1 landed on A7S pin 30), which
shorted the A7S **+3V3 onto shield GND** — the SBC went dark the moment the shield was seated. That header-
mate bug was only caught and fixed in **v2**. Do not fab anything in this folder.

| | Board | Fab | Notes |
|---|---|---|---|
| **rev1** ([REV1.md](REV1.md)) | `kicad/a7s_backplane_render.kicad_pcb` | `kicad/gerbers/` | original layout — A7S ports faced *inward* into the radios |
| **rev2** ([REV2.md](REV2.md)) | `kicad/a7s_backplane_rev2.kicad_pcb` | `kicad/gerbers_rev2/`, `kicad/fab_rev2/` | mechanical respin (ports out, mount shifted) — **still had the header-mirror short** |

> Note: `REV1.md` / `REV2.md` were written before the header-mirror bug was understood, so their
> "verified / ready to fab" language is wrong — both are DOA. Links in them to `../SCHEMATIC.md` etc.
> now sit one level up.
