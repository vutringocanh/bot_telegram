import time
import pyautogui

from computer_tools import ComputerTools


print("=== DAI COMPUTER TOOLS TEST ===")

print("Screen:", ComputerTools.screen_size())

print("Mouse:", ComputerTools.mouse_position())

print("Di chuyển chuột sau 3 giây...")

time.sleep(3)

size = ComputerTools.screen_size()

ComputerTools.move_mouse(
    size["width"] // 2,
    size["height"] // 2,
)

print("Mouse:", ComputerTools.mouse_position())

print("Click sau 2 giây...")

time.sleep(2)

ComputerTools.click()

print("DONE")