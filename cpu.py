import random

'''
TODO:   opcode 0xE000
        opcode 0xF00A
'''


class cpu:
    def __init__(self, renderer, keyboard):
        bytes_in_memory = 4096
        number_of_v_registers = 16

        self.renderer = renderer
        self.keyboard = keyboard

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
        try:
            fp = open(rom_file_name, 'rb')
            bytes_from_file = fp.read()
            fp.close()
        except:
            print("Unable to open and read rom file given. Please make sure path is correct.")
            exit(1)

        for i in range(len(bytes_from_file)):
            #dubious line ?
            self.memory[0x200 + i] = bytes_from_file[i]


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
            self.delay_timer -= 1
        
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def set_v_register(self, register, value):
        self.v_registers[register] = (value & 0xFF)

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
        self.renderer.render()
        #play sound if including sound

    def execute_opcode(self, opcode):
        print(hex(opcode))
        x = ((opcode & 0x0F00) >> 8)
        y = ((opcode & 0x00F0) >>4)
        opcode_msb = opcode & 0xF000

        if opcode_msb == 0x0000:
            if opcode == 0x00E0:
                self.renderer.clear()
            elif opcode == 0x00EE:
                self.program_counter = self.stack.pop()

        elif opcode_msb == 0x1000:
            self.program_counter = (opcode & 0x0FFF)

        elif opcode_msb == 0x2000:
            self.stack.append(self.program_counter)
            self.program_counter = (opcode & 0x0FFF)

        elif opcode_msb == 0x3000:
            if self.v_registers[x] == (opcode & 0x00FF):
                self.program_counter += 2

        elif opcode_msb == 0x4000:
            if self.v_registers[x] != (opcode & 0x00FF):
                self.program_counter += 2

        elif opcode_msb == 0x5000:
            if self.v_registers[x] == self.v_registers[y]:
                self.program_counter += 2

        elif opcode_msb == 0x6000:
            self.set_v_register(x, (opcode & 0x00FF))

        elif opcode_msb == 0x7000:
            self.set_v_register(x, (self.v_registers[x] + (opcode & 0x00FF)))

        elif opcode_msb == 0x8000:
            opcode_lsb = opcode & 0x000F

            if opcode_lsb == 0x0:
                self.set_v_register(x, self.v_registers[y])
            elif opcode_lsb == 0x1:
                self.set_v_register(x, (self.v_registers[x] | self.v_registers[y]))
            elif opcode_lsb == 0x2:
                self.set_v_register(x, (self.v_registers[x] & self.v_registers[y]))
            elif opcode_lsb == 0x3:
                self.set_v_register(x, (self.v_registers[x] ^ self.v_registers[y]))
            elif opcode_lsb == 0x4:
                sum = self.v_registers[x] + self.v_registers[y]

                self.set_v_register(0xF, 0)

                if sum > 0xFF:
                    self.set_v_register(0xF, 1)

                self.set_v_register(x, (sum & 0xFF))
            elif opcode_lsb == 0x5:
                self.set_v_register(0xF, 0)

                if self.v_registers[x] > self.v_registers[y]:
                    self.set_v_register(0xF, 1)

                self.set_v_register(x, ((self.v_registers[x] - self.v_registers[y]) & 0xFF))
            elif opcode_lsb == 0x6:
                self.set_v_register(0xF, (self.v_registers[x] & 0x1))
                
                self.v_registers[x] >>= 1
            elif opcode_lsb == 0x7:
                self.set_v_register(0xF, 0)

                if self.v_registers[y] > self.v_registers[x]:
                    self.set_v_register(0xF, 1)

                self.set_v_register(x, ((self.v_registers[y] - self.v_registers[x]) & 0xFF))
            elif opcode_lsb == 0xE:
                self.set_v_register(0xF, (self.v_registers[x] & 0x80))
                self.v_registers[x] <<= 1

        elif opcode_msb == 0x9000:
            if self.v_registers[x] != self.v_registers[y]:
                self.program_counter += 2

        elif opcode_msb == 0xA000:
            self.i_register = (opcode & 0x0FFF)

        elif opcode_msb == 0xB000:
            self.program_counter = ((opcode & 0x0FFF) + self.v_registers[0])

        elif opcode_msb == 0xC000:
            #might need to change the end of the range
            random_number = random.randint(1, 0xFF)
            self.set_v_register(x, (random_number & (opcode & 0xFF)))

        elif opcode_msb == 0xD000:
            width = 8
            height = (opcode & 0xF)

            self.set_v_register(0xF, 0)

            for row in range(height):
                sprite = self.memory[self.i_register + row]

                for col in range(width):
                    if (sprite & 0x80) > 0:
                        if self.renderer.toggle_pixels(self.v_registers[x] + col, self.v_registers[y] + row):
                            self.set_v_register(0xF, 1)

                    sprite <<= 1

        elif opcode_msb == 0xE000:
            opcode_least_significant_two_bits = opcode & 0x00FF

            if opcode_least_significant_two_bits == 0x009E:
                if self.keyboard.get_value_from_key(self.v_registers[x]) == 1:
                    self.program_counter += 2
            elif opcode_least_significant_two_bits == 0x00A1:
                if self.keyboard.get_value_from_key(self.v_registers[x]) == 0:
                    self.program_counter += 2

        elif opcode_msb == 0xF000:
            opcode_least_significant_two_bits = opcode & 0x00FF

            if opcode_least_significant_two_bits == 0x0007:
                self.set_v_register(x, self.delay_timer)
            elif opcode_least_significant_two_bits == 0x000A:
                #pause
                self.is_program_paused = True
                self.set_v_register(x, self.keyboard.wait_for_keypress())
                self.is_program_paused = False
            elif opcode_least_significant_two_bits == 0x0015:
                self.delay_timer = self.v_registers[x]
            elif opcode_least_significant_two_bits == 0x0018:
                self.sound_timer = self.v_registers[x]
            elif opcode_least_significant_two_bits == 0x001E:
                self.i_register += self.v_registers[x]
                self.i_register = (self.i_register & 0x0FFF)
            elif opcode_least_significant_two_bits == 0x0029:
                self.i_register = (self.v_registers[x] * 5)
            elif opcode_least_significant_two_bits == 0x0033:
                self.memory[self.i_register] = int(self.v_registers[x] / 100)
                self.memory[self.i_register + 1] = int((self.v_registers[x] % 100) / 10)
                self.memory[self.i_register + 2] = int(self.v_registers[x] % 10)
            elif opcode_least_significant_two_bits == 0x0055:
                for i in range(x + 1):
                    self.memory[self.i_register + i] = self.v_registers[i]
            elif opcode_least_significant_two_bits == 0x0065:
                for i in range(x + 1):
                    self.set_v_register(i, (self.memory[self.i_register + i]))

        else:
            print("Received unknown opcode %s from program. Exiting." % opcode)
            exit(1)
        
