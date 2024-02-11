# /// script
# dependencies = [
#  "plyer",
# ]
# ///


import asyncio
import plyer

def goto_xy(x, y):
    CSI(f"{y};{x}H")


async def main():
    CSI("2J")
    accelerometer = plyer.accelerometer
    accelerometer.enable()
    while True:
        goto_xy(10,10)
        print(accelerometer.get_acceleration())
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())

