import pcbnew,sys
def out(s): sys.stdout.write(s+"\n"); sys.stdout.flush()
F="kicad/a7s_backplane_routed.kicad_pcb"
b=pcbnew.LoadBoard(F)
def mm(v): return pcbnew.FromMM(v)
def V(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))
# existing edges
have=set()
for d in b.GetDrawings():
    if d.GetLayer()==pcbnew.Edge_Cuts and d.GetShape()==pcbnew.SHAPE_T_SEGMENT:
        a=d.GetStart(); e=d.GetEnd()
        have.add((round(pcbnew.ToMM(a.x),1),round(pcbnew.ToMM(a.y),1),round(pcbnew.ToMM(e.x),1),round(pcbnew.ToMM(e.y),1)))
out("existing edges: "+str(sorted(have)))
# full rectangle corners (from render/place/v2)
need=[(87.6,94.1,1.4,94.1),   # south
      (1.4,94.1,1.4,20.0)]    # west
added=0
for x0,y0,x1,y1 in need:
    s=pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(V(x0,y0)); s.SetEnd(V(x1,y1))
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.15)); b.Add(s); added+=1
out(f"added {added} edges (south + west)")
pcbnew.SaveBoard(F,b)
# verify closed
segs=[d for d in b.GetDrawings() if d.GetLayer()==pcbnew.Edge_Cuts and d.GetShape()==pcbnew.SHAPE_T_SEGMENT]
out("total Edge.Cuts now: "+str(len(segs)))
