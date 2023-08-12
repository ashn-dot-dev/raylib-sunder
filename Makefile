.POSIX:
.SUFFIXES:
.PHONY: \
	all \
	install \
	uninstall \
	clean

RAYLIB_REPOURL=https://github.com/raysan5/raylib.git
RAYLIB_VERSION=master

all: raylib.sunder libraylib.a libraylib-web.a

raylib:
	git clone --single-branch --branch "$(RAYLIB_VERSION)" "$(RAYLIB_REPOURL)"

raylib/parser/raylib_api.json: raylib
	(cd raylib/parser && make clean raylib_api.json FORMAT=JSON EXTENSION=json)

raylib.sunder: raylib/parser/raylib_api.json generate.py
	python3 generate.py raylib/parser/raylib_api.json > raylib.sunder

libraylib.a: raylib
	(cd raylib/src && make clean all PLATFORM=PLATFORM_DESKTOP)
	cp raylib/src/libraylib.a libraylib.a

libraylib-web.a: raylib
	(cd raylib/src && make clean all PLATFORM=PLATFORM_WEB)
	cp raylib/src/libraylib.a libraylib-web.a

install: raylib.sunder libraylib.a libraylib-web.a
	mkdir -p "$(SUNDER_HOME)/lib/raylib"
	cp raylib.sunder "$(SUNDER_HOME)/lib/raylib"
	cp libraylib.a "$(SUNDER_HOME)/lib/raylib"
	cp libraylib-web.a "$(SUNDER_HOME)/lib/raylib"
	cp raylib-config "$(SUNDER_HOME)/lib/raylib"
	cp emscripten-shell.html "${SUNDER_HOME}/lib/raylib"

uninstall:
	rm -rf "$(SUNDER_HOME)/lib/raylib"

clean:
	rm -f raylib.sunder libraylib.a libraylib-web.a
	(cd raylib/src && make clean)
	(cd raylib/parser && make clean)
