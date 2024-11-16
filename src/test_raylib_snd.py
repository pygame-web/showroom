PYGBAG_FS=1
# fmt: off
__import__('os').chdir(__import__('tempfile').gettempdir())
def fs_decode(fsname, o248):
    from pathlib import Path
    filename = Path.cwd() / fsname
    if not filename.is_file():
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(fsname,"wb") as fs:
            for input in o248.split("\n"):
                if not input: continue
                fs.write(bytes([ord(c) - 248 for c in input]))


fs_decode('resources/wabbit_alpha.png','''
ƁňņĿąĂĒĂøøøąŁŀļŊøøøĘøøøĘĀüøøøǑūƪŷøøùƯŁļĹŌŰǒżƍǅŭǛĨĄżķǜƩƎōęųǅƮƙúĚƏęǲƖƬǙŔǋƿŒġŞǮĘƀĚ
ĠŪƻǯŤǑĘĩĔǴĄŜǚŐŗĀǛįŎńƪǵőœǦĀĻĤŦŁŌǃøǋǂüĀƻƌąĎĵǆċŒǅĈŎĤùŘǗĨŖùǰŬēĴǵƶÿŘǆǘŐħĥûƢǅŠǗƗǉƵùƀƦ
ĢƔǲǳƏĈǚřǐƔŨƗŁſƹšǆĸƾŐőŬŋþǦŦǕħŊýĳŘŨǯǷƱǤǜƈſėĐŸưřǍŕǃĨċŅĊčƢĉśƦţŜĵøĭűƠǕǎúŧąǏǌƣǯŉƸŻǰǢƳ
ŮāƭŢǫǛĿǮųǮøǖŸųčǭƼƗľğǡŨƗĻƂŬǡĽűŧĴƂņŮƀǌŮǎǞŊǒķǑśŎŹǑƒŞƶżĨěƞĺǰŘǭŕƍƯēúǄŦǰǈǄƾħŘŪōĖǂǔĈįƪ
šǌǂŭǴĎǔǙƭǬĽƣƐŬǥĨăƵĖƭűŅŨƂŕƘňǩǶƂŢŀǵűƘƙƣƅƬƘǞǞğƇǢǐğǓĽęąûƳǔǭǥŋũſƫùƳŌŇûŽŬƑƳǁƑǭƻłĩƶĠǖş
ĝƧơǐÿŋőǅƯźƳƩōĢǍŰƠƖěŜšƠǆǴŝŢŐŮƊŰŘħǖǒşǆķĬǫǴǗŀŋŰŭǬřųƍŰǡƏǩĂœĳąĿŒĳďǇǪƖĈŧǛįƋďǁńƟǒǇǭĶƨǷ
ēøŴźƬĥŔžĲħøøøøŁĽņļƦĺŘź''')

# fmt:on
del fs_decode, PYGBAG_FS

# /// script
# dependencies = [
#     "cffi",
#     "raylib",
# ]
# ///

import pygbag.aio as asyncio

import aio.fetch


aio.fetch.FS("""
https://github.com/pygame-web/showroom/tree/main
sfx ~ sfx
└── game_music.ogg
""")


import platform
if 0:
    platform.window.eval("""
VM._ma_device_process_pcm_frames_playback__webaudio = console.log
VM._ma_device_process_pcm_frames_playback__webaudio
VM._ma_device__on_notification_unlocked = console.log
""")


# Dont use C data structures when we can avoid it.  Makes Pypy slightly faster.


from raylib import *
import random

