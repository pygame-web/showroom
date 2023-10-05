import pygbag.aio as asyncio

# /// pyproject
# [project]
# name = "name"
# version = "2023"
# description = "description"
# readme = {file = "README.txt", content-type = "text/markdown"}
# requires-python = ">=3.11"
#
# dependencies = [
#  "pygame",
#  "noise",
# ]
# ///


import pygame

from noise import pnoise2, snoise2

import random

pxsize = 255

async def main():
    f = open("out.pgm", "wt")
    octaves = 1
    freq = 16.0 * octaves

    pixels = []


    f.write("P2\n256 256\n255\n")
    for y in range(256):
        for x in range(256):
            pixval = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)
            if pixval > pxsize:
                pixval = pxsize
            f.write("%s\n" % pixval )

    f.close()

    await asyncio.sleep(.5)

    shell.interactive(prompt=True)

    await asyncio.sleep(.5)

    shell.display("out.pgm")


asyncio.run(main())
