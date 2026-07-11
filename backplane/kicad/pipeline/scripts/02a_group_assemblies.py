import pcbnew,sys
F="kicad/a7s_backplane_place.kicad_pcb"
b=pcbnew.LoadBoard(F)
out=lambda s:(sys.stdout.write(s+"\n"),sys.stdout.flush())

# integrity: every footprint's pads belong to it (rule out 'exploded' parts)
out("footprint pad counts:")
for fp in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
    out(f"   {fp.GetReference():5} {len(list(fp.Pads()))} pads  {fp.GetFPIDAsString().split(':')[-1]}")

GROUPS={
 "A7S":["J1","J2","H1","H2","H3","H4"], "RP2040":["A1"], "TFT":["J3"],
 "BUTTONS":["SW1","SW2","SW3","SW4"], "FLIPPER":["J12"],
 "RADIO1":["J5","J5b"], "RADIO2":["J6","J6b"],
 "JOYSTICK":["J8"], "ENCODER":["J10"], "BTN56":["J11"],
 "C1":["C1"], "C2":["C2"], "F1":["F1"], "F2":["F2"], "TP1":["TP1"], "TP2":["TP2"],
}
for g in list(b.Groups()): b.Remove(g)
for fp in b.GetFootprints(): fp.SetLocked(False)
allrefs=set()
for name,refs in GROUPS.items():
    grp=pcbnew.PCB_GROUP(b); grp.SetName(name); b.Add(grp)
    for ref in refs:
        fp=b.FindFootprintByReference(ref)
        if fp: grp.AddItem(fp); allrefs.add(ref)
    if name=="A7S":
        for d in b.GetDrawings():
            if d.GetLayer()==pcbnew.Dwgs_User: d.SetLocked(False); grp.AddItem(d)
missing=[fp.GetReference() for fp in b.GetFootprints() if fp.GetReference() not in allrefs]
out("\nUNGROUPED footprints: "+(", ".join(missing) if missing else "NONE - every part grouped"))
pcbnew.SaveBoard(F,b); out("saved")
