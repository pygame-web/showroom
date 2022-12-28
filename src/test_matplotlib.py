import sys
import os
import asyncio
import platform
import pygame


import matplotlib
import matplotlib.pyplot as plt

import numpy as np


async def main():

    #screen = pygame.display.set_mode((1024, 600))
    screen = pygame.display.set_mode((854, 480))
    #screen = pygame.display.set_mode((680, 400))
    #screen = pygame.display.set_mode((640, 360))

    # Fixing random state for reproducibility
    np.random.seed(1)

    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))                 # white noise 1
    nse2 = np.random.randn(len(t))                 # white noise 2

    # Two signals with a coherent part at 10 Hz and a random part
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, s1, t, s2)
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('s1 and s2')
    axs[0].grid(True)

    cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
    axs[1].set_ylabel('Coherence')

    fig.tight_layout()

    await display(fig)

asyncio.run(main())

