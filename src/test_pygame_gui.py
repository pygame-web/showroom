# /// script
# dependencies = [
#  "pygame-ce",
#  "pygame-gui",
#  "python-i18n",
# ]
# ///


import pygame
import pygame_gui
import i18n

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))


class Window(pygame_gui.elements.UIWindow):
    def __init__(self,
                 rect: pygame.Rect,
                 camera_name,
                 ui_manager: pygame_gui.core.interfaces.IUIManagerInterface):
        super().__init__(rect, ui_manager, window_display_title=camera_name, resizable=True)

    def update(self, time_delta: float):
        super().update(time_delta)





async def main():
    clock = pygame.time.Clock()
    is_running = True

    window_rect = pygame.Rect(0, 0, 400, 300)
    window_rect.topleft = [10,10]
    Window(window_rect, "Untitled pygame-gui window that can move", manager)


    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())

