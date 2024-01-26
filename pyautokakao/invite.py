from win32api import SendMessage
from win32gui import FindWindow, FindWindowEx, GetWindowRect
import win32con as con
from .util import open_chat_window, press_key_with_special, wait, close_chat_window, click_left_mouse


def invite(destination, friend_name:list, close_after: bool = True):
    """
    Invite friends to a chat window and send messages to them.
    
    Args:
        destination (str): The name of the chat window to open.
        friend_name (list): A list of friend names to invite to the chat.
        close_after (bool, optional): Whether to close the chat window after sending invitations. Defaults to True.
        
    Returns:
        bool: True if the invitations were sent successfully.
    """
    
    # Open the chat window
    open_chat_window(destination)
    
    # Find the main window handle and list control handle
    hwndMain = FindWindow(None, destination)
    hwndListControl = FindWindowEx(hwndMain, None, "EVA_VH_ListControl_Dblclk", None)
    
    press_key_with_special(hwndListControl, ord('I'), [con.VK_CONTROL], False)
    wait(long_enough=True)
    
    hwndkakao_edit = FindWindow('#32770', None)
    hwndkakao_edit2 = FindWindowEx( hwndkakao_edit, None, "#32770", None)
    edit = FindWindowEx( hwndkakao_edit2, None, "Edit", None)
    
    for friend in friend_name:
        SendMessage(edit, con.WM_SETTEXT, None, friend)
        wait(long_enough=True)
        
        frindlist_origin = press_key_with_special( hwndkakao_edit2, None, "EVA_VH_ListControl_Dblclk", None)
        frindlist = press_key_with_special( hwndkakao_edit2, frindlist_origin, "EVA_VH_ListControl_Dblclk", None)
        wait(long_enough=True)
        
        rect = GetWindowRect(frindlist)
        click_left_mouse(frindlist, (rect[0]+500, rect[1]+88))
        wait(long_enough=True)
    
    # Enter
    try: click_left_mouse(frindlist_origin, con.VK_RETURN)
    except: pass
    
    # Close
    if close_after: close_chat_window(hwndMain)
    
    return True