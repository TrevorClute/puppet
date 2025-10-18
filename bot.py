import pyautogui
import os
from pyvirtualdisplay.display import Display
import Xlib.display
import time


disp = Display(visible=True, size=(1920, 1080), backend="xvfb", use_xauth=True)
disp.start()

pyautogui._pyautogui_x11._display = Xlib.display.Display(':1')

time.sleep(5)

screen_width, screen_height = pyautogui.size()
print(screen_width, screen_height)

cursor_x, cursor_y = pyautogui.position()
print(cursor_x, cursor_y)

time.sleep(5)
pyautogui.moveTo(20, 5)
pyautogui.click()

time.sleep(10)

pyautogui.moveTo(screen_width * 0.5, screen_height * 0.1)
pyautogui.write("http://127.0.0.1:5000", interval=0.01)
pyautogui.press('enter')



print(cursor_x, cursor_y)
screenshot = pyautogui.screenshot()
screenshot.save("image.png")
