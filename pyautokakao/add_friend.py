from win32api import SendMessage
from win32gui import FindWindow, FindWindowEx
import win32con as con
from .util import wait, press_key, press_key_with_special

def add_friend(friend_name:str, phone_number:str):
    """
    Adds a friend on KakaoTalk using the specified friend name and phone number.
    
    Args:
        friend_name (str): The name of the friend to be added.
        phone_number (str): The phone number of the friend to be added.
    
    Returns:
        None
    """
    
    # Find the main window handle
    hwndkakao = FindWindow(None, "카카오톡")
    
    # Open friend add window
    press_key_with_special(hwndkakao, ord('A'), [con.VK_CONTROL], False)
    wait()
    
    # Find friend add edit
    hwndkakao_edit = FindWindow('#32770', None)
    hwndkakao_edit2_1 = FindWindowEx( hwndkakao_edit, None, "#32770", None)
    hwndkakao_edit2_2 = FindWindowEx( hwndkakao_edit, hwndkakao_edit2_1, "#32770", None)
    hwnd_friend_name_edit = FindWindowEx( hwndkakao_edit2_2, None, "Edit", None)
    hwnd_phone_number_edit = FindWindowEx( hwndkakao_edit2_2, hwnd_friend_name_edit, "Edit", None)
    wait()
    
    # Input friend name and phone number
    SendMessage(hwnd_friend_name_edit, con.WM_SETTEXT, None, friend_name)
    SendMessage(hwnd_phone_number_edit, con.WM_SETTEXT, None, phone_number)
    press_key(hwndkakao_edit2_2, con.VK_RETURN)
    wait()
    
    press_key(hwndkakao_edit2_2, con.VK_RETURN)
    
    return