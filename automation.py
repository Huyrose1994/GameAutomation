import numpy as np
import cv2
import pyautogui
import pygetwindow as gw

from time import sleep

class Automation():
    def __init__(self):
        # Target window location

        windows = gw.getAllTitles()
        target_window_title = 'BlueStacks App Player'
        target_window = gw.getWindowsWithTitle(target_window_title)
        target_window = target_window[0]
        self.left, self.top, self.width, self.height = target_window.left, target_window.top, target_window.width, target_window.height
        self.image_1 = cv2.imread('./DetectionObjects/Skip(1).png')
        self.image_2 = cv2.imread('./DetectionObjects/Skip(2).png')
        self.threshold = 0.7
        self.n_clicks = 500
        self.quest_1 = (173,486)
        self.quest_2 = (174,548)
        self.quest_3 = (169,619)
        self.xloc, self.yloc = self.quest_1
    def take_screenshot(self):
        return np.array(pyautogui.screenshot(region = (self.left, self.top, self.width, self.height)))
    
    def click_on_result(self, result):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= self.threshold:
            x, y = max_loc
            # Click on the matched location (x, y)
            pyautogui.click(x, y)
            sleep(5)
            click_on_result()

    def Skips(self):
        screenshot = self.take_screenshot()
        result_1 = cv2.matchTemplate(screenshot, self.image_1, cv2.TM_CCOEFF_NORMED)
        result_2 = cv2.matchTemplate(screenshot, self.image_2, cv2.TM_CCOEFF_NORMED)
        pyautogui.leftClick(x = self.xloc, y = self.yloc)
        print('Click Quest', end = '\r')
        self.click_on_result(result_1)
        self.click_on_result(result_2)     
        sleep(5)
        self.Skips()

if __name__ == '__main__':
     print('Running')
     initiate = Automation()
     initiate.Skips()
