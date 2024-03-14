#!/usr/bin/env python3
import pygame
import time
from cpu import cpu
from screen import screen

'''
TODO:   write out create_gui (might not actually need this) and start_emu_loop methods
        actually create the screen and keypad classes and add them to constructor
'''

SCREEN_SCALE = 20

class emulator:
    def __init__(self, frequency_of_cpu, rom_file_name):
        pygame.init()

        self.frequency_of_cpu = frequency_of_cpu
        self.ns = 1000000000.0 / self.frequency_of_cpu
        # Might want to refactor this line
        self.delta = 0

        #create screen, ketboard, and cpu
        

        
        self.screen = screen(SCREEN_SCALE)
        # screen = pygame.display.set_mode((900, 500))
        self.cpu = cpu(self.screen)
        
        self.keypad = None

        self.cpu.load_fontset_into_memory()
        self.cpu.load_rom_into_memory(rom_file_name)
        

    def start_emulator_loop(self):
        then = time.time_ns()

        run = True
        while run:
            pygame.display.flip()

            now = time.time_ns()
            self.delta += (now - then) / self.ns
            then = now

            if self.delta >= 1:
                self.cpu.emulate_cycle()
                self.delta -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()

def main():
    e = emulator(60, "./roms/IBM")
    e.start_emulator_loop()

if __name__ == "__main__":
    main()