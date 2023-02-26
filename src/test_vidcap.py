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
    FRAMES = 0
    DROPS = 0
    cam = camera.Camera( camera.list_cameras()[0], (640, 480), 0 )

    await cam.start()
    last  = 0
    cnt = 0

    while True:
        if cnt==300:
            print(f"Frame {DROPS=} {FRAMES=}")
            if os.path.isfile(cam.device):
                with open(cam.device) as file:
                    fd = file.fileno()
                    if last!=fd:
                        print(fd)
                        last = fd
                cnt = 0
        cnt += 1

        if cam.query_image():
            FRAMES += 1
            screen.blit( cam.get_image(), (0, 0))
            pygame.display.update()
        else:
            DROPS +=1
            #print(f"Frame {DROPS=} {FRAMES=}")
        await asyncio.sleep(0)


asyncio.run(main())

