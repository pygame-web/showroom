
import aio
import asyncio
import time
import socket
import select


# https://github.com/emscripten-core/emscripten/issues/4586 recv MSG_PEEK flag ignored

print(" *socktest* ")

import io,socket
import aio


async def aio_sock_open(sock, host, port):
    while True:
        try:
            sock.connect(
                (
                    host,
                    port,
                )
            )
        except BlockingIOError:
            await aio.sleep(0)
        except OSError as e:
            # 30 emsdk, 106 linux
            if e.errno in (30, 106):
                return sock
            sys.print_exception(e)

class aio_sock:
    def __init__(self, url, mode, tmout):
        host, port = url.rsplit(":", 1)
        self.port = int(port)
        # we don't want simulator to fool us
        if __WASM__ and __import__("platform").is_browser:
            if not url.startswith("://"):
                pdb(f"switching to {self.port}+20000 as websocket")
                self.port += 20000
            else:
                _, host = host.split('://', 1)

        self.host = host

        self.sock = socket.socket()
        # self.sock.setblocking(0)

    # overload socket directly ?

    def fileno(self):
        return self.sock.fileno()

    def send(self, *argv, **kw):
        self.sock.send(*argv, **kw)

    def recv(self, *argv):
        return self.sock.recv(*argv)

    # ============== specific ===========================

    async def __aenter__(self):
        # use async
        print("64: aio_sock_open", self.host, self.port)
        await aio_sock_open(self.sock, self.host, self.port)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        aio.protect.append(self)
        aio.defer(self.sock.close, (), {})
        del self.port, self.host, self.sock

    def read(self, size=-1):
        return self.recv(0)

    def write(self, data):
        if isinstance(data, str):
            return self.sock.send(data.encode())
        return self.sock.send(data)

    def print(self, *argv, **kw):
        kw["file"] = io.StringIO(newline="\r\n")
        print(*argv, **kw)
        self.write(kw["file"].getvalue())

    def __enter__(url, mode, tmout):
        # use softrt (wapy)
        return aio.await_for(self.__aenter__())

    def __exit__(self, exc_type, exc, tb):
        # self.sock.close()
        pass



async def irc_handler(sock):
    buf = []

    while not aio.exit:
        rr, rw, re = select.select([sock.sock], [], [], 0)
        if rr or rw or re:
            while not aio.exit:
                try:
                    # emscripten does not honor PEEK
                    # peek = sock.sock.recv(1, socket.MSG_PEEK |socket.MSG_DONTWAIT)
                    peek = sock.sock.recv(1, socket.MSG_DONTWAIT)
                    if peek:
                        buf.append(peek)
                        if peek == b"\n":
                            print("PEEK", b"".join(buf))
                            buf.clear()
                            break
                    else:
                        # lost con.
                        print("HANGUP", buf)
                        return
                except BlockingIOError as e:
                    if e.errno == 6:
                        await aio.sleep(0)
        else:
            await aio.sleep(0)
    sock.print("QUIT")


async def main():
    global sock
    print(" ------------- Hello WasmPython + sockets ----------")

    window.MM.set_socket("wss://")

    nick = "pygamer_" + str(time.time())[-5:].replace(".", "")
    d = {"nick": nick, "channel": "#sav"}

    #async with aio.open("wss://pmp-p.ddns.net/wss/6667:443", "a+", 5) as sock:
    async with aio_sock("://pmp-p.ddns.net/wss/6667:443", "a+", 5) as sock:
        sock.print("""CAP LS\r\nNICK {nick}\r\nUSER {nick} {nick} localhost :wsocket\r\nJOIN {channel}""".format(**d))
        sock.print("PRIVMSG #sav :Salut à vous !")
        await irc_handler(sock)
    sys.exit(0)


async def custom_site():
    await main()


asyncio.run(custom_site())
del custom_site


