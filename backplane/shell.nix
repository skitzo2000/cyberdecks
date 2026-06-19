# Dev shell for the A7S backplane: schematic netlist + KiCad + STEP measurement.
#   nix-shell            # from backplane/
# then:
#   python3 a7s_backplane_skidl.py        # -> a7s_backplane.net   (needs KiCad symbol libs; see hook)
#   freecad                                # GUI: open ../3dfiles/.../*.stp and measure headers
#   freecadcmd measure_headers.py          # headless geometry extraction (when we write it)
#   kicad                                  # new project -> import a7s_backplane.net -> place/route
{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  packages = [
    pkgs.kicad                                   # KiCad 8 + symbol/footprint/3D libraries
    pkgs.freecad                                 # STEP viewer/measure (also: freecadcmd)
    (pkgs.python3.withPackages (ps: with ps; [
      skidl                                      # netlist generation
    ]))
  ];

  # SKiDL finds KiCad symbol libs via these env vars. KiCad's own wrapper sets them, but the shell
  # may not export them for python — point them at the nix KiCad symbol/footprint dirs.
  shellHook = ''
    export KICAD8_SYMBOL_DIR="${pkgs.kicad.libraries.symbols or ""}/share/kicad/symbols"
    export KICAD8_FOOTPRINT_DIR="${pkgs.kicad.libraries.footprints or ""}/share/kicad/footprints"
    if [ ! -e "$KICAD8_SYMBOL_DIR/Device.kicad_sym" ]; then
      # fallback: locate the symbols dir in the nix store
      d=$(find /nix/store -maxdepth 4 -name 'Device.kicad_sym' -path '*symbols*' 2>/dev/null | head -1)
      [ -n "$d" ] && export KICAD8_SYMBOL_DIR="$(dirname "$d")"
    fi
    echo "KICAD8_SYMBOL_DIR=$KICAD8_SYMBOL_DIR"
    echo "[a7s-backplane] kicad $(kicad-cli version 2>/dev/null || echo '?'), freecad, skidl ready"
  '';
}
