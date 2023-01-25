import asyncio
import pygame
import pygame_widgets
from pygame_widgets.button import Button


pygame.init()

# reference/idealized screen pixels
REFX = 1980
REFY = 1080

# screen pixels (real, hardware)
WIDTH = 1024  # {{cookiecutter.width}}
HEIGHT = 600  # {{cookiecutter.height}}


def u(real, ref, v):
    if abs(v) < 0.9999999:
        result = int((float(real) / 100.0) * (v * 1000))
        if v < 0:
            return real + result
        return result
    return int((real / ref) * v)


def ux(*argv):
    global WIDTH, REFX
    acc = 0
    for v in argv:
        acc += u(WIDTH, REFX, v)
    return acc


def uy(*argv):
    global HEIGHT, REFY
    acc = 0
    for v in argv:
        acc += u(HEIGHT, REFY, v)
    return acc


async def main():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pad = 15  # relative to reference (here 1980) !

    padx = ux(pad) # report to 1024
    pady = uy(pad) # report to 600


    screen.fill("aquamarine4")

    #                           padx, pady,  width 50% -padx,  height 33% - pady
    button = Button(screen, padx, pady, ux(0.050) - padx, uy(0.033) - pady, text="Row 1_C1")
    button = Button(screen, ux(.050) + padx, pady, ux(.040) -padx, uy(.033)-pady, text="Row 1_C2")

    button = Button(screen, padx, uy(.033)+padx, ux(.090)-pady, uy(.033)-pady, text="Row 2_span")

# or use pad as second value
    button = Button(screen, ux(pad), uy(.066, +pad), ux(.090, -pad) , uy(0.033, -pad) , text="Row 3_span" )

# here -10% from max X instead of 90% from 0
    button = Button(screen, ux(-.010, +pad), uy(pad), ux(.010, -2*pad) , uy(0.100, -2*pad) , text="span_C3" )


    pygame_widgets.update(pygame.event.get())
    pygame.display.update()


asyncio.run(main())
