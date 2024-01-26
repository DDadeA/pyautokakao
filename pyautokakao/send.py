from win32api import SendMessage
from win32gui import FindWindow, FindWindowEx
import win32con as con
from .util import open_chat_window, press_key, wait, close_chat_window

def send(destination:str, message:str, close_after:bool=True):
    """
    Send a message to a destination chat window.

    Args:
        destination (str): The name of the destination chat window
        message (str): The message to be sent
        close_after (bool, optional): Whether to close the chat window after sending the message. Defaults to True.

    Returns:
        None
    """
    
    # Open the windows
    open_chat_window(destination)
    wait(long_enough=True)
    
    # Get chat room handle
    main = FindWindow(None, destination)
    hwndEdit = FindWindowEx(main, None, "RICHEDIT50W", None)
    
    # Send message
    SendMessage(hwndEdit, con.WM_SETTEXT, 0, message)
    press_key(hwndEdit, con.VK_RETURN)
    wait()
    
    # Close
    if close_after: close_chat_window(main)
    
    return