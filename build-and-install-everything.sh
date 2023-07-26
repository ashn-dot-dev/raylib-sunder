#!/bin/sh
set -eux

make clean
rm -rf build

make raylib.sunder
(sh build-platform-desktop.sh)
(sh build-platform-web.sh)

make install
cp build/* "${SUNDER_HOME}/lib/raylib"
cp raylib-config "${SUNDER_HOME}/lib/raylib"
