
import pygbag.aio as asyncio
import aio.fetch

aio.fetch.FS("""
https://github.com/pygame-web/showroom/tree/main
sfx ~ sfx
├── 00-zero-pygbag.ogg
├── 01-one-pygbag.ogg
├── 02-two-pygbag.ogg
├── 03-three-pygbag.ogg
├── 04-four-pygbag.ogg
├── 05-five-pygbag.ogg
├── 06-six-pygbag.ogg
├── 07-seven-pygbag.ogg
├── 08-height-pygbag.ogg
├── 09-nine-pygbag.ogg
└── 10-ten-pygbag.ogg
""")


import pygame
import time
import glob

# do not try to read file here they do not exist yet on web

async def main():
    last_pos = 9999999
    current_pos = 0

    pygame.init()
    pygame.mixer.init()


    oggl = glob.glob('sfx/??-*.ogg')
    oggl.sort()
    oggl.reverse()


    if not len(oggl):
        print('fs error')
        return

    current = oggl.pop(0)
    print('first :', current)
    pygame.mixer.music.load(current)

    await asyncio.sleep(1)

    pygame.mixer.music.play()

    while True:
        current_pos = pygame.mixer.music.get_pos()
        print(current_pos)
        if current_pos<0:
            print("not playing anything")
            break

        # switch to next
        if last_pos>current_pos:
            if len(oggl):
                next = oggl.pop(0)
                print('+',next)
                current_pos = 0
                pygame.mixer.music.queue(next)

        # playback stopped
        elif not pygame.mixer.music.get_busy():
            if not len(oggl):
                print("stopped")
                break

        last_pos = current_pos

        await asyncio.sleep(0) #.016)

    print("bye")

asyncio.run(main())

