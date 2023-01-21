#

"""
tested on wemos D1 mini esp8266
pip3 install esptool --user
esptool.py --chip esp8266 --port /dev/ttyUSB? erase_flash
esptool.py --chip esp8266 --port /dev/ttyUSB? --baud 1000000 write_flash --flash_size=4MB -fm dio 0 esp8266-1m-20230120-unstable-v1.19.1-831-g4f3780a15.bin


https://github.com/google/web-serial-polyfill
https://github.com/monteslu/webusb-serial


"""



import asyncio


async def main():
    print("\n"*20)
    await input("Press Enter to connect usb serial port\n\n")
    await jsiter( window.io.open_serial())
    print("connected!")

#    while True:
#        await asyncio.sleep(.5)
#        print( window.io.port.read() )
#        await asyncio.sleep(.5)
#        window.io.port.write('print("Hello World")\r\n')

    while True:
        await asyncio.sleep(0)
        data = window.io.port.read()
        if data:
            print( data )


asyncio.run(main())

