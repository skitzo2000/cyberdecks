import pcbnew,sys
F="kicad/a7s_backplane_place.kicad_pcb"
b=pcbnew.LoadBoard(F)
def out(s): sys.stdout.write(s+"\n"); sys.stdout.flush()
NEW={"JOYSTICK":["J8"],"ENCODER":["J10"],"BTN56":["J11"],
     "C1":["C1"],"C2":["C2"],"F1":["F1"],"F2":["F2"],"TP1":["TP1"],"TP2":["TP2"]}
existing={g.GetName() for g in b.Groups()}
for name,refs in NEW.items():
    if name in existing: continue
    grp=pcbnew.PCB_GROUP(b); grp.SetName(name); b.Add(grp)
    for r in refs:
        fp=b.FindFootprintByReference(r)
        if fp: grp.AddItem(fp)
    out("added group "+name)
out("saving...")
pcbnew.SaveBoard(F,b)
out("SAVE OK")
