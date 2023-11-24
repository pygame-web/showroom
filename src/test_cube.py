#!python3

# /// pyproject
# [project]
# name = "test_pygame"
# version = "version"
# description = "description"
# readme = {file = "README.txt", content-type = "text/markdown"}
# requires-python = ">=3.11"
#
# dependencies = [
#    "pygame.base",
# ]
# ///


import sys
import math
import pygame
screen_width, screen_height = 640, 480

async def main():
    D=1
    await asyncio.sleep(D)

    pygame.init()
    await asyncio.sleep(D)

    screen = pygame.display.set_mode((screen_width, screen_height), 0)
    await asyncio.sleep(D)

    pygame.display.set_caption("Spinning Solid Cube")

    print("""

    # set up the window


""")


    def face_distance(face):
        distance = 0
        for i in face:
            for k in range(3):
                distance += (cube_points_rotated[i][k] - camera_position[k])**2
        return distance


    # set up the cube
    cube_size = 50
    cube_points = [(-cube_size, -cube_size, -cube_size),
                   (cube_size, -cube_size, -cube_size),
                   (cube_size, cube_size, -cube_size),
                   (-cube_size, cube_size, -cube_size),
                   (-cube_size, -cube_size, cube_size),
                   (cube_size, -cube_size, cube_size),
                   (cube_size, cube_size, cube_size),
                   (-cube_size, cube_size, cube_size)]

    cube_faces = [(0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2),
                  (2, 6, 7, 3), (3, 7, 4, 0), (4, 7, 6, 5)]

    # create a dictionary that maps each face to its corresponding color
    face_colors = {
        (0, 1, 2, 3): (255, 0, 0),   # red
        (0, 4, 5, 1): (0, 255, 0),   # green
        (1, 5, 6, 2): (0, 0, 255),   # blue
        (2, 6, 7, 3): (255, 255, 0), # yellow
        (3, 7, 4, 0): (0, 255, 255), # cyan
        (4, 7, 6, 5): (255, 0, 255)  # magenta
    }

    # set up the rotation angles
    angle_x = 0
    angle_y = 0
    angle_z = 0

    # set up the camera
    camera_position = [0, 0, -500]
    camera_orientation = [0, 0, 0]

    # main game loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # clear the screen
        screen.fill((0, 0, 0))

        # rotate the cube
        angle_x += 0.01
        angle_y += 0.02
        angle_z += 0.03

        rotation_x = [[1, 0, 0],
                      [0, math.cos(angle_x), -math.sin(angle_x)],
                      [0, math.sin(angle_x), math.cos(angle_x)]]

        rotation_y = [[math.cos(angle_y), 0, math.sin(angle_y)],
                      [0, 1, 0],
                      [-math.sin(angle_y), 0, math.cos(angle_y)]]

        rotation_z = [[math.cos(angle_z), -math.sin(angle_z), 0],
                      [math.sin(angle_z), math.cos(angle_z), 0],
                      [0, 0, 1]]

        cube_points_rotated = []

        for point in cube_points:
            # rotate the point using the three rotation matrices
            point_rotated = point
            point_rotated = [sum([rotation_x[i][j] * point_rotated[j] for j in range(3)]) for i in range(3)]
            point_rotated = [sum([rotation_y[i][j] * point_rotated[j] for j in range(3)]) for i in range(3)]
            point_rotated = [sum([rotation_z[i][j] * point_rotated[j] for j in range(3)]) for i in range(3)]

            # add the rotated point to the list of rotated points
            cube_points_rotated.append(point_rotated)

        # sort the faces based on their distance from the camera
        sorted_faces = sorted(cube_faces, key=face_distance)

        # draw the faces of the cube as polygons
        for face in sorted_faces:
            points = [cube_points_rotated[i] for i in face]
            color = face_colors[face]
            pygame.draw.polygon(screen, color, [(p[0] + screen_width / 2, p[1] + screen_height / 2) for p in points])

        # update the screen
        pygame.display.update()
        await asyncio.sleep(0)
        pygame.time.Clock().tick(120)

asyncio.run(main())

