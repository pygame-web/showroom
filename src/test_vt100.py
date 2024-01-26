
# /// script
# [project]
# name = "name"
# version = "version"
# description = "description"
# readme = {file = "README.txt", content-type = "text/markdown"}
# requires-python = ">=3.11"
#
# dependencies = [
# ]
# ///



import asyncio
import sys
import termios
import tty
import select
import os

import platform

if sys.platform in ('emscripten','wasi'):
    # vsync, host handled => good
    platform_delay = 0
else:
    # 60 Hz, asyncio timers => wrong.
    platform_delay = 0.016



def os_write(data: str) -> None:
    sys.__stdout__.write(data)

def os_flush():
    sys.stdout.flush()

def goto_xy(x, y):
    CSI(f"{y};{x}H")


def ESC(*argv, flush=True):
    for arg in argv:
        os_write(chr(0x1B))
        os_write(arg)
    if flush:
        os_flush()

def CSI(*argv):
    for arg in argv:
        ESC(f"[{arg}", flush=False)
    os_flush()



class Toolkit:

    cp = 'utf-8'


    def __enter__(self):
        stdin = sys.stdin.fileno()
        self.stdin = stdin

        # save cursor+attr
        ESC("7")

        self.attrs_before = termios.tcgetattr(stdin)
        attrs_raw = termios.tcgetattr(stdin)
        attrs_raw[tty.LFLAG] &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
        attrs_raw[tty.IFLAG] &= ~(termios.IXON | termios.IXOFF | termios.ICRNL | termios.INLCR | termios.IGNCR)
        attrs_raw[tty.CC][termios.VMIN] = 1

        termios.tcsetattr(stdin, termios.TCSANOW, attrs_raw)

        self.mouse_support_enable()
        return self


    def mouse_support_enable(self) -> None:
        # SET_VT200_MOUSE SET_ANY_EVENT_MOUSE SET_VT200_HIGHLIGHT_MOUSE  SET_SGR_EXT_MODE_MOUSE
        CSI("?1000h", "?1003h", "?1015h", "?1006h")

    # todo, handle truncated utf-8 streams
    def input(self) -> str:
        if select.select([self.stdin], [], [], 0)[0]:
            try:
                payload = os.read(self.stdin, 1024)
                if payload:
                    return payload.decode(self.cp)
            except OSError:
                ...
        return ""


    def write(self, data: str) -> None:
        os_write(data)

    def flush(self) -> None :
        os_flush()

    def mouse_support_disable(self) -> None:
        write = self.write
        write("\x1b[?1000l")  #
        write("\x1b[?1003l")  #
        write("\x1b[?1015l")
        write("\x1b[?1006l")
        self.flush()


    def __exit__(self, *argv) -> None:
        termios.tcsetattr(self.stdin, termios.TCSANOW, self.attrs_before)
        self.mouse_support_disable()
        del self.attrs_before
        # restore cur+attr
        ESC("8")





async def main():
    loop = asyncio.get_running_loop()
    tk = Toolkit()
    tk.__enter__()

    while not loop.is_closed():
        await asyncio.sleep(platform_delay)
        stdinput = tk.input()
        if len(stdinput):
            if stdinput[0]=='q':
                break
            ESC("7")
            goto_xy(10,10)
            print(repr(stdinput), end="")
            # erase to eol
            CSI("K")
            ESC("8")
    print("bye")
    tk.__exit__()


if __name__ == "__main__":
    asyncio.run(main())



