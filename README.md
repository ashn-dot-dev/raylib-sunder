# raylib-sunder

[Sunder](https://github.com/ashn-dot-dev/sunder) bindings for [raylib](https://github.com/raysan5/raylib) v4.5.0.

## Dependencies
### Debian/Ubuntu

[Wiki entry](https://github.com/raysan5/raylib/wiki/Working-on-GNU-Linux#ubuntu).

```sh
$ sudo apt install libasound2-dev mesa-common-dev libx11-dev libxrandr-dev libxi-dev xorg-dev libgl1-mesa-dev libglu1-mesa-dev
```

### Arch/Manjaro
[Wiki entry](https://github.com/raysan5/raylib/wiki/Working-on-GNU-Linux#arch-linux).

```sh
$ sudo pacman -S alsa-lib mesa libx11 libxrandr libxi libxcursor libxinerama
```

## Generating Bindings
Clone the raylib sources ([wiki entry](https://github.com/raysan5/raylib/wiki/Working-on-GNU-Linux#build-raylib-using-make)):

```sh
$ git clone https://github.com/raysan5/raylib.git raylib
```

and run the Sunder code generation script over the raylib API JSON:

```sh
$ (cd raylib/parser && make clean raylib_api.json FORMAT=JSON EXTENSION=json)
$ python3 generate.py raylib/parser/raylib_api.json > raylib.sunder
```

## Building the Example Program
For some C program (in this case `examples/example.c`) built with the commands:

```sh
$ (cd raylib/src && make PLATFORM=PLATFORM_DESKTOP)
$ clang -Iraylib/src -Lraylib/src -o example examples/example.c -lraylib -lGL -lm -lpthread -ldl -lrt -lX11
```

the equivalent Sunder program (in this case `examples/example.sunder`) would be built with:

```sh
$ (cd raylib/src/ && make PLATFORM=PLATFORM_DESKTOP)
$ SUNDER_BACKEND=C sunder-compile -o example -Lraylib/src -lraylib -lGL -lm -lpthread -ldl -lrt -lX11 examples/example.sunder
```

## Additional Notes
When developing on the Pinebook Pro (or similar platforms) raylib may fail
initialize the OpenGL context due to a `GLXBadFBConfig` error. If this occurs,
set `LIBGL_ALWAYS_SOFTWARE=true` to force software rendering.

```sh
LIBGL_ALWAYS_SOFTWARE=true ./raylib-application
```

## License
All content in this repository is licensed under the Zero-Clause BSD license.

See LICENSE for more information.
