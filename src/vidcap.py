import pygame, os

# numpy cv2


import platform

import pygame.vidcap as camera

from PIL import Image

async def main():
    global cam
    cam = camera.Camera( camera.list_cameras()[0], (320,200), 0 )
    await cam.start()

    # cam.get_raw()

    screen = shell.pg_init()


    await asyncio.sleep( 1 )

    while True:
        #await cam.get_image()
        try:
            if not os.path.isfile("/dev/video0.bmp"):
                im = Image.open("/dev/video0")
                im.save("/dev/video0.bmp")
            else:
                surf = pygame.image.load_basic("/dev/video0.bmp")
                screen.blit(surf, (1, 1))
                pygame.display.update()
                os.unlink("/dev/video0.bmp")
                del surf

        except Exception as e:
            print('frame dropped',e)
            sys.print_exception(e)
            break
        await asyncio.sleep(0)


asyncio.run(main())

