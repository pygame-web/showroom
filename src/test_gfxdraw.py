#!/usr/bin/env python

"""Proof of concept gfxdraw example"""

import asyncio
import pygame
import pygame.gfxdraw
import pygame.draw

async def main():
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    screen.fill((255, 0, 0))
    s = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    pygame.draw.line(s, (0,0,0), (250, 250), (250+200,250))

    width = 1
    for a_radius in range(width):
        radius = 200
        #pygame.gfxdraw.aacircle(s, 250, 250, radius-a_radius, (0, 0, 0))
        pygame.draw.circle(s, (0, 0, 0), (250, 250), radius-a_radius, width=1)

    screen.blit(s, (0, 0))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    run = False
                    break
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()

if __name__ == '__main__':
    asyncio.run(main())
