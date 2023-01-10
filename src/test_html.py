import sys, platform

js = type(platform)("js")
js.document = platform.document
sys.modules["js"] = js

def jsid(elemid):
    import js
    # Element(str(elemid)).element
    return js.document.getElementById(str(elemid))

def jsattr(query, attr):
    if isinstance(query, str):
        return js.document.getElementById(str(query)).getAttribute(attr)
    return query.getAttribute(attr)

def new(oclass, *argv):
    return getattr(oclass, "new")(*argv)

# Read data from Emscripten Filesystem
ObjectURLs = {}

def File(path):
    global ObjectURLs
    from js import window
    import pyodide.ffi

    filename = str(path)
    bloburl = ObjectURLs.get(filename, None)
    if bloburl is None:
        with open(filename, "rb") as fp:
            data_from_FS = fp.read()
        jsfile = window.File.new([pyodide.ffi.to_js(data_from_FS)], filename)
        bloburl = window.URL.createObjectURL(jsfile)
        ObjectURLs[filename] = bloburl
    return bloburl

class HTML:
    def __init__(self, file="html"):
        self.file = file
        self.buffer = []
        self.ctx = 0

    def __call__(self, *argv, **kw):
        sys.__stderr__.write(f"HTML {argv}")
        kw.setdefault("end", "\n")
        kw.setdefault("pre", "  " * self.ctx)
        for pos, arg in enumerate(argv):
            pre = ""
            suf = ""
            if not pos:
                pre
            else:
                pre = ""
            arg = arg.replace("py-click=", 'onclick="route(event)" py-click=')
            arg = arg.replace('{','{i18n.')
            o_len = len(arg)
            arg = arg.rstrip("'")
            arg = eval(f"f'''{arg}'''") + "'" * (len(arg) - o_len)
            self.buffer.append(kw["pre"] + arg + kw["end"])
        if not self.ctx:
            self.flush()

    def read(self):
        return str().join(self.buffer)

    def flush(self):
        import js

        extend = js.document.createElement("div")
        extend.innerHTML = self.read()
        jsid(self.file).appendChild(extend)
        self.buffer.clear()

    def __enter__(self):
        self.ctx += 1
        return self

    def __exit__(self, *_):
        self.ctx -= 1
        if not self.ctx:
            self.flush()


class i18n:
    world = "mundo"

def clicked(*argv):
    print("button has be clicked")

async def main():
    html = HTML()

    with html as printf:
        printf("Hello {world}")
        printf('<button name=pushme onclick=py.clicked()>Say Hello {world}</button>')
    #jsid("pushme").addEventListener("click","py.clicked")



asyncio.run(main())

