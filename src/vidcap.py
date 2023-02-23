import pygame, os

# numpy cv2


import platform

import pygame.vidcap as camera

#from PIL import Image

if pygame.display.get_init():
    screen = pygame.display.get_surface()
else:
    screen = pygame.display.set_mode([1024, 1024]).subsurface( (100,100,900,900) )


async def main():
    global cam, screen

    cam = camera.Camera( camera.list_cameras()[0], (1280,720), 0 )

    await cam.start()


    while True:
        if await cam.query_image():
            try:
                screen.blit( cam.get_image(), (0, 0))
                pygame.display.update()

            except Exception as e:
                print('frame dropped',e)
                sys.print_exception(e)
                break
        await asyncio.sleep(0)

asyncio.run(main())

