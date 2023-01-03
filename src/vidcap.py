import pygame, numpy, cv2

# style="display:none;"
import platform

def list_cameras():
    return [0]


class Camera:

    def __init__(self, device, size, format):
        self.width, self.height = size
        self.format = format

    async def start(self):
        status = await platform.jsiter( platform.window.MM.camera.init(self.width, self.height, 0, self.format) )
        print(f"camera {status=}")

    def query_image(self):
        platform.window.MM.camera.get_raw()


    async def get_image(self):
        print("get_image:", await platform.jsprom( platform.window.MM.camera.get_image() ) )


    def get_raw(self):
        platform.window.MM.camera.get_raw()


async def main():
    global cam
    cam = Camera( list_cameras()[0], (320,200), 0 )
    await cam.start()
    # cam.get_raw()
    await cam.get_image()
    shell.display("/dev/video0")




asyncio.run(main())

