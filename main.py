#!/usr/bin/env python3

import pygame

def main():
    screen = pygame.display.set_mode((900, 500))
    run = True
    while run:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
    

if __name__ == "__main__":
    main()