import pygbag.aio as asyncio
import platform

# /// pyproject
# [project]
# name = "test_pygame"
# version = "version"
# description = "description"
# readme = {file = "README.txt", content-type = "text/markdown"}
# requires-python = ">=3.11"
#
# dependencies = [
#    "typing_extensions",
#    "pypng",
#    "qrcode",
# ]
# ///


if 1:
    print("\n"*10)
    print("="*80)
    print()
    ua = platform.window.navigator.userAgent
    print( ua )
    print()
    print("="*80)
    from qrcode_term import qrcode_string
    print(qrcode_string(ua))

