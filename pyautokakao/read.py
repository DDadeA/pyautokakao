import win32con as con
from win32gui import FindWindow, FindWindowEx
from .util import open_chat_window, press_key_with_special, press_key, wait, close_chat_window
from pywinauto import clipboard
from os import listdir


def read(destination: str, close_after: bool = True, use_clipboard: bool = True, saving_path: str = "data") -> str:
    """
    Get the chat log from the specified destination.

    Args:
        destination (str): The destination chat window.
        close_after (bool, optional): Whether to close the chat window after reading. Defaults to True.
        use_clipboard (bool, optional): Whether to use the clipboard to retrieve the chat log. If not, it will use log saving method(slow). Defaults to True.
        saving_path (str, optional): The path to save the chat log. It needs for use_clipboard=False. Defaults to "data".

    Returns:
        str: The chat log.
    """

    # Open the chat window
    open_chat_window(destination)

    # Find the main window handle and list control handle
    hwndMain = FindWindow(None, destination)
    hwndListControl = FindWindowEx(hwndMain, None, "EVA_VH_ListControl_Dblclk", None)

    # Wait for the window to be ready
    wait(long_enough=True)

    if use_clipboard:
        # Select all text in the chat history and copy to clipboard
        press_key_with_special(hwndListControl, ord('A'), [con.VK_CONTROL], False)
        press_key_with_special(hwndListControl, ord('C'), [con.VK_CONTROL], False)
        
        # Retrieve text from clipboard
        chat_log = clipboard.GetData()

    elif not use_clipboard:
        # Save the chat history
        press_key_with_special(hwndListControl, ord('S'), [con.VK_CONTROL], False)
        wait(long_enough=True)
        
        press_key(hwndListControl, con.VK_RETURN)
        wait(long_enough=True)
        
        hwndAlert = FindWindowEx(None, None, "EVA_Window_Dblclk", None)
        press_key(hwndAlert, con.VK_RETURN)
        wait(long_enough=True)
        
        # Get Recent File
        files = listdir(saving_path)
        with open(f'{saving_path}/{files[-1]}', 'r', encoding='utf8') as f:
            chat_log = f.read()
    
    # Close the chat window
    if close_after: close_chat_window(hwndMain)
    
    return chat_log