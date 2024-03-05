#code: https://paste.pythondiscord.com/wuxuxeluje.py

import pygame
import asyncio
import aio.fetch

aio.fetch.FS("""
https://github.com/pygame-web/showroom/tree/main
sfx ~ sfx
├── click.ogg
└── game_music.ogg
""")


settings = {"loaded":False, "paused":False}

def load():

    if settings["loaded"]: return "music already loaded"
    file = "game_music"
    pygame.mixer.music.load("sfx/"+file+".ogg")
    pygame.mixer.music.play(-1)
    settings["loaded"] = True
    settings["paused"] = False
    return F"loaded and playing {file}"

def unload():
    if not settings["loaded"]: return "music already unloaded"
    pygame.mixer.music.unload()
    settings["loaded"] = False
    return "unloaded music"

def pause():
    if not settings["loaded"]: return "music not loaded"
    if settings["paused"]: return "music already paused"
    pygame.mixer.music.pause()
    settings["paused"] = True
    return "music paused"

def unpause():
    if not settings["loaded"]: return "music not loaded"
    if not settings["paused"]: return "music already unpaused"
    pygame.mixer.music.unpause()
    settings["paused"] = False
    return "music unpaused"

def mk_button(font:pygame.font.Font, text:str, col="black", bg_col="cyan") -> pygame.Surface:

    w, h = font.size(text)
    surf = pygame.Surface((int(w+10), int(h+10)))
    surf.fill(bg_col)
    text_surf = font.render(text, True, col)
    surf.blit(text_surf, (5, 5))

    return surf


def vol_min():
    pygame.mixer.music.set_volume(0.1)
    return f"vol set to {pygame.mixer.music.get_volume()}"

def vol_avg():
    pygame.mixer.music.set_volume(0.4)
    return f"vol set to {pygame.mixer.music.get_volume()}"

def vol_max():
    pygame.mixer.music.set_volume(0.99)
    return f"vol set to {pygame.mixer.music.get_volume()}"


async def main():
    #await aio.fetch.preload_fetch()
    pygame.init()
    W, H = 640, 360
    screen = pygame.display.set_mode((W, H), pygame.SCALED)
    font = pygame.font.SysFont("impact", 32)
    buttons = [
        ((W/4, H/6*2), mk_button(font, "load"), load),
        ((W/4*1.5, H/6*2), mk_button(font, "vmin"), vol_min),
        ((W/4*2.0, H/6*2), mk_button(font, "vavg"), vol_avg),
        ((W/4*2.5, H/6*2), mk_button(font, "vmax"), vol_max),
        ((W/4*3, H/6*2), mk_button(font, "unload"), unload),
        ((W/4, H/6*3), mk_button(font, "pause"), pause),
        ((W/4*3, H/6*3), mk_button(font, "unpause"), unpause),
        ((W/2, H/6*4), mk_button(font, "code"), lambda:"In Description"),
    ]
    relay_msg = ""
    click_sound = pygame.mixer.Sound("sfx/click.ogg")

    while True:

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        #draw

        screen.fill("lightgrey")

        for (x, y), surf, func in buttons:

            rect = pygame.Rect(x - surf.get_width()/2, y - surf.get_height()/2, *surf.get_size())
            screen.blit(surf, rect)

            if clicked and rect.collidepoint(pygame.mouse.get_pos()):
                click_sound.play()
                relay_msg = func()

        display_text_w, h = font.size(relay_msg)
        text_surf = font.render(relay_msg, True, "black")
        screen.blit(text_surf, (W/2 - display_text_w/2, H - h*1.5))

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())
