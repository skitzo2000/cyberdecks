import pcbnew
F="kicad/a7s_backplane_hdrfix.kicad_pcb"
b=pcbnew.LoadBoard(F)
def mm(v): return pcbnew.FromMM(v)
def V(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))

# --- derive STEP->KiCad affine from the 4 mounting holes (corrected orientation) ---
H={h.GetReference():(pcbnew.ToMM(h.GetPosition().x),pcbnew.ToMM(h.GetPosition().y)) for h in b.GetFootprints() if h.GetReference().startswith("H")}
# STEP holes  ->  KiCad holes  (STEP west maps to KiCad east after the horizontal flip)
# STEP TL(-19.81,-33.18)->H3 ; TR(23.99,-33.18)->H4 ; BL(-19.81,-76.98)->H1 ; BR(23.99,-76.98)->H2
a=(H["H4"][0]-H["H3"][0])/(23.99-(-19.81)); bX=H["H3"][0]-a*(-19.81)
c=(H["H1"][1]-H["H3"][1])/(-76.98-(-33.18)); dY=H["H3"][1]-c*(-33.18)
def S(sx,sy): return (a*sx+bX, c*sy+dY)      # STEP mm -> KiCad mm
print(f"transform: kx={a:.3f}*sx+{bX:.3f}  ky={c:.3f}*sy+{dY:.3f}")

LY=pcbnew.Dwgs_User
def rect(x0,y0,x1,y1,w=0.2):
    for (ax,ay,bx,by) in [(x0,y0,x1,y0),(x1,y0,x1,y1),(x1,y1,x0,y1),(x0,y1,x0,y0)]:
        s=pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(V(ax,ay)); s.SetEnd(V(bx,by)); s.SetLayer(LY); s.SetWidth(mm(w)); b.Add(s)
def txt(x,y,t,sz=1.2):
    o=pcbnew.PCB_TEXT(b); o.SetText(t); o.SetLayer(LY); o.SetPosition(V(x,y)); o.SetTextSize(pcbnew.VECTOR2I(mm(sz),mm(sz))); o.SetTextThickness(mm(0.2)); b.Add(o)

# A7S PCB outline (STEP X[-23.31,27.49] Y[-29.68,-80.48])
c1=S(-23.31,-29.68); c2=S(27.49,-80.48)
rect(min(c1[0],c2[0]),min(c1[1],c2[1]),max(c1[0],c2[0]),max(c1[1],c2[1]),0.25)
txt((c1[0]+c2[0])/2, (c1[1]+c2[1])/2, "A7S BOARD")

# Ethernet RJ45 body (approx 16x16, protrudes to STEP x=+31.5)
e1=S(15.5,-58.5); e2=S(31.5,-74.5)
rect(min(e1[0],e2[0]),min(e1[1],e2[1]),max(e1[0],e2[0]),max(e1[1],e2[1]),0.25)
eth_edge=min(e1[0],e2[0])
txt(eth_edge+1, (e1[1]+e2[1])/2, "ETH")

# USB-C/A ports (east edge in STEP -> west in KiCad); draw small boxes protruding to x=+31.5
for cx,cy,nm in [(24.51,-39.61,"USBC1"),(24.51,-46.11,"USBC2"),(24.69,-53.83,"USBA")]:
    p1=S(cx-3,cy-4.5); p2=S(31.5,cy+4.5)
    rect(min(p1[0],p2[0]),min(p1[1],p2[1]),max(p1[0],p2[0]),max(p1[1],p2[1]),0.2)

# PCB (shield) west edge
bb=b.GetBoardEdgesBoundingBox(); pcb_w=pcbnew.ToMM(bb.GetLeft())
print(f"\nPCB west edge X = {pcb_w:.2f}")
print(f"ETH port west edge X = {eth_edge:.2f}")
print(f"GAP (PCB extends west of ETH by) = {eth_edge-pcb_w:.2f} mm")
print(f"-> to line them up, shift A7S (holes+headers) WEST by {eth_edge-pcb_w:.2f} mm")
# also report westmost A7S feature vs encoder
j10=b.FindFootprintByReference("J10")
print(f"encoder J10 origin X = {pcbnew.ToMM(j10.GetPosition().x):.2f} (watch for collision when A7S moves west)")
pcbnew.SaveBoard(F,b); print("saved overlay to",F)
