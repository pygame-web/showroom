
# /// pyproject
# [project]
# dependencies = [
#  "pygame-ce",
#  "six",
#  "bidi",
# ]
# ///


# bidi and embedded
# https://github.com/lvgl/lvgl/issues/899

# diacritic print("\u0628\u0650\u0651")


import aio.fetch

aio.fetch.FS("""
.
fonts ~ fonts
├── Amiri-Regular.ttf
""")


DX=DY=100
X = 924
Y = 412

import pygame

#pygame.freetype.init()
#pygame._freetype.init()

if 0:

    def SysFont(name, size, bold=False, italic=False, constructor=None):
        if constructor is None:

            def constructor(fontpath, size, bold, italic):
                try:
                    font = pygame._freetype.Font(fontpath, size)
                except:

                    first_match = pygame.font.match_font( pygame.font.get_fonts() )
                    print(f"ERROR: failed to load font {name} {size=} {bold=} {italic=} using {first_match} instead")
                    try:
                        font =  pygame.freetype.Font(first_match, size)
                    except Exception as e:
                        print(e, pygame.freetype.get_error())
                        raise Exception(f"_freetype module internal error {pygame.freetype.get_error()}")

                font.strong = bold
                font.oblique = italic
                return font


        return pygame.sysfont.SysFont(name, size, bold, italic, constructor)


    pygame.freetype.SysFont = SysFont



if pygame.display.get_init():
    screen = pygame.display.get_surface()
else:
    screen = pygame.display.set_mode([X+DX, Y+DY]).subsurface( (DX, DY,X,Y) )

green = pygame.Color("green")
blue = pygame.Color("blue")
white = pygame.Color("white")






from bidi.algorithm import get_display as bidi

async def main():
    global localized1, localized2

    import tempfile
    await aio.fetch.preload()


    print(" \npygame.font.init")

    await asyncio.sleep(0)


    await asyncio.sleep(1)

    if not sys.argv[-1].endswith('.py'):
        fnt = sys.argv[-1]
    else:
        fnt =  "Amiri-Regular"

    print(fnt)

    import os
    fnt_path = f"{os.getcwd()}/fonts/{fnt}.ttf"

    with open('fc-list','w') as file:
        file.write(f"{fnt_path}: Amiri:style=Regular\n")

    with open('fc-list','r') as file:
        print("FC CACHE:")
        print(file.read())
        print()


    FT = true
    if FT:
        import pygame.freetype
        font = pygame.freetype.SysFont("Amiri", size=64)
        font.kerning = True
    else:
        font = pygame.font.Font(f"fonts/{fnt}.ttf", 64)
        pygame.font.init()

        await asyncio.sleep(0)

    print("get_sdl_ttf_version :", pygame.font.get_sdl_ttf_version() )

    print(f"{pygame.freetype.get_default_font()=}" )

    print("setting script")

    await asyncio.sleep(0)

    if not FT:
        font.set_script("Arab")
        FT = false


    # RTL + latin
    localized1 =  "علي"
    localized1 += " : "
    localized1 += "ALI"

    # LTR latin + Arabic
    localized2 = "ALI translates to "
    localized2 +=  "علي"

    if FT:
        text1, textRect1 = font.render( bidi(localized1), fgcolor=green, bgcolor=blue)
        text2, textRect2 = font.render( bidi(localized2), fgcolor=green, bgcolor=blue)
        text3, textRect3 = font.render( fnt , fgcolor=green, bgcolor=blue)

    else:
        text1 = font.render( bidi(localized1),  True, green, blue)
        text2 = font.render( bidi(localized2),  True, green, blue)
        text3 = font.render( fnt ,  True, green, blue)

        # create a rectangular object for the
        # text surface object
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect3 = text3.get_rect()

    textRect1.center = (X // 2, Y // 5)
    textRect2.center = (X // 2, Y // 2)
    textRect3.center = (X // 2, int(Y / 1.2) )

    clock = pygame.time.Clock()

    # infinite loop
    while True:

        # completely fill the surface object
        # with white color
        screen.fill(white)

        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)
        screen.blit(text3, textRect3)

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                return

            # Draws the surface object to the screen.

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

    # deactivates the pygame library
    pygame.quit()

    # quit the program.
    quit()



asyncio.run(main())

