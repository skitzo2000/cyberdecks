#!/usr/bin/env python3
# Generate backplane/a7s_backplane.kicad_sch FROM the netlist (derived artifact; source of
# truth is a7s_backplane_skidl.py). Run from backplane/ with kiutils installed and KICAD_SYM set:
#   python3 -m venv venv && venv/bin/pip install kiutils
#   KICAD_SYM=$(../backplane/tools/kpython -c "import os;print(os.environ['KICAD_SYM'])") \
#     venv/bin/python tools/gen_kicad_schematic.py
"""Generate a readable, openable KiCad schematic (.kicad_sch) from the SKiDL netlist.
Every component = its real symbol; a global net-label on every connected pin."""
import re, os, uuid
from kiutils.schematic import Schematic
from kiutils.symbol import SymbolLib, Symbol, SymbolPin
from kiutils.items.schitems import SchematicSymbol, GlobalLabel, SymbolProjectInstance, SymbolProjectPath, Connection, Stroke
from kiutils.items.common import Position, Property, Effects, Font
from kiutils.items.syitems import SyRect, Stroke, Fill

SYM_DIR=os.environ["KICAD_SYM"]; NET="a7s_backplane.net"; OUT="a7s_backplane.kicad_sch"
def U(): return str(uuid.uuid4())

# ---- S-expr parser ----
def parse(s):
    toks=re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', s); it=iter(toks)
    def rd(t):
        if t=='(':
            l=[]
            while True:
                t=next(it)
                if t==')': return l
                l.append(rd(t))
        return t[1:-1] if t.startswith('"') else t
    return rd(next(it))
tree=parse(open(NET).read())
def find(n,k): return [x for x in n if isinstance(x,list) and x and x[0]==k]
def val(n,k):
    f=find(n,k); return f[0][1] if f and len(f[0])>1 else None
comps={}
for c in find(find(tree,'components')[0],'comp'):
    ls=find(c,'libsource')
    comps[val(c,'ref')]=(val(c,'value'), val(ls[0],'lib') if ls else None, val(ls[0],'part') if ls else None)
pin_net={}
for net in find(find(tree,'nets')[0],'net'):
    nm=val(net,'name')
    for nd in find(net,'node'): pin_net[(val(nd,'ref'),val(nd,'pin'))]=nm
print(f"parsed {len(comps)} comps, {len(pin_net)} pin-net links")

libcache={}
def load_sym(lib,part):
    if (lib,part) in libcache: return libcache[(lib,part)]
    sl=SymbolLib.from_file(os.path.join(SYM_DIR,lib+".kicad_sym"))
    for s in sl.symbols:
        if s.entryName==part:
            s.libraryNickname=lib          # top-level id = Lib:Part; units keep Part_x_x
            libcache[(lib,part)]=s; return s
    raise SystemExit(f"{lib}:{part} not found")
def sym_pins(sym): return [p for u in sym.units for p in u.pins]

def build_rp2040():
    a1=[p for (r,p) in pin_net if r=="A1"]
    order=["5V","GND","3V3"]+[f"GP{i}" for i in range(30)]
    a1=[p for p in order if p in a1]+[p for p in a1 if p not in order]
    n=len(a1); half=(n+1)//2; W=25.4; top=(half-1)*2.54/2
    sym=Symbol.create_new(id="RP2040_Zero", reference="A", value="RP2040_Zero")
    sym.libraryNickname="a7s"; sym.entryName="RP2040_Zero"
    u=Symbol(); u.entryName="RP2040_Zero"; u.unitId=1; u.styleId=1
    u.graphicItems.append(SyRect(start=Position(-W/2, top+2.54), end=Position(W/2, top-(n-half)*2.54-2.54),
                                 stroke=Stroke(width=0.254), fill=Fill(type="background")))
    for i,pn in enumerate(a1):
        if i<half: y=top-i*2.54; x=-W/2-2.54; ang=0
        else:      y=top-(i-half)*2.54; x=W/2+2.54; ang=180
        u.pins.append(SymbolPin(electricalType='passive', graphicalStyle='line',
                      position=Position(x,y,ang), length=2.54, name=pn, number=pn))
    sym.units.append(u); return sym

sch=Schematic.create_new(); sch.uuid=U(); sch.paper.paperSize="A2"
used={}
for ref,(v,lib,part) in comps.items():
    if lib=="NO_LIB": continue
    if f"{lib}:{part}" not in used: used[f"{lib}:{part}"]=load_sym(lib,part)
rp=build_rp2040(); used["a7s:RP2040_Zero"]=rp
sch.libSymbols=list(used.values())

def props(ref,v,x,y):
    return [Property(key="Reference",value=ref,position=Position(x-2.54,y-5.0,0),effects=Effects(font=Font(height=1.27,width=1.27))),
            Property(key="Value",value=v,position=Position(x-2.54,y-2.5,0),effects=Effects(font=Font(height=1.0,width=1.0)))]
STUB=5.08
def add_labels(ref,sym,sx,sy):
    for p in sym_pins(sym):
        net=pin_net.get((ref,p.number))
        if not net: continue
        lx=sx+p.position.X; ly=sy-p.position.Y
        dx=lx-sx; dy=ly-sy
        if abs(dx)>=abs(dy): ox=(1 if dx>0 else -1); oy=0; lang=0 if ox>0 else 180
        else:                ox=0; oy=(1 if dy>0 else -1); lang=270 if oy>0 else 90
        ex=round(lx+ox*STUB,2); ey=round(ly+oy*STUB,2); lx=round(lx,2); ly=round(ly,2)
        # wire stub pin -> label
        sch.graphicalItems.append(Connection(type="wire",
            points=[Position(lx,ly),Position(ex,ey)], stroke=Stroke(width=0), uuid=U()))
        sch.globalLabels.append(GlobalLabel(text=net, shape="input",
            position=Position(ex,ey,lang), effects=Effects(font=Font(height=1.0,width=1.0)), uuid=U()))

GROUPS=[("A7S",["J1","J2"]),("RP2040",["A1"]),("Display",["J3"]),
        ("Radios",["J5","J6","J5b","J6b"]),("Flipper",["J12"]),
        ("Inputs",["J8","J10","J11","SW1","SW2","SW3","SW4"]),
        ("Power",["F1","F2","C1","C2"]),("Console",["TP1","TP2"])]
colx=38.1; colw=76.2
for title,refs in GROUPS:
    yy=50.8
    for ref in refs:
        if ref not in comps: continue
        v,lib,part=comps[ref]; sym= rp if lib=="NO_LIB" else used[f"{lib}:{part}"]
        npins=len(sym_pins(sym)); sx=colx+30.48; sy=yy+npins*2.54/2+20.32
        ln = lib if lib!="NO_LIB" else "a7s"; en = part
        ss=SchematicSymbol(libraryNickname=ln, entryName=en, position=Position(sx,sy,0),
             unit=1, inBom=True, onBoard=True, uuid=U(), properties=props(ref,v,sx,sy))
        ss.instances=[SymbolProjectInstance(name="a7s_backplane",
             paths=[SymbolProjectPath(sheetInstancePath="/"+sch.uuid, reference=ref, unit=1)])]
        sch.schematicSymbols.append(ss); add_labels(ref,sym,sx,sy)
        yy=sy+npins*2.54/2+30.48
    colx+=colw
sch.to_file(OUT)
print("wrote",OUT,"| symbols:",len(sch.schematicSymbols),"| net labels:",len(sch.globalLabels))
