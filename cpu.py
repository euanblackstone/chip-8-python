import random

'''
TODO:   opcode 0x00e0
        opcode 0xD000
        opcode 0xE000
        opcode 0xF00A
'''


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
        x = ((opcode & 0x0F00) >> 8)
        y = ((opcode & 0x00F0) >>4)

        match (opcode & 0xF000):
            case 0x0000:
                match (opcode):
                    case 0x00E0:
                        #clear the renderer
                        print("hi")
                    case 0x00EE:
                        self.program_counter = self.stack.pop()
            
            case 0x1000:
                self.program_counter = (opcode & 0x0FFF)

            case 0x2000:
                self.stack.append(self.program_counter)
                self.program_counter = (opcode & 0x0FFF)

            case 0x3000:
                if self.v_registers[x] == (opcode & 0x00FF):
                    self.program_counter += 2

            case 0x4000:
                if self.v_registers[x] != (opcode & 0x00FF):
                    self.program_counter += 2

            case 0x5000:
                if self.v_registers[x] == self.v_registers[y]:
                    self.program_counter += 2

            case 0x6000:
                self.v_registers[x] = (opcode & 0x00FF)

            case 0x7000:
                self.v_registers[x] = (self.v_registers[x] + (opcode & 0x00FF))

            case 0x8000:
                match (opcode & 0x000F):
                    case 0x0:
                        self.v_registers[x] = self.v_registers[y]
                    case 0x1:
                        self.v_registers[x] = (self.v_registers[x] | self.v_registers[y])
                    case 0x2:
                        self.v_registers[x] = (self.v_registers[x] & self.v_registers[y])
                    case 0x3:
                        self.v_registers[x] = (self.v_registers[x] ^ self.v_registers[y])
                    case 0x4:
                        sum = self.v_registers[x] + self.v_registers[y]

                        self.v_registers[0xF] = 0

                        if sum > 0xFF:
                            self.v_registers[0xF] = 1

                        self.v_registers[x] = (sum & 0xFF)
                    case 0x5:
                        self.v_registers[0xF] = 0

                        if self.v_registers[x] > self.v_registers[y]:
                            self.v_registers[0xF] = 1

                        self.v_registers[x] = ((self.v_registers[x] - self.v_registers[y]) & 0xFF)
                    case 0x6:
                        self.v_registers[0xF] = (self.v_registers[x] & 0x1)
                        
                        self.v_registers[x] >>= 1
                    case 0x7:
                        self.v_registers[0xF] = 0

                        if self.v_registers[y] > self.v_registers[x]:
                            self.v_registers[0xF] = 1

                        self.v_registers[x] = ((self.v_registers[y] - self.v_registers[x]) & 0xFF)
                    case 0xE:
                        self.v_registers[0xF] = (self.v_registers[x] & 0x80)
                        self.v_registers[x] <<= 1

            case 0x9000:
                if self.v_registers[x] != self.v_registers[y]:
                    self.program_counter += 2

            case 0xA000:
                self.i_register = (opcode & 0x0FFF)

            case 0xB000:
                self.program_counter = ((opcode & 0x0FFF) + self.v_registers[0])

            case 0xC000:
                #might need to change the end of the range
                random_number = random.randint(1, 0xFF)
                self.v_registers[x] = (random_number & (opcode & 0xFF))

            case 0xD000:
                #display stuff
                print("hi")

            case 0xE000:
                match (opcode & 0x00FF):
                    case 0x009E:
                        #keyboard
                        print("hi")
                    case 0x00A1:
                        #keyboard
                        print("hi")

            case 0xF000:
                match (opcode & 0x00FF):
                    case 0x0007:
                        self.v_registers[x] = self.delay_timer
                    case 0x000A:
                        #pause
                        self.is_program_paused = True
                    case 0x0015:
                        self.delay_timer = self.v_registers[x]
                    case 0x0018:
                        self.sound_timer = self.v_registers[x]
                    case 0x001E:
                        self.i_register += self.v_registers[x]
                        self.i_register = (self.i_register & 0x0FFF)
                    case 0x0029:
                        self.i_register = (self.v_registers[x] * 5)
                    case 0x0033:
                        self.memory[self.i_register] = (self.v_registers[x] / 100)
                        self.memory[self.i_register + 1] = ((self.v_registers[x] % 100) / 10)
                        self.memory[self.i_register + 2] = (self.v_registers[x] % 10)
                    case 0x0055:
                        for i in range(x + 1):
                            self.memory[self.i_register + i] = self.v_registers[i]
                    case 0x0065:
                        for i in range(x + 1):
                            self.v_registers[i] = self.memory[self.i_register + i]


                    
            case _:
                print("Received unknown opcode %s from program. Exiting." % opcode)
                exit(1)
        

cpu = cpu()