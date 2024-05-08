# chip-8-python
A Chip-8 interpreter written in python.

## Goal
This goal of this project was to learn more about low-level programming and emulator development. The interpreter employs the common fetch, decode, and execute cycle. It uses Pygame to render graphics to the screen and accept user input.

## Usage
If you would like to try this interpreter yourself, first make sure you have Pygame installed.

```console
$ pip install pygame
```

Next, clone the repo into a directory of your choice.

```console
$ git clone https://github.com/euanblackstone/chip-8-python.git
```

Next, run the make file and run the executable, supplying the directory to the ROM you wish to use

```console
$ make
$ ./chip8 ./roms/IBM
```

## Known Issues
* Flickering
  * With some roms, notably Pong, the screen will flicker. This is natural with the original Chip-8 specifications. To fix this, one could use a double buffering technique to make rendering appear seamless.

