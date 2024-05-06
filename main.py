#!/usr/bin/env python3

from emulator import emulator
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage incorrect.")
        sys.exit(0)
    
    try:
        chip8 = emulator(60, sys.argv[1])
        chip8.start_emulator_loop()
    except FileNotFoundError:
        print("Rom unknown. Please use a rom from rom folder.")
        sys.exit(0)

    

if __name__ == "__main__":
    main()