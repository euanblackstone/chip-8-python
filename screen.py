'''
TODO:   find a way to render pixels to a screen. I think pygame would be the best way to do this
'''


class screen:
    screen_width = 64
    screen_height = 32

    def __init__(self):
        self.screen_pixels = [[False for x in range(screen_width)] for y in range(screen_height)]

    def get_screen_width(self):
        return screen_width
    
    def get_screen_height(self):
        return screen_height