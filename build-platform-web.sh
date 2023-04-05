#!/bin/sh

set -eux

(cd raylib/src && make clean)
(cd raylib/src && emcc -c rcore.c -Os -Wall -DPLATFORM_WEB -DGRAPHICS_API_OPENGL_ES2)
(cd raylib/src && emcc -c rshapes.c -Os -Wall -DPLATFORM_WEB -DGRAPHICS_API_OPENGL_ES2)
(cd raylib/src && emcc -c rtextures.c -Os -Wall -DPLATFORM_WEB -DGRAPHICS_API_OPENGL_ES2)
(cd raylib/src && emcc -c rtext.c -Os -Wall -DPLATFORM_WEB -DGRAPHICS_API_OPENGL_ES2)
(cd raylib/src && emcc -c rmodels.c -Os -Wall -DPLATFORM_WEB -DGRAPHICS_API_OPENGL_ES2)
(cd raylib/src && emcc -c utils.c -Os -Wall -DPLATFORM_WEB)
(cd raylib/src && emcc -c raudio.c -Os -Wall -DPLATFORM_WEB)
(cd raylib/src && emar rcs libraylib.a rcore.o rshapes.o rtextures.o rtext.o rmodels.o utils.o raudio.o)
