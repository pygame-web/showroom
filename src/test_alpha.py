# /// script
# dependencies = [
#  "pygame-ce",
# ]
# ///

import pygame
import asyncio
import platform, sys

if sys.platform in ('emscripten', 'wasi'):
    platform.document.body.style.background = "#00FF00"
    platform.window.canvas.style.imageRendering = "pixelated"

import pygame
pygame.init()

async def main():
    print("""



    MOVE MOUSE OVER CANVAS




    """)

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    BLUE = pygame.Color('dodgerblue4')
    # I just create the background surface in the following lines.
    background = pygame.Surface(screen.get_size())
    background.fill((90, 120, 140))
    for y in range(0, 600, 20):
        for x in range(0, 800, 20):
            pygame.draw.rect(background, BLUE, (x, y, 20, 20), 1)

    # This dark gray surface will be blitted above the background surface.
    surface = pygame.Surface(screen.get_size()).convert_alpha()
    surface.fill(pygame.Color('gray11'))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEMOTION:
                surface.fill(pygame.Color('gray11'))  # Clear the gray surface ...
                # ... and draw a transparent circle onto it to create a hole.
                pygame.draw.circle(surface, (255, 255, 255, 0), event.pos, 90)

        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))

        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
