from win32api import SendMessage
from win32gui import FindWindow, FindWindowEx, GetWindowRect, GetDlgItem
import win32con as con
from .util import wait, press_key, press_key_with_special, click_left_mouse, config

def make_room(chat_name:str, friend_name:str|list):
    """
    Create a chatroom in KakaoTalk and add the specified friends to the chatroom.
    
    Args:
        chat_name (str): The name of the chatroom.
        friend_name (str|list): The name of the friend or a list of friend names to add to the chatroom.
        
    Returns:
        None
    """
    # If friend_name is a string, convert it to a list
    if isinstance(friend_name, str): friend_name = [friend_name]
    
    # Find Kakao Window
    hwndkakao = FindWindow(None, "카카오톡")
    
    # Ctrl + N
    press_key_with_special(hwndkakao, ord('N'), [con.VK_CONTROL], False)
    wait()
    
    # Find Edit
    hwndkakao_edit = FindWindow('#32770', None)
    hwndkakao_edit2 = FindWindowEx( hwndkakao_edit, None, "#32770", None)
    hwnd_find_friend_edit = FindWindowEx( hwndkakao_edit2, None, "Edit", None)
    
    # Add all friends
    for friend in friend_name:
        SendMessage(hwnd_find_friend_edit, con.WM_SETTEXT, None, friend)
        
        frindlist_origin = FindWindowEx( hwndkakao_edit2, None, "EVA_VH_ListControl_Dblclk", None)
        frindlist = FindWindowEx( hwndkakao_edit2, frindlist_origin, "EVA_VH_ListControl_Dblclk", None)
        wait(long_enough=True)
        
        rect = GetWindowRect(frindlist)
        pos = config['invite_button_position']
        click_left_mouse(frindlist, (rect[0]+pos[0], rect[1]+pos[1]))
    wait()
    
    try: press_key(frindlist_origin, con.VK_RETURN)
    except: pass
    wait(long_enough=True)
    
    # Set Chatroom Name
    hwnd_set_chatroom_name = FindWindow("EVA_Window_Dblclk", "")
    hwnd_find_friend_edit = GetDlgItem(hwnd_set_chatroom_name, 0x64)
    SendMessage(hwnd_find_friend_edit, con.WM_SETTEXT, None, chat_name)
    wait(long_enough=True)
    
    # Make Chatroom!
    rect = GetWindowRect(hwnd_set_chatroom_name)
    pos = config['make_button_position']
    click_left_mouse(hwnd_set_chatroom_name, (rect[0]+pos[0], rect[1]+pos[1]))
    
    return