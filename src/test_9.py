
import pygbag.aio as asyncio
import aio.fetch


aio.fetch.FS("""
https://github.com/pygame-web/showroom/tree/main
sfx ~ sfx
└── 09-nine-pygbag.ogg
""")





import pygame


pygame.init()
pygame.mixer.init()


async def main():
    sound = pygame.mixer.Sound("sfx/09-nine-pygbag.ogg")
    angle = -90

    if 0:
        while True:
            channel = sound.play()
            for angle in [-90,-45,0,45,90]:
                channel.set_source_location(angle, 100)
                await asyncio.sleep(0.1)
            await asyncio.sleep(1.5)
    else:
        for angle in [-90,90]*10:
            channel = sound.play()
            channel.set_source_location(angle, 100)
            await asyncio.sleep(1.2)

asyncio.run(main())
