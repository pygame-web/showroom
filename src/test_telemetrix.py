"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import asyncio
import sys
import time

from telemetrix_aio import telemetrix_aio

"""
Setup a pin for digital output and output a signal
and toggle the pin. Do this 4 times.
"""

# some globals
DIGITAL_PIN = 2  # arduino pin number



async def the_callback(data):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
    print(f'Motor {data[1]} absolute motion completed at: {date}.')


async def running_callback(data):
    if data[1]:
        print('The motor is running.')
    else:
        print('The motor IS NOT running.')

async def step_absolute(board):

    # create an accelstepper instance for a TB6600 motor driver
    #motor = await board.set_pin_mode_stepper(interface=2, pin1=8, pin2=9)

    # if you are using a 28BYJ-48 Stepper Motor with ULN2003
    # comment out the line above and uncomment out the line below.
    motor = await board.set_pin_mode_stepper(interface=4, pin1=16, pin2=5, pin3=4, pin4=0)

    await board.stepper_is_running(motor, callback=running_callback)
    await asyncio.sleep(.2)

    # set the max speed and acceleration
    await board.stepper_set_max_speed(motor, 100)
    await board.stepper_set_acceleration(motor, 400)

    # set the absolute position in steps


    # run the motor

    for way in (1,-1,1,-1,1,-1):
        print('Starting motor...')
        await board.stepper_move_to(motor, way * 50)
        await board.stepper_run(motor, completion_callback=the_callback)
        await asyncio.sleep(.2)
        await board.stepper_is_running(motor, callback=running_callback)
        await asyncio.sleep(3)
        await board.stepper_stop(motor)
        await asyncio.sleep(2)


async def blink(board, pin):
    """
    This function will to toggle a digital pin.

    :param board: a telemetrix_aio instance
    :param pin: pin to be controlled
    """

    # set the pin mode
    await board.set_pin_mode_digital_output(pin)

    # toggle the pin 4 times and exit
    for x in range(2):
        print('ON')
        await board.digital_write(pin, 0)
        await asyncio.sleep(.5)
        print('OFF')
        await board.digital_write(pin, 1)
        await asyncio.sleep(.5)


# get the event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# instantiate telemetrix_aio

if sys.argv[-1].find('192.') <0:
    ip_addr = '192.168.0.1'
else:
    ip_addr = sys.argv[-1]


async def main():
    global ip_addr
    if sys.platform in ('emscripten',):
        window.MM.set_socket("ws://")
        print(f"Board (Web)socket : {ip_addr}:31335")
    else:
        print(f"Board socket : {ip_addr}:31335")

    board = telemetrix_aio.TelemetrixAIO(ip_address=ip_addr, autostart=False)

    await board.start_aio()

    await blink(board, DIGITAL_PIN)
    await step_absolute(board)

asyncio.run( main() )

