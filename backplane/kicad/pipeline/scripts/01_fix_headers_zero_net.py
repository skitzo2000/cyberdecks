import pcbnew, sys
SRC="kicad/a7s_backplane_render.kicad_pcb"      # clean, fully-placed source
OUT="kicad/a7s_backplane_place.kicad_pcb"
b=pcbnew.LoadBoard(SRC)
def mm(v): return pcbnew.FromMM(v)
def V(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))
out=lambda s:(sys.stdout.write(s+"\n"),sys.stdout.flush())

# ---- 1) correct header orientation (centered on hole line, per confirmed spec) ----
H={h.GetReference():(pcbnew.ToMM(h.GetPosition().x),pcbnew.ToMM(h.GetPosition().y)) for h in b.GetFootprints() if h.GetReference().startswith("H")}
bc=((H["H3"][0]+H["H2"][0])/2,(H["H3"][1]+H["H2"][1])/2)
def centroid(ref):
    fp=b.FindFootprintByReference(ref); ps=list(fp.Pads())
    return (sum(pcbnew.ToMM(p.GetPosition().x) for p in ps)/len(ps), sum(pcbnew.ToMM(p.GetPosition().y) for p in ps)/len(ps))
def orient_center(ref,cx,cy,orient):
    fp=b.FindFootprintByReference(ref); fp.SetOrientationDegrees(orient)
    ps=list(fp.Pads()); ccx=sum(p.GetPosition().x for p in ps)/len(ps); ccy=sum(p.GetPosition().y for p in ps)/len(ps)
    fp.Move(pcbnew.VECTOR2I(int(mm(cx)-ccx),int(mm(cy)-ccy)))
j1t=(2*bc[0]-centroid("J1")[0], 2*bc[1]-centroid("J1")[1])
j2t=(2*bc[0]-centroid("J2")[0], 2*bc[1]-centroid("J2")[1])
orient_center("J1", j1t[0], j1t[1], 270)   # J1->north, pin1/2 west
orient_center("J2", j2t[0], j2t[1], 90)     # J2->south, pin15 west
out(f"headers set: J1 center~{tuple(round(v,1) for v in j1t)} J2~{tuple(round(v,1) for v in j2t)}")

# ---- 2) strip routing + nets (clean placement canvas) ----
tr=list(b.GetTracks())
for t in tr: b.Remove(t)
np=0
for fp in b.GetFootprints():
    for p in fp.Pads(): p.SetNetCode(0); np+=1
out(f"removed {len(tr)} tracks, zeroed {np} pads")

# ---- 3) lock every footprint so it selects/moves as one solid unit ----
nl=0
for fp in b.GetFootprints(): fp.SetLocked(True); nl+=1
out(f"locked {nl} footprints")

# ---- 4) A7S reference overlay on Dwgs.User, LOCKED (won't interfere with selection) ----
a=(H["H4"][0]-H["H3"][0])/(23.99-(-19.81)); bX=H["H3"][0]-a*(-19.81)
c=(H["H1"][1]-H["H3"][1])/(-76.98-(-33.18)); dY=H["H3"][1]-c*(-33.18)
def S(sx,sy): return (a*sx+bX, c*sy+dY)
LY=pcbnew.Dwgs_User
def rect(x0,y0,x1,y1):
    for ax,ay,bx,by in [(x0,y0,x1,y0),(x1,y0,x1,y1),(x1,y1,x0,y1),(x0,y1,x0,y0)]:
        s=pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(V(ax,ay)); s.SetEnd(V(bx,by)); s.SetLayer(LY); s.SetWidth(mm(0.25)); s.SetLocked(True); b.Add(s)
c1=S(-23.31,-29.68); c2=S(27.49,-80.48); rect(min(c1[0],c2[0]),min(c1[1],c2[1]),max(c1[0],c2[0]),max(c1[1],c2[1]))   # A7S board
e1=S(15.5,-58.5); e2=S(31.5,-74.5); rect(min(e1[0],e2[0]),min(e1[1],e2[1]),max(e1[0],e2[0]),max(e1[1],e2[1]))       # ETH
tt=pcbnew.PCB_TEXT(b); tt.SetText("A7S+ETH ref (locked)"); tt.SetLayer(LY); tt.SetPosition(V((c1[0]+c2[0])/2,(c1[1]+c2[1])/2)); tt.SetTextSize(pcbnew.VECTOR2I(mm(1.5),mm(1.5))); tt.SetTextThickness(mm(0.25)); tt.SetLocked(True); b.Add(tt)

pcbnew.SaveBoard(OUT,b); out("saved "+OUT)
