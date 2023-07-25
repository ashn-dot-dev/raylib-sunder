#!/bin/sh
set -eux

(cd raylib/src && make clean)
(cd raylib/src && make clean all PLATFORM=PLATFORM_DESKTOP)
(mkdir -p build && cp raylib/src/libraylib.a build)
