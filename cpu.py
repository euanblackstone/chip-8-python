#!/usr/bin/env python3

class cpu:
    bytes_in_memory = 4096
    number_of_v_registers = 16

    def __init__(self):
        self.memory = bytearray(bytes_in_memory)
        self.v_registers = bytearray(number_of_v_registers)
        #initializes list to have a len of 16, can change this to a proper stack if needed
        self.stack = [0] * 16

        self.i_register = 0

        self.delay_timer = 0
        self.sound_timer = 0

        self.program_counter = 0x0200
        
        self.is_program_paused = False;
        self.speed_of_emulation = 10

    def load_rom_into_memory(self, rom_file_name):
        print("hi")

    def load_fontset_into_memory(self):
        fontset = bytearray([
            0xF0, 0x90, 0x90, 0x90, 0xF0, 
            0x20, 0x60, 0x20, 0x20, 0x70, 
            0xF0, 0x10, 0xF0, 0x80, 0xF0, 
            0xF0, 0x10, 0xF0, 0x10, 0xF0, 
            0x90, 0x90, 0xF0, 0x10, 0x10, 
            0xF0, 0x80, 0xF0, 0x10, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0, 
            0xF0, 0x10, 0x20, 0x40, 0x40,
            0xF0, 0x90, 0xF0, 0x90, 0xF0,
            0xF0, 0x90, 0xF0, 0x10, 0xF0,
            0xF0, 0x90, 0xF0, 0x90, 0x90,
            0xE0, 0x90, 0xE0, 0x90, 0xE0,
            0xF0, 0x80, 0x80, 0x80, 0xF0,
            0xE0, 0x90, 0x90, 0x90, 0xE0,
            0xF0, 0x80, 0xF0, 0x80, 0xF0,
            0xF0, 0x80, 0xF0, 0x80, 0x80
        ])

        for i in range(len(fontset)):
            self.memory[0x80 + i] = fontset[i]

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer = self.delay_timer - 1 
        
        if self.sound_timer > 0:
            self.sound_timer = self.sound_timer - 1

    def emulate_cycle(self):
        i = 0
        while i < self.speed_of_emulation:
            if not self.is_program_paused:
                opcode = (self.memory[self.program_counter] << 8 | self.memory[self.program_counter + 1])
                self.program_counter += 2
                self.execute_opcode(opcode)
            i = i + 1

        if not self.is_program_paused:
            self.update_timers()

        #render to the screen
        #play sound if including sound

    def execute_opcode(self, opcode):
        x = ((opcode & 0x0f00) >> 8)
        y = ((opcode & 0x00f0) >>4)

        match (opcode & 0xf000):
            case 0x0000:
                print("hi")
            case _:
                print("Received unknown opcode %s from program. Exiting." % opcode)
                exit(1)
        

cpu = cpu()