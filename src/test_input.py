#
import asyncio
import sys

if sys.platform not in ('emscripten','wasi'):

    def patch_input():
        import builtins
        builtins_input = input
        async def async_input(prompt=""):
            return builtins_input(prompt)
        builtins.input = async_input

    patch_input()
    del patch_input



async def main():
    color = await input("what is your favorite colour ? ")
    print(f" {color=} ")


asyncio.run(main())
