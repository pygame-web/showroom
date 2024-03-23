import asyncio
import js

async def main():
    import platform
    platform.window.debug(1)


    espeak = await dlopen("espeak")
    engine = await dlopen("enginesound")

    async def soundmgr():
        await asyncio.sleep(.6)
        await espeak.say("Gentleman : start your engine !")
        await asyncio.sleep(2)
        await engine.start()

    aio.loop.create_task(soundmgr())

    await asyncio.sleep(10)
    print("cut engine")
    await engine.stop()



asyncio.run(main())

