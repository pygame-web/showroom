import asyncio
import pygame

from pygame._sdl2.audio import (
    get_audio_device_names,
    AudioDevice,
    AUDIO_F32,
    AUDIO_ALLOW_FORMAT_CHANGE,
)
from pygame._sdl2.mixer import set_post_mix


pygame.mixer.pre_init(44100, 32, 2, 512)
pygame.init()

async def main():

    # init_subsystem(INIT_AUDIO)
    screen = pygame.display.set_mode([320,200])
    print("\n"*10)

    names = get_audio_device_names(True)
    print(names)

    sounds = []
    sound_chunks = []


    def callback(audiodevice, audiomemoryview):
        """This is called in the sound thread.
        Note, that the frequency and such you request may not be what you get.
        """
        # print(type(audiomemoryview), len(audiomemoryview))
        # print(audiodevice)
        sound_chunks.append(bytes(audiomemoryview))


    def postmix_callback(postmix, audiomemoryview):
        """This is called in the sound thread.
        At the end of mixing we get this data.
        """
        #print(type(audiomemoryview), len(audiomemoryview))
        #print(postmix)
        ...



    set_post_mix(postmix_callback)

    audio = AudioDevice(
        devicename=names[0],
        iscapture=True,
        frequency=44100,
        audioformat=AUDIO_F32,
        numchannels=2,
        chunksize=512,
        allowed_changes=AUDIO_ALLOW_FORMAT_CHANGE,
        callback=callback,
    )

    await asyncio.sleep(0)

    # start recording.
    audio.pause(0)

    print(audio)

    print(f"recording with '{names[0]}'")
    await asyncio.sleep(5)

    audio.pause(0)


    print(f"Turning data {len(sound_chunks)=} into a pygame.mixer.Sound")
    sound = pygame.mixer.Sound(buffer=b"".join(sound_chunks))

    print("playing back recorded sound")
    sound.play()

    await asyncio.sleep(10)
    print("done")

    pygame.quit()

asyncio.run(main())

