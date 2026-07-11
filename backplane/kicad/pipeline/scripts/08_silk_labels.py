import pcbnew,sys
def out(s): sys.stdout.write(s+"\n"); sys.stdout.flush()
F="kicad/a7s_backplane_routed.kicad_pcb"
b=pcbnew.LoadBoard(F)
def mm(v): return pcbnew.FromMM(v)
eb=b.GetBoardEdgesBoundingBox(); BCX=(eb.GetLeft()+eb.GetRight())/2
# 1) wipe all loose silk labels + my rings (footprint silk untouched)
rm=[d for d in b.GetDrawings() if (d.GetClass()=='PCB_TEXT' and d.GetLayer() in (pcbnew.F_SilkS,pcbnew.B_SilkS))
    or (d.GetClass()=='PCB_SHAPE' and d.GetShape()==pcbnew.SHAPE_T_CIRCLE and d.GetLayer() in (pcbnew.F_SilkS,pcbnew.B_SilkS))]
for d in rm: b.Remove(d)
out(f"cleared {len(rm)} old loose labels/rings")

CONN={
 "J1":{"m":{"1":"3V3","2":"5V","4":"5V","6":"GND","9":"GND","14":"GND","17":"3V3","20":"GND","25":"GND","30":"GND"},"g":{"6","9","14","20","25","30"},"asm":None,"front":False},
 "J2":{"m":{"1":"PB3","4":"GND","9":"GND","15":"PG5"},"g":{"4","9"},"asm":None,"front":False},
 "A1":{"m":{"5V":"5V","GND":"GND","3V3":"3V3","GP0":"TX","GP1":"RX","GP2":"BTN1","GP3":"BTN2","GP4":"BTN3","GP5":"BTN4","GP6":"BTN5","GP7":"BTN6","GP8":"JSW","GP9":"EA","GP10":"EB","GP11":"ESW","GP26":"JX","GP27":"JY"},"g":{"GND"},"asm":None,"front":False},
 "J3":{"m":{"1":"VCC","2":"GND","3":"CS","4":"RST","5":"DC","6":"SDI","7":"SCK","8":"LED","9":"SDO","10":"TCLK","11":"TCS","12":"TDIN","13":"TDO","14":"TIRQ"},"g":{"2"},"asm":"TFT","front":True},
 "J8":{"m":{"1":"3V3","2":"GND","3":"X","4":"Y","5":"SW"},"g":{"2"},"asm":"JOY","front":False},
 "J10":{"m":{"1":"A","2":"B","3":"SW","4":"GND"},"g":{"4"},"asm":"ENC","front":False},
 "J11":{"m":{"1":"A","2":"B","3":"GND"},"g":{"3"},"asm":"BTN","front":False},
}
OFF=mm(1.5); SZ=0.8; TH=0.15
JL=pcbnew.GR_TEXT_H_ALIGN_LEFT; JR=pcbnew.GR_TEXT_H_ALIGN_RIGHT; JC=pcbnew.GR_TEXT_H_ALIGN_CENTER
def put(x,y,s,layer,mir,just,sz=SZ):
    t=pcbnew.PCB_TEXT(b); t.SetText(s); t.SetLayer(layer); t.SetPosition(pcbnew.VECTOR2I(int(x),int(y)))
    t.SetTextSize(pcbnew.VECTOR2I(mm(sz),mm(sz))); t.SetTextThickness(mm(TH))
    if mir: t.SetMirrored(True)
    t.SetHorizJustify(just); b.Add(t)
for ref,c in CONN.items():
    fp=b.FindFootprintByReference(ref); pads=list(fp.Pads())
    xs=[p.GetPosition().x for p in pads]; ys=[p.GetPosition().y for p in pads]
    xsp=max(xs)-min(xs); ysp=max(ys)-min(ys); cx=sum(xs)/len(xs); cy=sum(ys)/len(ys)
    layer=pcbnew.F_SilkS if c["front"] else pcbnew.B_SilkS; mir=not c["front"]
    single_col = xsp<mm(3); single_row = ysp<mm(3)
    for p in pads:
        k=p.GetNumber()
        if k not in c["m"]: continue
        pp=p.GetPosition(); px,py=pp.x,pp.y
        if single_col:                       # label to interior side, right next to pin
            side=1 if cx<BCX else -1; x=px+side*OFF; y=py
            just=(JL if side>0 else JR); 
            if mir: just=(JR if side>0 else JL)
        elif single_row:                     # label just above pin
            x=px; y=py-OFF; just=JC
        else:                                # 2D block: outward along dominant axis
            if xsp>=ysp:                     # 2 rows -> up/down
                x=px; y=py+(-OFF if py<cy else OFF); just=JC
            else:                            # 2 cols -> left/right
                side=(-1 if px<cx else 1); x=px+side*OFF; y=py
                just=(JR if px<cx else JL)
                if mir: just=(JL if px<cx else JR)
        put(x,y,c["m"][k],layer,mir,just)
        if k in c["g"]:
            r=pcbnew.PCB_SHAPE(b); r.SetShape(pcbnew.SHAPE_T_CIRCLE); r.SetCenter(pp); r.SetEnd(pcbnew.VECTOR2I(px+mm(1.25),py)); r.SetLayer(layer); r.SetWidth(mm(0.2)); b.Add(r)
    if c["asm"]:
        put(cx, min(ys)-mm(2.4), c["asm"], layer, mir, JC, sz=1.0)
    out(f"{ref}: {'col' if single_col else 'row' if single_row else '2D'} relabeled")
pcbnew.SaveBoard(F,b); out("saved")
