import ctypes
from time import sleep
from win32api import PostMessage, GetCurrentThreadId, MAKELONG, SendMessage
from win32gui import FindWindow, FindWindowEx, IsWindow, ScreenToClient
import win32con as con

config = {
    "long_delay": 1,
    "short_delay": 0.5
}

PBYTE256 = ctypes.c_ubyte * 256
_user32 = ctypes.WinDLL("user32")
GetKeyboardState = _user32.GetKeyboardState
SetKeyboardState = _user32.SetKeyboardState
GetWindowThreadProcessId = _user32.GetWindowThreadProcessId
AttachThreadInput = _user32.AttachThreadInput
MapVirtualKeyA = _user32.MapVirtualKeyA
MapVirtualKeyW = _user32.MapVirtualKeyW

def wait(long_enough:bool=False) -> None:
    if long_enough:
        sleep(config["long_delay"])
        return
    
    sleep(config["short_delay"])
    return


def press_key(HandlingWindow, key, sec:float=0.01):
    """
    Simulates a key press in the specified window.

    Args:
        HandlingWindow: The window to send the key press to.
        key: The key to be pressed.
        sec (float): The duration to hold the key down, in seconds (default is 0.01).
    """
    
    PostMessage(HandlingWindow, con.WM_KEYDOWN, key, 0)
    sleep(sec)
    PostMessage(HandlingWindow, con.WM_KEYUP, key, 0)


def press_key_with_special(hwnd, key, shift, specialkey):
    """
    Press key with special keys

    Args:
        hwnd: Handle to the window to receive the keystroke.
        key: Virtual-key code of the key to be pressed.
        shift: List of modifier keys to be pressed along with the main key.
        specialkey: Boolean indicating if the key is a special key.
    Returns:
        None
    """
    if IsWindow(hwnd):

        ThreadId = GetWindowThreadProcessId(hwnd, None)

        lparam = MAKELONG(0, MapVirtualKeyA(key, 0))
        msg_down = con.WM_KEYDOWN
        msg_up = con.WM_KEYUP

        if specialkey:
            lparam = lparam | 0x1000000

        if len(shift) > 0:
            pKeyBuffers = PBYTE256()
            pKeyBuffers_old = PBYTE256()

            SendMessage(hwnd, con.WM_ACTIVATE, con.WA_ACTIVE, 0)
            AttachThreadInput(GetCurrentThreadId(), ThreadId, True)
            GetKeyboardState(ctypes.byref(pKeyBuffers_old))

            for modkey in shift:
                if modkey == con.VK_MENU:
                    lparam = lparam | 0x20000000
                    msg_down = con.WM_SYSKEYDOWN
                    msg_up = con.WM_SYSKEYUP
                pKeyBuffers[modkey] |= 128

            SetKeyboardState(ctypes.byref(pKeyBuffers))
            sleep(0.01)
            PostMessage(hwnd, msg_down, key, lparam)
            sleep(0.01)
            PostMessage(hwnd, msg_up, key, lparam | 0xC0000000)
            sleep(0.01)
            SetKeyboardState(ctypes.byref(pKeyBuffers_old))
            sleep(0.01)
            AttachThreadInput(GetCurrentThreadId(), ThreadId, False)

        else:
            SendMessage(hwnd, msg_down, key, lparam)
            SendMessage(hwnd, msg_up, key, lparam | 0xC0000000)


def open_chat_window(destination:str):
    """
    Search and open the window based on the given destination.
    """
    
    # Get hwndFindEdit
    hwndkakao = FindWindow(None, "카카오톡")
    press_key_with_special(hwndkakao, ord('F'), [con.VK_CONTROL], False) # For initialize

    hwndkakao_edit1 = FindWindowEx( hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = FindWindowEx( hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit2_2 = FindWindowEx( hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
    hwndFindEdit = FindWindowEx( hwndkakao_edit2_2, None, "Edit", None)

    # Search chat room
    SendMessage(hwndFindEdit, con.WM_SETTEXT, 0, destination)
    wait(long_enough=True)
    
    # Open
    press_key(hwndFindEdit, con.VK_RETURN)
    SendMessage(hwndFindEdit, con.WM_SETTEXT, 0, "") # Blank hwndFindEdit input

def close_chat_window(hwnd):
    #try: press_key(hwnd, con.VK_ESCAPE)
    try: PostMessage(hwnd, con.WM_CLOSE, 0, 0)
    except: pass

# https://github.com/neal365/python/blob/master/mouseClick.py
def click_left_mouse(handle, pos):
    """
    Perform a left click action at the specified position on the given handle.
    Args:
        handle: The handle of the target window.
        pos: The position where the left click action will be performed.
    Returns:
        None
    """
    
    client_pos = ScreenToClient(handle, pos)
    tmp = MAKELONG(client_pos[0], client_pos[1])
    
    SendMessage(handle, con.WM_ACTIVATE, con.WA_ACTIVE, 0)
    SendMessage(handle, con.WM_LBUTTONDOWN, con.MK_LBUTTON, tmp) 
    SendMessage(handle, con.WM_LBUTTONUP, con.MK_LBUTTON, tmp)


if __name__ == "__main__":
    pass