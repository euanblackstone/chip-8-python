import pygame

KEY_DOWN = 1
KEY_UP = 0

class keyboard:
    def __init__(self):
        self.key_map = {
            pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 12,
            pygame.K_q: 4, pygame.K_w: 5, pygame.K_e: 6, pygame.K_r: 13,
            pygame.K_a: 7, pygame.K_s: 8, pygame.K_d: 9, pygame.K_f: 14,
            pygame.K_z: 10, pygame.K_x: 0, pygame.K_c: 11, pygame.K_v: 15
        }
        self.keys = [0] * 16

    def key_pressed(self, key):
        self.keys[self.key_map[key]] = KEY_DOWN

    def key_released(self, key):
        self.keys[self.key_map[key]] = KEY_UP

    def get_value_from_key(self, value):
        return self.keys[value]
    
    def wait_for_keypress(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.KEYDOWN:
                    return self.key_map[event.key]


