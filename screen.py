from pygame import display, Color, draw


SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32

# COLOR_BLACK = Color(0, 0, 0, 255)
# COLOR_WHITE = Color(255, 255, 255, 255)

class screen:
    def __init__(self, scale_factor):
        # self.screen_pixels = [[False for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]
        self.current_frame = [[False for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]
        self.previous_frame = [[False for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]

        self.scale = scale_factor
        self.scaled_screen_width = SCREEN_WIDTH * self.scale
        self.scaled_screen_height = SCREEN_HEIGHT * self.scale

        #display.init()
        self.screen = display.set_mode((self.scaled_screen_width, self.scaled_screen_height))
        display.set_caption("Chip-8")
        self.clear()
        # display.flip()
        



    def get_screen_width(self):
        return self.scaled_screen_width
    
    def get_screen_hegiht(self):
        return self.scaled_screen_height
    
    def clear(self):
        # self.screen_pixels = [[False for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]
        self.current_frame = [[False for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]
        self.previous_frame = [[False for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]
        self.screen.fill((0, 0, 0))

    def update(self):
        display.flip()

    def toggle_pixels(self, x, y):
        # x = x & 0xFF
        # y = y & 0xFF

        if x >= SCREEN_WIDTH:
            x = x % SCREEN_WIDTH

        if y >= SCREEN_HEIGHT:
            y = y % SCREEN_HEIGHT

        self.current_frame[y][x] ^= True

        return not self.current_frame[y][x]

    def render(self):
        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                if self.current_frame[y][x] != self.previous_frame[y][x]:
                    color = (255, 255, 255) if self.current_frame[y][x] == 1 else (0, 0, 0)
                    draw.rect(self.screen, color, (x * self.scale, y * self.scale, self.scale, self.scale))
        
        self.previous_frame = [row[:] for row in self.current_frame]
