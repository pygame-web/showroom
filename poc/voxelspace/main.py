# Python port of VoxelSpace by Sebastian Macke/Peter Sovietov
#
# https://jhawthorn.github.io/VoxelSpace/VoxelSpace.html

import pygbag.aio as asyncio

from aio.fetch import FS
FS("""
poc/voxelspace/maps ~/maps
├── C1W.png
└── D1.png
""", silent=False, debug=True)



import time
import math
import numpy

import json
import gzip
import sys
import pygame


from typing import Final




SCREEN_WIDTH: Final = 800
SCREEN_HEIGHT: Final = 400
BACK_COLOR = (153, 204, 255)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def load_data():
    with gzip.GzipFile("c1w.json.gz", "rb") as f:
        colors = json.loads(f.read().decode())
    with gzip.GzipFile("d1.json.gz", "rb") as f:
        heights = json.loads(f.read().decode())
    return colors, heights


class Map:
    width: int = 1024
    height: int = 1024
    shift: int = 10

    def __init__(self, cmap, hmap):
        self.cmap = cmap
        self.hmap = hmap


def load_map(colormap, heightmap):
    hmap = pygame.image.load(heightmap)
    cmap = pygame.image.load(colormap)
    return cmap, hmap


def load_level():
    return Map(*load_map("maps/C1W.png", "maps/D1.png"))



class Camera:
    x : float = 0
    y : float = 0
    z : float = 20
    depth : float = 600
    horizon : float = SCREEN_HEIGHT / 3

class Terrain:
    def __init__(self):
        self.scale_height : float = 100

        self.ybuffer = numpy.zeros(SCREEN_WIDTH)

        for i in range(SCREEN_WIDTH):
            self.ybuffer[i] = SCREEN_HEIGHT
        self.level = load_level()


    def render(self):
        global cam, SCREEN_WIDTH, SCREEN_HEIGHT

        screen.fill((0, 120, 250))

        hmap = self.level.hmap
        cmap = self.level.cmap

        cam.y = cam.y + 1


        self.ybuffer.fill(SCREEN_HEIGHT)

        depth: float = 1.0
        dd: float = 1.0


        left_x : float = .0
        left_y : float = .0

        right_x : float = .0


        i : int = 0
        scale : float = 0

        while int(depth) < cam.depth:

            left_x  = cam.x - depth
            left_y  = cam.y + depth

            right_x = cam.x + depth
            #right_y : float = self.player_y - depth

            dx : float = (right_x - left_x) / SCREEN_WIDTH
            scale = self.scale_height / depth

            samp_y : int = int(left_y) % 1024

            for i in range(SCREEN_WIDTH):
                #continue
                samp_x : int = int(left_x) % 1024

# https://www.pygame.org/docs/ref/pixelarray.html
                hcolor : int = SCREEN_HEIGHT - hmap.get_at([samp_x, samp_y]).r

                height : int = int(  (hcolor * scale) + cam.horizon)

                col = cmap.get_at([samp_x, samp_y])

                if height < self.ybuffer[i]:
                    pygame.draw.line(screen, col, (i, height), (i, self.ybuffer[i]))
                    self.ybuffer[i] = height
                left_x += dx
            depth += dd
            dd += 0.02


async def main():
    global cam, terrain

    cam = Camera()
    terrain = Terrain()
    next_tick : float = time.time() + 1
    fps : int = 0
    while 1:
        fps = fps + 1
        terrain.render()
        pygame.display.flip()
        await asyncio.sleep(0)
        t : float = time.time()
        if t >= next_tick:
            print("fps", fps / 5)
            fps = 0
            next_tick = t + 5


asyncio.run(main())


