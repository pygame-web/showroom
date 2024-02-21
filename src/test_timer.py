import asyncio
import pygame
from typing import Union
import uuid

# do no change import order for *thread*
# patching threading.Thread
import aio.gthread

# patched module
from threading import Thread

THREADS = {}


def patch_set_timer(event: Union[int, pygame.event.Event], millis: int, loops: int = 0):
    """Patches the pygame.time.set_timer function to use gthreads"""
    print("In patch_set_timer")
    dlay = float(millis) / 1000
    cevent = pygame.event.Event(event)
    event_loop = asyncio.get_event_loop()

    async def fire_event(thread_uuid):
        """The thread's target function to handle the timer

        Early exit conditions:
          - event loop is closed
          - event type is no longer in THREADS dictionary
          - the thread's uuid is not the latest one
          - Max loop iterations if loops param is not zero
        """
        loop_counter = 0
        while True:
            await asyncio.sleep(dlay)
            if (
                event_loop.is_closed()
                or event not in THREADS
                or THREADS[event] != thread_uuid
                or (loops and loop_counter >= loops)
            ):
                break

            pygame.event.post(cevent)
            loop_counter += 1 if loops else 0

    if dlay > 0:
        # uuid is used to track the latest thread,
        # stale threads will be terminated
        thread_uuid = uuid.uuid4()
        Thread(target=fire_event, args=[thread_uuid]).start()
        THREADS[event] = thread_uuid

    else:
        # This cancels the timer for the event
        if event in THREADS:
            del THREADS[event]


def cancel_timer_test(event, timer_event, set_timer_func, val, max_val):
    if event.type == timer_event:
        print("timer_event!")
        if val >= 0:
            val += 1
            print(f"[{timer_event}] timer_val: {val}")
        if val == max_val:
            # attempt to cancel timer
            set_timer_func(timer_event, 0)
        elif val > max_val:
            val = -1
            print("Failed to cancel timer")
    return val


async def test_cancel_original_timer(start):
    print("Test canceling original timer after 3 secs...")
    timer_event = pygame.USEREVENT
    pygame.time.set_timer(timer_event, 1000)
    timer_val = 0
    while True:
        if pygame.time.get_ticks() - start > 4000:
            break
        # event loop
        for event in pygame.event.get():
            timer_val = cancel_timer_test(
                event, timer_event, pygame.time.set_timer, timer_val, 3
            )

        await asyncio.sleep(0)
    return timer_val


async def test_cancel_patched_timer(start):
    print("Test canceling patched timer after 3 secs...")
    patched_timer_event = pygame.USEREVENT + 1
    patch_set_timer(patched_timer_event, 1000)
    patched_timer_val = 0
    while True:
        if pygame.time.get_ticks() - start > 4000:
            break
        # event loop
        for event in pygame.event.get():
            patched_timer_val = cancel_timer_test(
                event, patched_timer_event, patch_set_timer, patched_timer_val, 3
            )

        await asyncio.sleep(0)
    return patched_timer_val


async def main():
    start = pygame.time.get_ticks()
    org_timer_val = await test_cancel_original_timer(start)
    print(f"RETURN VAL: {org_timer_val}")
    assert org_timer_val == -1

    start = pygame.time.get_ticks()
    patch_timer_val = await test_cancel_patched_timer(start)
    assert patch_timer_val == 3


if __name__ == "__main__":
    asyncio.run(main())
