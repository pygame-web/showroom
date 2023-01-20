import asyncio
import pygame
import pygame_widgets


async def main():
    print("\n"*20)
    await input("Press Enter to connect usb serial port\n\n")
    await jsiter( window.io.open_serial())
    print("connected!")


asyncio.run(main())

