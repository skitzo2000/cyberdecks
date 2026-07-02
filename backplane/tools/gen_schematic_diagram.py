#!/usr/bin/env python3
"""
Generate a readable schematic diagram (Graphviz DOT) for the A7S backplane.

This mirrors the connectivity in a7s_backplane_skidl.py (the schematic source of
truth). It is a *documentation* artifact — a bipartite part/net graph grouped and
coloured by function — NOT a KiCad schematic. Render with:

    nix-shell -p graphviz --run \
      "dot -Tsvg tools/a7s_backplane.dot -o a7s_backplane_schematic.svg"

Edit connectivity in a7s_backplane_skidl.py; keep this file in sync by hand (the
dicts below are copied verbatim from that source).
"""

# ---- part -> {pin: net}  (copied from a7s_backplane_skidl.py) ---------------
PARTS = {
    "J1": ("A7S host header\\n2x15 (Conn_02x15)", {
        1: "+3V3_IN", 2: "+5V_IN", 3: "UART3_RX", 4: "+5V_IN", 5: "UART3_TX",
        6: "GND", 7: "A7S_U2TX", 8: "CONSOLE_TX", 9: "GND", 10: "CONSOLE_RX",
        11: "A7S_U2RX", 14: "GND", 16: "RADIO1_CS", 17: "+3V3_IN",
        18: "RADIO1_FLEXB", 19: "SPI_MOSI", 20: "GND", 21: "SPI_MISO",
        23: "SPI_SCK", 24: "TFT_CS", 25: "GND", 26: "TFT_DC", 27: "I2C_SDA",
        28: "I2C_SCK", 29: "TFT_RST", 30: "GND"}),
    "J2": ("A7S host header\\n1x15 (Conn_01x15)", {
        1: "RADIO1_FLEXA", 2: "TOUCH_CS", 3: "TOUCH_IRQ", 4: "GND", 5: "TFT_BL",
        6: "SPARE3", 7: "RADIO2_FLEXA", 8: "RADIO2_CS", 9: "GND",
        10: "RADIO2_FLEXB", 11: "RADIO1_AUX", 12: "RADIO2_AUX", 13: "SPARE0",
        14: "SPARE1", 15: "SPARE2"}),
    "F1": ("Polyfuse F1\\nMF-R050 0.5A (5V)", {1: "+5V_IN", 2: "+5V"}),
    "F2": ("Polyfuse F2\\nMF-R050 0.5A (3V3)", {1: "+3V3_IN", 2: "+3V3"}),
    "C8": ("C8 0.1uF\\nradio1 decouple", {1: "+3V3", 2: "GND"}),
    "C9": ("C9 0.1uF\\nradio2 decouple", {1: "+3V3", 2: "GND"}),
    "J3": ("TFT 2.8\" (J3)\\nConn_01x14", {
        1: "+5V", 2: "GND", 3: "TFT_CS", 4: "TFT_RST", 5: "TFT_DC",
        6: "SPI_MOSI", 7: "SPI_SCK", 8: "TFT_BL", 10: "SPI_SCK", 11: "TOUCH_CS",
        12: "SPI_MOSI", 13: "SPI_MISO", 14: "TOUCH_IRQ"}),
    "J5": ("Radio 1 (J5)\\n2x04 socket", {
        1: "GND", 2: "+3V3", 3: "RADIO1_FLEXA", 4: "RADIO1_CS", 5: "SPI_SCK",
        6: "SPI_MOSI", 7: "SPI_MISO", 8: "RADIO1_FLEXB"}),
    "J6": ("Radio 2 (J6)\\n2x04 socket", {
        1: "GND", 2: "+3V3", 3: "RADIO2_FLEXA", 4: "RADIO2_CS", 5: "SPI_SCK",
        6: "SPI_MOSI", 7: "SPI_MISO", 8: "RADIO2_FLEXB"}),
    "J5b": ("J5b\\nradio1 aux pin", {1: "RADIO1_AUX"}),
    "J6b": ("J6b\\nradio2 aux pin", {1: "RADIO2_AUX"}),
    "A1": ("RP2040-Zero (A1)\\nco-processor", {
        "5V": "+5V", "GND": "GND", "3V3": "RP_3V3", "GP0": "A7S_U2RX",
        "GP1": "A7S_U2TX", "GP2": "BTN1", "GP3": "BTN2", "GP4": "BTN3",
        "GP5": "BTN4", "GP6": "BTN5", "GP7": "BTN6", "GP8": "JOY_SW",
        "GP9": "ENC_A", "GP10": "ENC_B", "GP11": "ENC_SW", "GP26": "JOY_X",
        "GP27": "JOY_Y"}),
    "SW1": ("SW1 button", {1: "BTN1", 2: "GND"}),
    "SW2": ("SW2 button", {1: "BTN2", 2: "GND"}),
    "SW3": ("SW3 button", {1: "BTN3", 2: "GND"}),
    "SW4": ("SW4 button", {1: "BTN4", 2: "GND"}),
    "J8": ("Joystick (J8)\\nConn_01x05", {
        1: "RP_3V3", 2: "GND", 3: "JOY_X", 4: "JOY_Y", 5: "JOY_SW"}),
    "J10": ("Encoder (J10)\\nConn_01x04", {
        1: "ENC_A", 2: "ENC_B", 3: "ENC_SW", 4: "GND"}),
    "J11": ("Buttons 5/6 (J11)\\nConn_01x03", {1: "BTN5", 2: "BTN6", 3: "GND"}),
    "J12": ("Flipper GPIO (J12)\\n1x18 header", {
        1: "+5V", 2: "SPI_MOSI", 3: "SPI_MISO", 4: "SPARE0", 5: "SPI_SCK",
        6: "SPARE1", 7: "SPARE2", 8: "GND", 9: "+3V3", 11: "GND",
        13: "UART3_TX", 14: "UART3_RX", 15: "I2C_SDA", 16: "I2C_SCK",
        17: "SPARE3", 18: "GND"}),
    "TP1": ("TP1\\nconsole TX", {1: "CONSOLE_TX"}),
    "TP2": ("TP2\\nconsole RX", {1: "CONSOLE_RX"}),
}

