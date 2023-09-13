PYGBAG_FS = 3
__import__("os").chdir(__import__("tempfile").gettempdir())

def fs_decode(fsname, o248):
    from pathlib import Path

    filename = Path.cwd() / fsname
    if not filename.is_file():
        filename.parent.mkdir(parents=True, exist_ok=True)
        print("FS:", filename)
        with open(fsname, "wb") as fs:
            for input in o248.split("\n"):
                if not input:
                    continue
                fs.write(bytes([ord(c) - 248 for c in input]))


fs_decode(
    "resources_compiled/shaders/mdl.fsb",
    """
ľŋŀăŭǬşƣøøøøøøǉùøøŨŪŝśšūšŧŦĘŠšşŠŨĘūřťŨŤŝŪĪļĹŪŪřűĳĂŨŪŝśšūšŧŦĘŠšşŠŨĘšŦŬĳĂŨŪŝśšūšŧ
ŦĘŠšşŠŨĘŞŤŧřŬĳĂŧŭŬĘŮŝśĬĘŚşŞŰŗľŪřşĻŧŤŧŪĳĂšŦĘŮŝśīĘŮņŧŪťřŤĳĂŮŧšŜĘťřšŦĘĠġĂųĂĘĘŮŝśīĘ
ŬťŨŮřŪŗĩĳĂĘĘŬťŨŮřŪŗĩĘĵĘŦŧŪťřŤšŲŝĠŮņŧŪťřŤġĳĂĘĘŚşŞŰŗľŪřşĻŧŤŧŪĘĵĘťšŦĘĠĠĠŮŝśĬĠĂĘĘĘĘ
ťřŰĘĠĨĦĨĤĘĥĠŜŧŬĘĠŬťŨŮřŪŗĩĤĘŮŝśīĠĨĦįĪįīıĪıĤĘĨĦĭİĩıĩĬĬĤĘĨĦīĮīĮıĮĭġġġġĂĘĘġĘģĘĂĘĘĘĘ
ĠťřŰĘĠĨĦĨĤĘĥĠŜŧŬĘĠŬťŨŮřŪŗĩĤĘŮŝśīĠĥĨĦįĪįīıĪıĤĘĥĨĦĭİĩıĩĬĬĤĘĥĨĦīĮīĮıĮĭġġġġĘĢĘŮŝśĬĠ
ĨĦīįĭĤĘĨĦĬĪĭĤĘĨĦĭĤĘĨĦĭġġĂĘĘġĘģĘŮŝśĬĠĨĦĩĤĘĨĦĩĤĘĨĦĪĤĘĩĦĨġġĤĘŮŝśĬĠĩĦĨĤĘĩĦĨĤĘĩĦĨĤĘĩ
ĦĨġġĳĂŵĂĂø""",
)

fs_decode(
    "resources_compiled/shaders/mdl.vsb",
    """
ŎŋŀăøøøøŭǬşƣúøÿŭŗťŧŜŝŤüĘøøĘøøøøøćŭŗťŧŜŝŤŎšŝůňŪŧŢüùøøùøøøøøǓùøøŨŪŝśšūšŧŦĘŠšşŠŨĘū
řťŨŤŝŪĪļĹŪŪřűĳĂŨŪŝśšūšŧŦĘŠšşŠŨĘšŦŬĳĂŨŪŝśšūšŧŦĘŠšşŠŨĘŞŤŧřŬĳĂšŦĘŠšşŠŨĘŮŝśīĘřŗŦŧŪť
řŤĳĂšŦĘŠšşŠŨĘŮŝśīĘřŗŨŧūšŬšŧŦĳĂŧŭŬĘŠšşŠŨĘŮŝśīĘŮņŧŪťřŤĳĂŭŦšŞŧŪťĘťřŬĬĘŭŗťŧŜŝŤœīĪŕĳ
ĂŭŦšŞŧŪťĘŠšşŠŨĘťřŬĬĘŭŗťŧŜŝŤŎšŝůňŪŧŢĳĂŮŧšŜĘťřšŦĘĠġĂųĂĘĘŠšşŠŨĘŮŝśĬĘŬťŨŮřŪŗĩĳĂĘĘŬť
ŨŮřŪŗĩĦůĘĵĘĨĦĨĳĂĘĘŬťŨŮřŪŗĩĦŰűŲĘĵĘĠĠřŗŦŧŪťřŤĘĢĘĪĦĨġĘĥĘĩĦĨġĳĂĘĘŮņŧŪťřŤĘĵĘĠŭŗťŧŜŝŤ
œĨŕĘĢĘŬťŨŮřŪŗĩġĦŰűŲĳĂĘĘŠšşŠŨĘŮŝśĬĘŬťŨŮřŪŗĪĳĂĘĘŬťŨŮřŪŗĪĦůĘĵĘĩĦĨĳĂĘĘŬťŨŮřŪŗĪĦŰűŲĘ
ĵĘřŗŨŧūšŬšŧŦĳĂĘĘşŤŗňŧūšŬšŧŦĘĵĘĠŭŗťŧŜŝŤŎšŝůňŪŧŢĘĢĘŬťŨŮřŪŗĪġĳĂŵĂĂ""",
)
del fs_decode, PYGBAG_FS

import sys
import platform
import asyncio
#import pygame
import harfang as hg
hg.InputInit()
hg.WindowSystemInit()
res_x, res_y = 512, 512
# Draw models without a pipeline
async def hg3d_test():
    platform.window.transfer.hidden = true
    platform.window.canvas.style.visibility = "visible"
    await asyncio.sleep(1)
    print("===================================")
    win = hg.RenderInit('Harfang - Draw Models no Pipeline', res_x, res_y, hg.RT_OpenGLES)
    print("===================================")

    if 1:
        # vertex layout and models
        vtx_layout = hg.VertexLayoutPosFloatNormUInt8()

        cube_mdl = hg.CreateCubeModel(vtx_layout, 1, 1, 1)
        ground_mdl = hg.CreatePlaneModel(vtx_layout, 5, 5, 1, 1)

        shader = hg.LoadProgramFromFile('resources_compiled/shaders/mdl')

        # main loop
        angle = 0

        while 1: #not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
            dt = hg.TickClock()
            angle = angle + hg.time_to_sec_f(dt)

            viewpoint = hg.TranslationMat4(hg.Vec3(0, 1, -3))
            hg.SetViewPerspective(0, 0, 0, res_x, res_y, viewpoint)

            hg.DrawModel(0, cube_mdl, shader, [], [], hg.TransformationMat4(hg.Vec3(0, 1, 0), hg.Vec3(angle, angle, angle)))
            hg.DrawModel(0, ground_mdl, shader, [], [], hg.TranslationMat4(hg.Vec3(0, 0, 0)))

            hg.Frame()
            hg.UpdateWindow(win)
            await asyncio.sleep(0)


        hg.RenderShutdown()



import asyncio
import os

if sys.platform in ("emscripten","wasi",):

    async def sitecustomize():
        platform.window.python.is_ready = True
        await TopLevel_async_handler.start_toplevel(platform.shell, console=True)
        asyncio.create_task(main())
    asyncio.run(sitecustomize())


    async def main():
        with open("/data/data/org.python/assets/cpython.six","r") as f:
            print(f.read())
        print("Hello #python-fr et longue vie à Harfang3D")
        print("greetz to fra^ and MooZ")
        platform.window.debug()
        await hg3d_test()
        embed.prompt()

