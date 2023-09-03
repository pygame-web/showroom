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


# ../../prebuilt/assetc -api GLES resources resources_gles -platform linux

FS("""
.
└── resources_compiled
    ├── core
    │   └── shader
    │       ├── font.fsb
    │       ├── font.vsb
    │       ├── imgui.fsb
    │       ├── imgui_image.fsb
    │       ├── imgui_image.vsb
    │       └── imgui.vsb
    ├── font
    │   └── default.ttf
    └── shaders
        ├── mdl.fsb
        └── mdl.vsb
""", "webgl")


print("===================================")

import harfang as hg

hg.InputInit()
hg.WindowSystemInit()


# initialize ImGui

if 0:
    # hg.AddAssetsFolder('resources_compiled')
    imgui_prg = hg.LoadProgramFromAssets('resources_compiled/core/shader/imgui')
    imgui_img_prg = hg.LoadProgramFromAssets('resources_compiled/core/shader/imgui_image')

    embed.webgl()


res_x, res_y = 1024, 600


win = hg.RenderInit("Harfang - Draw Models no Pipeline", res_x, res_y, hg.RT_OpenGLES)
print("===================================")

#hg.ImGuiInit(10, imgui_prg, imgui_img_prg)


# Draw models without a pipeline
async def main():
    global preload


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


    while not hg.ReadKeyboard().Key(hg.K_Escape): # and hg.IsWindowOpen(win):
        dt = hg.TickClock()
        angle = angle + hg.time_to_sec_f(dt)
        if 0:
            hg.ImGuiBeginFrame(res_x//2, res_y//2, hg.TickClock(), hg.ReadMouse(), hg.ReadKeyboard())

            if hg.ImGuiBegin('Window'):
                hg.ImGuiText('Hello World!')
            hg.ImGuiEnd()

            hg.SetView2D(0, 0, 0, res_x//2, res_y//2, -1, 1, hg.CF_Color | hg.CF_Depth, hg.Color.Red, 1, 0)
            hg.ImGuiEndFrame(255)


        if 1:
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
