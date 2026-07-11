import pcbnew,sys
def out(s): sys.stdout.write(s+"\n"); sys.stdout.flush()
SRC_NETS="kicad/a7s_backplane_render.kicad_pcb"   # authoritative connectivity
PLACE   ="kicad/a7s_backplane_place.kicad_pcb"     # user's placement (zero net)
OUT     ="kicad/a7s_backplane_v2.kicad_pcb"        # placement + nets, ready to route
r=pcbnew.LoadBoard(SRC_NETS); p=pcbnew.LoadBoard(PLACE)
# map (ref,pad)->netname from render
netmap={}
for fp in r.GetFootprints():
    for pad in fp.Pads():
        nm=pad.GetNetname()
        if nm: netmap[(fp.GetReference(),pad.GetNumber())]=nm
out(f"connectivity map: {len(netmap)} netted pads, {len(set(netmap.values()))} nets")
# create nets in place board
pn={}
for nm in sorted(set(netmap.values())):
    ni=pcbnew.NETINFO_ITEM(p,nm); p.Add(ni); pn[nm]=ni
# assign
asg=miss=0
for fp in p.GetFootprints():
    for pad in fp.Pads():
        k=(fp.GetReference(),pad.GetNumber())
        if k in netmap: pad.SetNet(pn[netmap[k]]); asg+=1
        else: miss+=1
out(f"assigned {asg} pads; {miss} left unconnected (NC pads)")
p.BuildListOfNets()
pcbnew.SaveBoard(OUT,p)
out("saved "+OUT+"  | net count: "+str(p.GetNetCount()))
