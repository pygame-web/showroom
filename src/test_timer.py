import asyncio
import pygame
from typing import Union
import uuid

pygame.init()

# do no change import order for *thread*
# patching threading.Thread
import aio.gthread

# patched module
from threading import Thread

# Global var to keep track of timer threads
#   - key: event type
#   - value: thread uuid
THREADS = {}


def patch_set_timer(event: Union[int, pygame.event.Event], millis: int, loops: int = 0):
    """repeatedly create an event on the event queue

    Patches the pygame.time.set_timer function to use gthreads
    """
    dlay = float(millis) / 1000
    if isinstance(event, pygame.event.Event):
        event_type = event.type
        cevent = event
    else:
        event_type = int(event)
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
                or event_type not in THREADS
                or THREADS[event_type] != thread_uuid
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
        THREADS[event_type] = thread_uuid

    else:
        # This cancels the timer for the event
        if event in THREADS:
            del THREADS[event_type]


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
    pygame.event.set_blocked(timer_event)
    pygame.event.clear()
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
    pygame.event.set_blocked(patched_timer_event)
    pygame.event.clear()
    return patched_timer_val


async def test_repeated_original_timer(start):
    print("Test repeating original timer after 10 secs...")
    timer_event = pygame.USEREVENT + 2
    pygame.time.set_timer(timer_event, 1000)
    timer_val = 0
    while True:
        if pygame.time.get_ticks() - start > 10_000:
            break
        # event loop
        for event in pygame.event.get():
            if event.type == timer_event:
                timer_val += 1
                if timer_val == 2:
                    pygame.time.set_timer(timer_event, 2000)
                print(timer_val)

        await asyncio.sleep(0)
    pygame.event.set_blocked(timer_event)
    pygame.event.clear()
    return timer_val


async def test_repeated_patched_timer(start):
    print("Test repeating patched timer after 10 secs...")
    timer_event = pygame.USEREVENT + 3
    patch_set_timer(timer_event, 1000)
    timer_val = 0
    while True:
        if pygame.time.get_ticks() - start > 10_000:
            break
        # event loop
        for event in pygame.event.get():
            if event.type == timer_event:
                timer_val += 1
                if timer_val == 2:
                    patch_set_timer(timer_event, 2000)
                print(timer_val)

        await asyncio.sleep(0)
    pygame.event.set_blocked(timer_event)
    pygame.event.clear()
    return timer_val


async def test_fixed_iterations_patched_timer(start, num_iter):
    print(f"Test looping timer {num_iter} times")
    timer_event = pygame.USEREVENT + 4
    patch_set_timer(timer_event, 1000, num_iter)
    timer_val = 0
    while True:
        if pygame.time.get_ticks() - start > 4000:
            break
        # event loop
        for event in pygame.event.get():
            if event.type == timer_event:
                timer_val += 1
                print(timer_val)

        await asyncio.sleep(0)
    pygame.event.set_blocked(timer_event)
    pygame.event.clear()
    return timer_val


async def test_event_object_param_patched_timer(start, num_iter):
    print(f"Test looping timer {num_iter} times using event object")
    timer_event = pygame.USEREVENT + 5
    timer_event_obj = pygame.event.Event(timer_event)
    patch_set_timer(timer_event_obj, 1000, num_iter)
    timer_val = 0
    while True:
        if pygame.time.get_ticks() - start > 4000:
            break
        # event loop
        for event in pygame.event.get():
            if event.type == timer_event:
                timer_val += 1
                print(timer_val)

        await asyncio.sleep(0)
    pygame.event.set_blocked(timer_event)
    pygame.event.clear()
    return timer_val


async def main():
    print("===== CANCEL TEST 1: Original vs Patched Timer =====")
    # Original timer creates multiple duplicate timers with delay of 0
    start = pygame.time.get_ticks()
    org_timer_val = await test_cancel_original_timer(start)
    assert org_timer_val == -1
    print("===> TEST CASE 1 Complete")

    # Patched timer cancels the timer correctly
    start = pygame.time.get_ticks()
    patch_timer_val = await test_cancel_patched_timer(start)
    assert patch_timer_val == 3
    print("===> TEST CASE 2 Complete")

    print("===== REPEAT TEST 2: Original vs Patched Timer =====")
    # Original timer will create a duplicate timer instead of
    # canceling the current one
    start = pygame.time.get_ticks()
    org_timer_val = await test_repeated_original_timer(start)
    assert org_timer_val > 10
    print("===> TEST CASE 3 Complete")

    # Patched timer replaces the existing one
    start = pygame.time.get_ticks()
    patch_timer_val = await test_repeated_patched_timer(start)
    assert patch_timer_val < 10
    print("===> TEST CASE 4 Complete")

    # The following tests are for the patched timer only
    print("===== FIXED ITERATION TEST 3: Patched Timer =====")
    start = pygame.time.get_ticks()
    patch_timer_val = await test_fixed_iterations_patched_timer(start, 3)
    assert patch_timer_val == 3
    print("===> TEST CASE 5 Complete")

    print("===== EVENT OBJ PARM TEST 4: Patched Timer =====")
    start = pygame.time.get_ticks()
    patch_timer_val = await test_event_object_param_patched_timer(start, 3)
    assert patch_timer_val == 3
    print("===> TEST CASE 6 Complete")

    print("ALL DONE!")


if __name__ == "__main__":
    asyncio.run(main())
