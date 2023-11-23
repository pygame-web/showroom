import pygame

pygame.init()

# set up the window
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("blank")

# main game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # clear the screen
    screen.fill((0, 0, 0))

    # update the screen
    pygame.display.update()

    pygame.time.Clock().tick(120)

