import platform
import base64
print(sys.argv)

async def to_img_file(filename, url):
    with open(filename,'wb') as out:

        if url.startswith('//') or url.startswith('http'):
            async with platform.fopen(img, "rb") as img:
                out.write(img.read())
        elif url.startswith('data:image/'):
            url = url[url.find(';base64,')+7:]
            out.write(base64.b64decode(url,validate=False))
            print("IMAGE:", filename,len(url))


async def main():
    buff = []
    code = False
    if sys.argv[-1].find('hackmd.io')<0:
        sys.argv.append('https://hackmd.io/zZTCp8XETLiX0QA30bbPUQ')

    async with platform.fopen(sys.argv[-1]+"/download", "r") as file:
        for line in file.readlines():
            if line[0]=='!' and line.find('](')>0:
                tag, img = line.rsplit('](',1)
                tag = tag.rsplit('[',1)[-1].strip()
                img = img.strip(')\n')
                await to_img_file(tag, img)
                continue
            if line.startswith('```py'):
                print('Begin')
                code = True
                continue

            if line.endswith('```\n'):
                print('End')
                code = False
                continue

            if code:
                buff.append(line)
                continue
            print(line,end="")

    with open('main.py','w') as file:
        file.write(''.join(buff))

    await shell.runpy('main.py')

    print("\n"*4, "HACKMD URL :", sys.argv[-1],"\n"*4)
    shell.interactive(prompt=True)

    while 1:
        await asyncio.sleep(0)


asyncio.run(main())

