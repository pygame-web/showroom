import platform

# /// pyproject
# [project]
# name = "name"
# version = "version"
# description = "description"
# readme = {file = "README.txt", content-type = "text/markdown"}
# requires-python = ">=3.11"
#
# dependencies = [
#     "pygame-ce",
# ]
# ///

import pygame

def on_upload_files(ev):
    print("on_upload_files", ev)
    if ev.mimetype.startswith('image/'):
        # we can display that
        shell.display(ev.text)

platform.EventTarget.addEventListener(None, "upload", on_upload_files )

platform.window.dlg_multifile.hidden = false


async def main():
    shell.interactive(prompt=True)
    while not aio.exit:
        await asyncio.sleep(0)

asyncio.run(main())
