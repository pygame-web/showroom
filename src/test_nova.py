import pygbag.aio as asyncio
from math import pi, degrees
from time import perf_counter

import pygame
import nova

async def main():

    # Configuration
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    MAX_FPS = 165
    DT = 1.0 / 60.0


    # Initialize pygame & create window
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame-CE & Nova Physics Example for Pygbag")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 14)
    y_gap = 17
    bg_color = (32, 32, 36)
    body_color = (237, 244, 255)
    hud_surface = pygame.Surface((150, y_gap * 5 + 5 * 6)).convert()
    hud_surface.set_alpha(128)


    # Create space instance
    space = nova.Space()

    # Create a SHG (Spatial Hash Grid) with 3.0m x 3.0m cells.
    space.set_shg(
        0.0, 0.0, WINDOW_WIDTH / 10.0, WINDOW_HEIGHT / 10.0,
        3.0, 3.0
    )


    # Create grounds & walls

    ground = nova.create_rect(nova.STATIC, 64, 72 - 2.5, 0, 1.0, 0.0, 0.7, 128, 5)
    space.add(ground)

    platform0 = nova.create_rect(nova.STATIC, 36, 21, pi / 7, 1.0, 0.0, 0.2, 50, 2.0)
    space.add(platform0)

    platform1 = nova.create_rect(nova.STATIC, 128-36, 41, -pi / 7, 1.0, 0.0, 0.2, 50, 2.0)
    space.add(platform1)

    wall_left = nova.create_rect(nova.STATIC, 15, 36, 0.2, 1.0, 0.0, 0.7, 5, 100)
    space.add(wall_left)

    wall_right = nova.create_rect(nova.STATIC, 113, 36, -0.2, 1.0, 0.0, 0.7, 5, 100)
    space.add(wall_right)

    # Create objects
    rows = 15
    cols = 5
    size = 3.0
    for y in range(rows):
        for x in range(cols):
            if (x + y) % 10 == 0:
                ball = nova.create_rect(
                    nova.DYNAMIC, 43 + x * size, -rows/2-60 + y * size - 40, 0.0, 1.0, 0.08, 0.05, size, size)
            else:
                ball = nova.create_circle(
                    nova.DYNAMIC, 43 + x * size, -rows/2-60 + y * size - 40, 0.0, 1.0, 0.08, 0.05, size / 2)

            space.add(ball)
            ball.apply_force(nova.Vector2(0.0, 10000.0/4))

    # Profiling variables
    step_end = 0.0
    render_end = 0.0

    selected = None

    # Game loop
    while True:
        clock.tick(MAX_FPS)

        mouse_ = pygame.mouse.get_pos()
        mouse = nova.Vector2(mouse_[0] / 10.0, mouse_[1] / 10.0)

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected is None:
                    for body in space.get_bodies():
                        if body.type == nova.STATIC: continue

                        aabb = body.get_aabb()
                        rect = pygame.Rect(aabb[0]*10, aabb[1]*10, (aabb[2] - aabb[0])*10, (aabb[3] - aabb[1])*10)

                        if rect.collidepoint(*mouse_):
                            selected = body
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                selected = None

        if selected:
            selected_pos = selected.position
            delta = pygame.Vector2((mouse - selected_pos).x, (mouse - selected_pos).y)
            strength = 400
            force = delta * strength
            selected.apply_force(nova.Vector2(force.x, force.y))


        step_start = perf_counter()

        # Advance the simulation
        space.step(
            DT, # Timestep
            10,  # Velocity iteration count
            10,  # Position iteration count
            5,  # Constraint iteration count
            1   # Substep count
        )

        step_end = perf_counter() - step_start


        # Rendering

        render_start = perf_counter()
        window.fill(bg_color)


        if selected:
            body_pos = selected.position
            body_pos = (body_pos.x * 10, body_pos.y * 10)
            pygame.draw.line(window, (150, 150, 150), body_pos, mouse_, 1)


        # Render bodies

        for body in space.get_bodies():
            if body.shape == 0:
                position = body.position * 10.0
                radius = pygame.Vector2(1.0, 0.0).rotate(degrees(body.angle)) * (body.radius * 10.0 - 1)
                r = position + nova.Vector2(radius.x, radius.y)

                pygame.draw.circle(
                    window,
                    body_color,
                    (position.x, position.y),
                    round(body.radius * 10.0),
                    1
                )

            elif body.shape == 1:
                vertices = [((v * 10.0).x, (v * 10.0).y) for v in body.get_vertices()]
                pygame.draw.polygon(window, body_color, vertices, 1)


        # Draw UI

        window.blit(hud_surface, (0, 0))

        window.blit(
            font.render(f"Pygame-CE {pygame.version.ver}", True, (255, 255, 255)),
            (5, 5 + y_gap*0)
        )

        window.blit(
            font.render(f"Nova Physics {nova.nova_version}", True, (255, 255, 255)),
            (5, 5 + y_gap*1)
        )

        window.blit(
            font.render(f"FPS: {round(clock.get_fps(), 1)}", True, (255, 255, 255)),
            (5, 5 + y_gap*2)
        )

        window.blit(
            font.render(f"Physics: {round(step_end * 1000, 2)} ms", True, (255, 255, 255)),
            (5, 5 + y_gap*3)
        )

        window.blit(
            font.render(f"Render: {round(render_end * 1000, 2)} ms", True, (255, 255, 255)),
            (5, 5 + y_gap*4)
        )

        window.blit(
            font.render(f"Bodies: {len(space.get_bodies())}", True, (255, 255, 255)),
            (5, 5 + y_gap*5)
        )

        render_end = perf_counter() - render_start


        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())

