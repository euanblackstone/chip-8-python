import cpu

'''
TODO:   write out create_gui (might not actually need this) and start_emu_loop methods
        actually create the screen and keypad classes and add them to constructor
'''

class emulator:
    screen_scale = 20

    def __init__(self, frequency_of_cpu, rom_file_name):
        self.frequency_of_cpu = frequency_of_cpu
        self.ns = 1000000000.0 / self.frequency_of_cpu

        #create screen, ketboard, and cpu
        self.cpu = cpu()
        self.screen = None
        self.keypad = None

        self.create_gui()

        self.cpu.load_fontset_into_memory()
        self.cpu.load_rom_into_memory(rom_file_name)

    def create_gui(self):
        print("Hi")

    def start_emulator_loop(self):
        print("hi")