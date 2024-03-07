import pygbag.aio as asyncio

# /// script
# dependencies = [
#  "pygame-ce",
#  "noise",
# ]
# ///

import pygame
import noise
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
            pixval = int(noise.snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)
            if pixval > pxsize:
                pixval = pxsize
            f.write("%s\n" % pixval )

    f.close()

    await asyncio.sleep(.5)

    shell.interactive(prompt=True)

    await asyncio.sleep(.5)


    shell.display("out.pgm")


asyncio.run(main())
