from threading import Thread, Event, Timer
import keyboard
from functools import partial

from config import config


def print_status(io, monitor_view):
    """Show commands status until user hit the keyboard."""

    # Flag turned on when user hit the keyboard
    kbhit_event = Event()

    # Initialize listener for keyboard hit
    keypress_callback = partial(handle_keypress, kbhit_event)
    keyboard.on_press(keypress_callback, True)

    # Print table with interval
    print_thread = Thread(target=print_status_by_interval, args=[io, monitor_view, kbhit_event])
    print_thread.start()

    # Stay in function until user hit the keyboard
    while not kbhit_event.is_set():
        pass
    return


def print_status_by_interval(io, monitor_view, event):
    t = Timer(int(config['FUNCTIONAL']['REFRESH_INTERVALS_SEC']), print_status_by_interval, [io, monitor_view, event])
    if event.is_set():
        return
    io.clear()
    monitor_view.show()
    t.start()


def handle_keypress(flag_event, _):
    keyboard.unhook_all()
    flag_event.set()
