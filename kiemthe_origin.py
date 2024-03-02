import numpy as np
import cv2
import pyautogui
import PIL
from Xlib import X, display

from ewmh import EWMH
import re

def find_window_position(window_name_pattern):
    # Create an EWMH object
    ewmh = EWMH()

    # Get all windows
    windows = ewmh.getClientList()
    # Test
    window = windows[5]
    name = ewmh.getWmName(window)
    geometry = window.get_geometry()
    print(f"Window '{name}' Position and Size: {geometry.x}, {geometry.y}, {geometry.width}x{geometry.height}")

#     # Compile the window name pattern
#     pattern = re.compile(window_name_pattern)

#     for win in windows:
#         # Get window name
#         name = ewmh.getWmName(win)
#         if name and pattern.search(name):
#             # If window name matches the pattern, get its geometry
#             geometry = win.get_geometry()
#             print(f"Window '{name}' Position and Size: {geometry.x}, {geometry.y}, {geometry.width}x{geometry.height}")
#             return geometry.x, geometry.y, geometry.width, geometry.height

#     print("Window not found.")
#     return None

# Example usage
window_name_pattern = "Genymotion Player"
find_window_position(window_name_pattern)