# ---- net categories -> colour ----------------------------------------------
CATS = {
    "GND":   ("#111111", ["GND"]),
    "5V":    ("#c0392b", ["+5V", "+5V_IN"]),
    "3V3":   ("#e67e22", ["+3V3", "+3V3_IN", "RP_3V3"]),
    "SPI":   ("#2980b9", ["SPI_SCK", "SPI_MOSI", "SPI_MISO"]),
    "I2C":   ("#8e44ad", ["I2C_SDA", "I2C_SCK"]),
    "UART":  ("#16a085", ["UART3_TX", "UART3_RX", "A7S_U2TX", "A7S_U2RX",
                          "CONSOLE_TX", "CONSOLE_RX"]),
    "TFT":   ("#2c3e50", ["TFT_CS", "TFT_DC", "TFT_RST", "TFT_BL",
                          "TOUCH_CS", "TOUCH_IRQ"]),
    "RADIO": ("#7f8c8d", ["RADIO1_CS", "RADIO1_FLEXA", "RADIO1_FLEXB",
                          "RADIO1_AUX", "RADIO2_CS", "RADIO2_FLEXA",
                          "RADIO2_FLEXB", "RADIO2_AUX"]),
    "INPUT": ("#27ae60", ["BTN1", "BTN2", "BTN3", "BTN4", "BTN5", "BTN6",
                          "JOY_X", "JOY_Y", "JOY_SW", "ENC_A", "ENC_B",
                          "ENC_SW"]),
    "SPARE": ("#95a5a6", ["SPARE0", "SPARE1", "SPARE2", "SPARE3"]),
}
NET_COLOR = {net: color for color, nets in CATS.values() for net in nets}

# part functional clusters (ref -> group)
CLUSTERS = {
    "HOST (A7S)": ["J1", "J2"],
    "POWER": ["F1", "F2", "C8", "C9"],
    "DISPLAY": ["J3"],
    "RADIOS": ["J5", "J6", "J5b", "J6b"],
    "CO-PROCESSOR + INPUTS": ["A1", "SW1", "SW2", "SW3", "SW4", "J8", "J10", "J11"],
    "EXPANSION / CONSOLE": ["J12", "TP1", "TP2"],
}


def esc(s):
    return s.replace('"', '\\"')


def main():
    import sys
    use_clusters = "--no-clusters" not in sys.argv
    out = "tools/a7s_backplane_flat.dot" if not use_clusters else "tools/a7s_backplane.dot"
    all_nets = sorted({n for _, pins in PARTS.values() for n in pins.values()})
    lines = [
        "graph a7s_backplane {",
        '  rankdir=LR; splines=true; overlap=false; nodesep=0.28; ranksep=1.4;',
        '  bgcolor="white";',
        '  fontname="DejaVu Sans"; fontsize=22; labelloc="t";',
        '  label="A7S Cyberdeck Backplane — connectivity diagram\\n'
        '(generated from a7s_backplane_skidl.py — the schematic source of truth)";',
        '  node [fontname="DejaVu Sans"];',
        '  edge [fontname="DejaVu Sans", fontsize=8];',
    ]

    # part nodes, grouped in clusters (clusters honoured only by dot)
    for ci, (title, refs) in enumerate(CLUSTERS.items()):
        if use_clusters:
            lines.append(f'  subgraph cluster_{ci} {{')
            lines.append(f'    label="{title}"; style="rounded,filled"; '
                         f'fillcolor="#f4f6f8"; color="#b0b8c0"; fontsize=16;')
        for ref in refs:
            desc = PARTS[ref][0]
            lines.append(f'    "{ref}" [shape=box, style="filled,rounded", '
                         f'fillcolor="#dfe7ef", color="#34495e", '
                         f'label="{esc(desc)}"];')
        if use_clusters:
            lines.append("  }")

    # net nodes
    for net in all_nets:
        color = NET_COLOR.get(net, "#555555")
        shape = "box" if net in ("GND",) else "ellipse"
        lines.append(f'  "net_{net}" [shape={shape}, style=filled, '
                     f'fillcolor="{color}", fontcolor="white", fontsize=10, '
                     f'label="{net}"];')

    # edges: part-pin -> net
    for ref, (_, pins) in PARTS.items():
        for pin, net in pins.items():
            color = NET_COLOR.get(net, "#555555")
            lines.append(f'  "{ref}" -- "net_{net}" '
                         f'[label="{pin}", color="{color}"];')

    lines.append("}")
    dot = "\n".join(lines)
    with open(out, "w") as f:
        f.write(dot)
    print(f"wrote {out}  ({len(PARTS)} parts, {len(all_nets)} nets)")


if __name__ == "__main__":
    main()
