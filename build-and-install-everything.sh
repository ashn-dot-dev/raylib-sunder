#!/bin/sh
set -eux

make raylib.sunder
[ -e build/libraylib.a ] || (sh build-platform-desktop.sh)
[ -e build/libraylib-web.a ] || (sh build-platform-web.sh)

make install
cp build/* "${SUNDER_HOME}/lib/raylib"
cp raylib-config "${SUNDER_HOME}/lib/raylib"
cp emscripten-shell.html "${SUNDER_HOME}/lib/raylib"
