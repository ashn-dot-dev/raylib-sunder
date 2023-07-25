.POSIX:
.SUFFIXES:
.PHONY: \
	all \
	install \
	uninstall \
	clean

RAYLIB_VERSION=4.5.0

all: raylib.sunder

raylib.sunder: raylib/parser/raylib_api.json generate.py
	python3 generate.py raylib/parser/raylib_api.json > raylib.sunder

raylib/parser/raylib_api.json:
	[ -d raylib ] || git clone --single-branch --branch $(RAYLIB_VERSION) https://github.com/raysan5/raylib.git
	(cd raylib && git pull && git checkout $(RAYLIB_VERSION))
	(cd raylib/parser && make clean raylib_api.json FORMAT=JSON EXTENSION=json)

install: raylib.sunder
	mkdir -p "$(SUNDER_HOME)/lib/raylib"
	cp raylib.sunder "$(SUNDER_HOME)/lib/raylib"

uninstall:
	rm -rf "$(SUNDER_HOME)/lib/raylib"

clean:
	(cd raylib/src && make clean)
	(cd raylib/parser && make clean)
