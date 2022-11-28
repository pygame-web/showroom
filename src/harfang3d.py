#

import sys
import platform
import asyncio




preload = []

def FS(tree, base=".", silent=False,debug=False):
    global preload
    path = [base]
    last = 0
    trail = False
    for l in map(str.rstrip, tree.split('\n')):
        if not l: continue
        if l=='.': continue
        pos, elem = l.rsplit(' ', 1)
        current = (1+len(pos))//4
        if not silent:
            print(l[4:])
        if current <= last :
            preload.append( [ '/'.join(path) , '/'.join(path[1:])] )
            if debug: print(preload[-1],'write', current, last)
            while len(path)>current:
                path.pop()
        else:
            trail = True
        #print(pos, elem, current, path, last )
        if len(path)<current+1:
            path.append(elem)
        path[current] = elem
        last = current
    if trail:
        preload.append( [ '/'.join(path) , '/'.join(path[1:])] )

async def preload_fetch(silent=False,debug=False):
    global preload
    from pathlib import Path
    while len(preload):
        url, strfilename = preload.pop(0)
        filename = Path(strfilename)
        if debug:
            print(f"{url} => {Path.cwd() / filename}")

        if not filename.is_file():
            filename.parent.mkdir(parents=True, exist_ok=True)
            async with platform.fopen(url,"rb") as source:
                with open(filename,"wb") as target:
                    target.write(source.read())
        if not silent:
            print("FS:", filename)


FS("""
.
└── resources_compiled
    ├── core
    │   └── shader
    │       ├── font.fsb
    │       └── font.vsb
    ├── font
    │   └── default.ttf
    └── shaders
        ├── mdl.fsb
        └── mdl.vsb
""", "webgl")


embed.webgl()

print("===================================")

import harfang as hg

# Draw models without a pipeline
async def main():
    global preload

    hg.InputInit()
    hg.WindowSystemInit()


    res_x, res_y = 1024, 600


    win = hg.RenderInit("Harfang - Draw Models no Pipeline", res_x, res_y, hg.RT_OpenGLES)
    print("===================================")

    #return

    print("X"*50)

    await preload_fetch(debug=True)

    print("X"*50)

    # vertex layout and models
    vtx_layout = hg.VertexLayoutPosFloatNormUInt8()

    cube_mdl = hg.CreateCubeModel(vtx_layout, 1, 1, 1)
    ground_mdl = hg.CreatePlaneModel(vtx_layout, 5, 5, 1, 1)

    shader = hg.LoadProgramFromFile("resources_compiled/shaders/mdl")

    # main loop
    angle = 0

    if 0:
        print("done")
        return

    while 1:  # not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
        dt = hg.TickClock()
        angle = angle + hg.time_to_sec_f(dt)

        viewpoint = hg.TranslationMat4(hg.Vec3(0, 1, -3))
        hg.SetViewPerspective(0, 0, 0, res_x, res_y, viewpoint)

        hg.DrawModel(
            0,
            cube_mdl,
            shader,
            [],
            [],
            hg.TransformationMat4(hg.Vec3(0, 1, 0), hg.Vec3(angle, angle, angle)),
        )
        hg.DrawModel(
            0, ground_mdl, shader, [], [], hg.TranslationMat4(hg.Vec3(0, 0, 0))
        )

        hg.Frame()
        hg.UpdateWindow(win)
        await asyncio.sleep(0)

    hg.RenderShutdown()


asyncio.run(main())

# -->
