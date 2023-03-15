# raylib-sunder

[Sunder](https://github.com/ashn-dot-dev/sunder) bindings for [raylib](https://github.com/raysan5/raylib) v4.5.0.

## Dependencies
### Debian/Ubuntu

[Wiki entry](https://github.com/raysan5/raylib/wiki/Working-on-GNU-Linux#ubuntu).

```sh
$ sudo apt install libasound2-dev mesa-common-dev libx11-dev libxrandr-dev libxi-dev xorg-dev libgl1-mesa-dev libglu1-mesa-dev
```

## Generating Bindings
Clone the raylib sources ([wiki entry](https://github.com/raysan5/raylib/wiki/Working-on-GNU-Linux#build-raylib-using-make)):

```sh
$ git clone https://github.com/raysan5/raylib.git raylib
```

and run the Sunder code generation script over the raylib API JSON:

```sh
$ python3 generate.py raylib/parser/output/raylib_api.json > raylib.sunder
```

## Building the Example Program
For some C program (in this case `example.c`) built with the commands:

```sh
$ (cd raylib/src/ && make PLATFORM=PLATFORM_DESKTOP)
$ clang -Iraylib/src -Lraylib/src -o example example.c -lraylib -lGL -lm -lpthread -ldl -lrt -lX11
```

the equivalent Sunder program (in this case `example.sunder`) would be built with:

```sh
$ (cd raylib/src/ && make PLATFORM=PLATFORM_DESKTOP)
$ sunder-compile -o example -Lraylib/src -lraylib -lGL -lm -lpthread -ldl -lrt -lX11 example.sunder
```
