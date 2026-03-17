#
import asyncio
import sys
import os

async def main():

    q = "what is your favorite colour ? "

    if sys.platform in ('emscripten','wasi'):

        if "PYGBAG" not in os.environ:
            print("you need pygbag runtime for async input on terminal main thread")
        else:
            # import platform
            # platform.window.set_raw_mode(1)

            # if not using raw input, add EOT manually to flush prints
            q += sys.__eot__

            def goto_xy(x, y):
                CSI(f"{y};{x}H")

            CSI("2J")
            goto_xy(1,10)
            color = await input(q)
    else:
        color = input(q)

    print(f" {color=} ")

asyncio.run(main())