async def main():

    try:
        MAX_BUNNIES = int(sys.argv[-1])
    except:
        MAX_BUNNIES      =  10000

    # This is the maximum amount of elements (quads) per batch
    # NOTE: This value is defined in [rlgl] module and can be changed there
    MAX_BATCH_ELEMENTS  = 8192


    class Bunny:
        def __init__(self):
            self.position_x = 0.0
            self.position_y = 0.0
            self.speed_x = 0.0
            self.speed_y = 0.0
            self.color_r = 0
            self.color_g = 0
            self.color_b = 0
            self.color_a = 0


    # // Initialization
    # //--------------------------------------------------------------------------------------
    screenWidth = 1920;
    screenHeight = 1080;

    InitWindow(screenWidth, screenHeight, b"raylib [textures] example - bunnymark")

    print("================================================================")
    InitAudioDevice()
    print("================================================================")


    import platform
    platform.window.window_resize()
    # // Load bunny texture
    texBunny = LoadTexture(b"resources/wabbit_alpha.png")


    fxogg = LoadSound(b"sfx/game_music.ogg");

    bunnies = []
    for i in range(0, MAX_BUNNIES):
        bunnies.append(Bunny())

    bunniesCount = 0;          # Bunnies counter

    SetTargetFPS(60);               # Set our game to run at 60 frames-per-second
    #//--------------------------------------------------------------------------------------

    await asyncio.sleep(0)
    for i in range(0, MAX_BUNNIES):
        bunnies[bunniesCount].position_x = 100
        bunnies[bunniesCount].position_y = 100
        bunnies[bunniesCount].speed_x = random.randint(-250, 250)/60.0
        bunnies[bunniesCount].speed_y = random.randint(-250, 250)/60.0
        bunnies[bunniesCount].color_r = random.randint(50,240)
        bunnies[bunniesCount].color_g = random.randint(80, 240)
        bunnies[bunniesCount].color_b = random.randint(100, 240)
        bunnies[bunniesCount].color_a = 255
        bunniesCount+=1


    PlaySound(fxogg)

    #// Main game loop
    while not WindowShouldClose():    #// Detect window close button or ESC key

        # // Update bunnies
        for i in range(0, bunniesCount):
            bunnies[i].position_x += bunnies[i].speed_x
            bunnies[i].position_y += bunnies[i].speed_y

            if ((bunnies[i].position_x + texBunny.width/2) > GetScreenWidth()) or ((bunnies[i].position_x + texBunny.width/2) < 0):
                bunnies[i].speed_x *= -1
            if ((bunnies[i].position_y + texBunny.height/2) > GetScreenHeight()) or ((bunnies[i].position_y + texBunny.height/2 - 40) < 0):
                bunnies[i].speed_y *= -1

        # //----------------------------------------------------------------------------------
        #
        # // Draw
        # //----------------------------------------------------------------------------------
        BeginDrawing()

        ClearBackground(RAYWHITE)

        for i in range(0, bunniesCount):
            # // NOTE: When internal batch buffer limit is reached (MAX_BATCH_ELEMENTS),
            # // a draw call is launched and buffer starts being filled again;
            # // before issuing a draw call, updated vertex data from internal CPU buffer is send to GPU...
            # // Process of sending data is costly and it could happen that GPU data has not been completely
            # // processed for drawing while new data is tried to be sent (updating current in-use buffers)
            # // it could generates a stall and consequently a frame drop, limiting the number of drawn bunnies
            DrawTexture(texBunny, int(bunnies[i].position_x), int(bunnies[i].position_y), (bunnies[i].color_r,bunnies[i].color_g,bunnies[i].color_b,bunnies[i].color_a))

        DrawRectangle(0, 0, screenWidth, 40, BLACK)
        text = f"bunnies {bunniesCount}"
        DrawText(text.encode('utf-8'), 120, 10, 20, GREEN)
        text = f"batched draw calls: { 1 + int(bunniesCount/MAX_BATCH_ELEMENTS)}"
        DrawText(text.encode('utf-8'), 320, 10, 20, MAROON)

        DrawFPS(10, 10)

        EndDrawing()
        #//----------------------------------------------------------------------------------
        await asyncio.sleep(0)

    #// De-Initialization
    #//--------------------------------------------------------------------------------------

    UnloadSound(fxogg);

    UnloadTexture(texBunny);   #Unload bunny texture

    CloseWindow()              # Close window and OpenGL context
    #//--------------------------------------------------------------------------------------

asyncio.run(main())

