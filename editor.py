import sys, os
import asyncio
import aio.fetch
import importlib

import os.path

import pygame
import pygments
import pygame_widgets


from pygame_texteditor import TextEditor
from pygame_widgets.button import ButtonArray


import platform

pygame.init()


# screen pixels (real, hardware)
WIDTH = int(platform.window.canvas.width)
HEIGHT = int(platform.window.canvas.height)

# reference/idealized screen pixels
REFX = 1980
REFY = 1080


def u(real, ref, v):
    if abs(v) < 0.9999999:
        result = int((float(real) / 100.0) * (v * 1000))
        if v < 0:
            return real - result
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


class Editor(TextEditor):
    async def on_load(self, cpath=""):

        import aio.fetch
        self.run = False

        # get pending files
        try:
            # <0.8 backward compat
            fileset = await aio.fetch.preload_fetch()
        except:
            fileset = await aio.fetch.preload()

        mappings = {"RUN": "RUN"}
        labels = []
        if len(fileset):
            cpath = (cpath or os.path.commonpath(fileset)).rstrip("/") + "/"

        for filename in fileset:
            lbl = str(filename)
            if cpath:
                lbl = lbl.replace(cpath, "")
            mappings[lbl] = filename
            labels.append(lbl)

        labels.sort()
        labels.insert(0, "RUN")

        # Creates an array of buttons
        buttonArray = ButtonArray(
            # Mandatory Parameters
            self.screen,  # Surface to place button array on
            1,  # X-coordinate
            1,  # Y-coordinate
            ux(0.100),  # Width
            self.editor_offset_Y - 1,  # Height
            (len(labels), 1),  # Shape: 2 buttons wide, 2 buttons tall
            border=1,  # Distance between buttons and edge of array
            texts=labels,  # Sets the texts of each button (counts left to right then top to bottom)
        )

        def print_idx(*argv):
            idx, button, filename = argv
            if filename == 'RUN':
                print("run!")
                self.run = True
                return
            for idx, otherbutton in enumerate(buttonArray.getButtons()):
                otherbutton.colour =  (210, 210, 180)
            #button.set('string', "[" + labels[idx] + "]" )
            button.colour = (50, 50, 50)
            print(idx, button, filename)
            with open(filename,'r') as file:
                self.set_text_from_string(file.read())

        for idx,button in enumerate(buttonArray.getButtons()):

            button.setOnClick(print_idx, (idx, button, mappings[button.string]) )



async def main():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame")
    pygame.display.get_surface().fill((200, 200, 200))  # background coloring

    # parameters

    screen = pygame.display.get_surface()  # get existing pygame window/screen
    offset_X = 0  # offset from the left border of the pygame window
    offset_Y = 24  # offset from the top border of the pygame window
    textAreaHeight = uy(0.100) - offset_Y
    textAreaWidth = ux(0.100)

    # Instantiation
    TX = Editor(offset_X, offset_Y, textAreaWidth, textAreaHeight, screen)
    TX.set_line_numbers(True)  # optional
    TX.set_syntax_highlighting(True)  # optional
    TX.set_colorscheme("bright")

    # ready to edit files
    await TX.on_load()

    while True:  # pygame-loop
        # capture input
        pygame_events = pygame.event.get()
        pressed_keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # display editor functionality once per loop
        TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)

        # display bar
        pygame_widgets.update(pygame_events)

        # update pygame window
        pygame.display.flip()
        await asyncio.sleep(0)
        if TX.run:
            break

    importlib.invalidate_caches()
    print(os.listdir("examples"))
    print(sys.path)
    await run()

asyncio.run(main())
