import time
import pyautogui

from computer_tools import ComputerTools


print("Mở Notepad sau 2 giây...")
time.sleep(2)

pyautogui.hotkey("win", "r")
time.sleep(1)

ComputerTools.type_text("notepad")
pyautogui.press("enter")

time.sleep(2)

ComputerTools.type_text(
    "Xin chào DAI! 👋\n"
    "Đây là tiếng Việt.\n"
    "你好世界！\n"
    "こんにちは！"
)

print("DONE")