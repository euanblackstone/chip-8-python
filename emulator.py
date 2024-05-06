#!/usr/bin/env python3
import pygame
import time
from cpu import cpu
from screen import screen
from keyboard import keyboard

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

        #create screen, keyboard, and cpu
        

        
        self.screen = screen(SCREEN_SCALE)
        self.keypad = keyboard()
        # screen = pygame.display.set_mode((900, 500))
        self.cpu = cpu(self.screen, self.keypad)
        

        self.cpu.load_fontset_into_memory()
        self.cpu.load_rom_into_memory(rom_file_name)
        

    def start_emulator_loop(self):
        then = time.time_ns()

        run = True
        while run:
            pygame.display.update()

            now = time.time_ns()
            self.delta += (now - then) / self.ns
            then = now

            if self.delta >= 1:
                self.cpu.emulate_cycle()
                self.delta -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.keypad.key_map:
                        self.keypad.key_pressed(event.key)
                elif event.type == pygame.KEYUP:
                    if event.key in self.keypad.key_map:
                        self.keypad.key_released(event.key)
        pygame.quit()
