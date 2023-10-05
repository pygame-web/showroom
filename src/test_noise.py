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


#  "netpbm",
#  "Pillow",
#  "netpbmfile",


import pygame


from noise import pnoise2, snoise2

import random

# print ID string (P5)
# print comments (if any)
# print width
# print height
# print size
# print data

rnd = random
# rnd.seed()

width = 256
height = 256
pxsize = 255

# create the PGM header
hdrstr = "P5\n%d\n%d\n%d\n" % (width, height, pxsize)

pixels = []
for i in range(0, width):
    for j in range(0, height):
        # generate random values of powers of 2
        pixval = 2 ** rnd.randint(0, 8)
        # some values will be 256, so fix them
        if pixval > pxsize:
            pixval = pxsize
        # endif
        pixels.append(pixval)

# convert array to character values
outpix = "".join(map(chr, pixels))

# append the "image" to the header
outstr = hdrstr + outpix

# and write it out to the disk
FILE = open("pgmtest.pgm", "w")
FILE.write(outstr)
FILE.close()




async def main():
    f = open("out.pgm", "wt")
    octaves = 1
    freq = 16.0 * octaves

    pixels = []

    if 1:
        f.write("P2\n256 256\n255\n")
        for y in range(256):
            for x in range(256):
                pixval = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)
                if pixval > pxsize:
                    pixval = pxsize
                f.write("%s\n" % pixval )
    else:
        f.write("P5\n256\n256\n255\n")
        for x in range(256):
            for y in range(256):
                pixval = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)
                if pixval > pxsize:
                    pixval = pxsize
                pixels.append(pixval)
        f.write("".join(map(chr, pixels)))

    f.close()

    #shell.display("pgmtest.pgm")

    await asyncio.sleep(.5)

    shell.interactive(prompt=True)

    await asyncio.sleep(.5)

    # shell.display("pgmtest.pgm")

    shell.display("out.pgm")


asyncio.run(main())
