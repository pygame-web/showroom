#!python3

# /// script
# dependencies = [
#    "cycler",
#    "kiwisolver",
#    "numpy",
#    "packaging",
#    "Pillow",
#    "pyparsing",
#    "dateutil",
#    "pytz",
#    "six",
#    "matplotlib",
#    "pygame-ce",
# ]
# ///


import asyncio
import pygame
import os
import matplotlib.pyplot as plt




async def main():
    import matplotlib.pyplot as plt
    import numpy as np
    import time


    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Make the X, Y meshgrid.
    xs = np.linspace(-1, 1, 50)
    ys = np.linspace(-1, 1, 50)
    X, Y = np.meshgrid(xs, ys)

    # Set the z axis limits so they aren't recalculated each frame.
    ax.set_zlim(-1, 1)

    # Begin plotting.
    wframe = None
    tstart = time.time()
    for phi in np.linspace(0, 180. / np.pi, 100):
        # If a line collection is already remove it before drawing.
        if wframe:
            wframe.remove()
        # Generate data.
        Z = np.cos(2 * np.pi * X + phi) * (1 - np.hypot(X, Y))
        # Plot the new wireframe and pause briefly before continuing.
        wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
        if os.uname().machine.startswith("wasm"):
            await plt.pause(0)
        else:
            plt.pause(0.016)


    print('Average FPS: %f' % (100 / (time.time() - tstart)))


asyncio.run(main())

