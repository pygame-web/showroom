
import sys
import asyncio
import pygame

if sys.platform in ('emscripten','wasi',):
    import aio.fetch
    aio.fetch.FS("""
.
├── Amiri-Regular.ttf
""", "fonts")

DX=DY=100
X = 924
Y = 412


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
    pygame.font.init()
    print( pygame.font.get_sdl_ttf_version() )


    fnt = "fonts/Amiri-Regular.ttf"
    print(fnt)
    font = pygame.font.Font(fnt, 64)


    font.set_script("Arab")

    localized1 =  "علي"
    localized1 += " : "
    localized1 += "ALI"

    text1 = font.render( bidi(localized1),  True, green, blue)

    localized2 = "ALI translate to "
    localized2 +=  "علي"

    text2 = font.render( bidi(localized2),  True, green, blue)


    # create a rectangular object for the
    # text surface object
    textRect1 = text1.get_rect()
    textRect1.center = (X // 2, Y // 5)

    textRect2 = text2.get_rect()
    textRect2.center = (X // 2, Y // 2)

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
        await asyncio.sleep(0)



    # deactivates the pygame library
    pygame.quit()

    # quit the program.
    quit()



if __name__ == "__main__":
    asyncio.run(main())

