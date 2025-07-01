# https://github.com/Schwarzbaer/panda_examples/blob/master/buffer_protocol/pygame_to_panda3d.py

# /// script
#
# dependencies = [
#  "pygame-ce",
#  "panda3d",
# ]
# ///

import asyncio

from direct.showbase.ShowBase import *
from direct.task import Task
from panda3d.core import CardMaker, PTAUchar, Texture, PNMImage, Point2

import panda3d.core as p3d
import direct
import direct.task
import direct.task.TaskManagerGlobal
import direct.showbase

p3d.loadPrcFileData("", "win-size 1024 600")
p3d.loadPrcFileData("", "support-threads #f")
p3d.loadPrcFileData("", "textures-power-2 down")
p3d.loadPrcFileData("", "textures-square down")

import pygame
import random


from direct.showbase.ShowBase import ShowBase as ShowBase



class Game:
    def __init__(self):
        pygame.init()
        self.res = (320, 320)
        self.surface = pygame.Surface(self.res)

    def update(self):
        r = []
        for i in range(7):
            r.append(random.randint(0,255))
        self.surface.fill((r[0],r[1],r[2]),(r[3], r[4], r[5], r[6]))


class PygameCard(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.game = Game()
        self.camLens.setFov(120)
        self.input_img = PNMImage(self.game.res[0], self.game.res[1])
        self.input_tex = Texture()
        self.input_tex.load(self.input_img)

        self.card = CardMaker('pygame_card')
        self.screen = render.attach_new_node(self.card.generate())
        self.screen.setPos(-0.5,2,-0.5)
        self.screen.setTexture(self.input_tex)

        self.game_ram_image = self.game.surface.get_view("0")
        taskMgr.add(self.update, "update pygame_card")

    def update(self, task):
        self.game.update()
        self.input_tex.set_ram_image_as(self.game_ram_image, "RGBA")
        return task.cont


    async def async_loop(self):

        while not asyncio.get_running_loop().is_closed():
            #print(".")
            try:
                direct.task.TaskManagerGlobal.taskMgr.step()
            except SystemExit:
                print('87: Panda3D stopped',file= __import__('sys').stderr)
                break
            # go to host
            await asyncio.sleep(0)

        print(self.async_loop,"exiting")

    def async_run(self):
        self.__class__.instance = self
        aio.loop.create_task(self.async_loop())

    # patch the sync run which would prevent to enter interactive mode
    run = async_run


p = PygameCard()
p.run()
