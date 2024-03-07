import sys
try:
    import pygame
except:
    print("===========================")
    if sys.platform in ('emscripten','wasi'):
        print('clearing')
        embed.PyErr_Clear()
        print('done')

import pygame

pygame.init()

# set up the window
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("blank")

# main game loop
while True:
    # clear the screen
    screen.fill((0, 128, 0))

    # update the screen
    pygame.display.update()

    pygame.time.Clock().tick(120)

