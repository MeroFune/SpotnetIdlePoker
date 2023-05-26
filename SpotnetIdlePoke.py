import asyncio
import time as time
import win32gui  # pip install pywin32
import win32api
import win32con

# internal state list
WAIT, NOT_IDLE, IDLE = range(3)
STATE_STRS = ["Waiting for apps", "User not idle", "User idle --- Running"]


def is_window_open(window_title):
    # Enumerate through all open windows
    def enum_windows_callback(hwnd, w_list):
        if window_title in win32gui.GetWindowText(hwnd):
            # print(f"Found window: {win32gui.GetWindowText(hwnd)}") #  for debugging
            w_list.append(win32gui.GetWindowText(hwnd))

    window_list = []

    # Enumerate through all windows and populate the window_list
    win32gui.EnumWindows(enum_windows_callback, window_list)

    return len(window_list) > 0


def get_idle_time():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


def detect_state(idle_time):
    """
    :return: Currently evaluated state, whether discord is detected, whether spotify is detected
    """
    # check each possible state in order
    # first check to see if discord and spotify are detected
    discord_detected = is_window_open("Discord")
    spotify_detected = is_window_open("Spotify")

    # if neither are detected, return wait state
    if not (discord_detected and spotify_detected):
        return WAIT, discord_detected, spotify_detected

    # if both are detected, now need to detect idle state
    if get_idle_time() > idle_time:
        return IDLE, discord_detected, spotify_detected
    else:
        return NOT_IDLE, discord_detected, spotify_detected


def send_window_message(window_title, message):
    # Enumerate through all open windows
    def enum_windows_callback(hwnd, w_list):
        if window_title in win32gui.GetWindowText(hwnd):
            win32gui.SendMessage(hwnd, message, win32con.WA_ACTIVE, 0)

    window_list = []

    # Enumerate through all windows and populate the window_list
    win32gui.EnumWindows(enum_windows_callback, window_list)


def poke_apps():
    """
    Ideas:
        - Send an activate message to spotify and discord windows
        - get current focussed window, unfocus it, then refocus it for current, spotify, and discord
    """

    # This is sufficient to work lmao
    send_window_message("Discord", win32con.WM_ACTIVATE)
    send_window_message("Spotify", win32con.WM_ACTIVATE)


def update_terminal(state, d_detected, s_detected):
    print(f"Discord detected: {d_detected}")
    print(f"Spotify detected: {s_detected}")
    print(f"Current state: {STATE_STRS[int(state)]}")
    print("\n\n")  # few new lines for readability
    ##TODO: This looks like shit. Would be nice if this looked prettier.


async def main_loop():
    # internal state variables
    state = WAIT  # wait state by default
    discord_detected = False
    spotify_detected = False

    focus_time = 40  # seconds between focus operations
    app_detection_time = 1  # seconds between re-checking for discord/ spotify presence
    idle_time = focus_time * 0.5  # seconds after which you are considered idle. by default is half of focus_time for
    # safety with detect_state()

    # main loop
    while True:
        start_time = time.monotonic()
        wait_time = focus_time  # default wait time
        state, discord_detected, spotify_detected = detect_state(idle_time)

        # evaluate based on state
        if state == WAIT:
            pass  # do nothing if waiting
            wait_time = app_detection_time
        elif state == NOT_IDLE:
            pass  # do nothing if not idle
            wait_time = focus_time
        elif state == IDLE:
            poke_apps()
            wait_time = focus_time

        update_terminal(state, discord_detected, spotify_detected)

        sleep_time = wait_time - (time.monotonic() - start_time)
        if sleep_time > 0:
            await asyncio.sleep(sleep_time)

if __name__ == '__main__':
    asyncio.run(main_loop())
