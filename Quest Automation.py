import numpy as np
import cv2
import pyautogui
import pygetwindow as gw
import glob

from skimage.metrics import structural_similarity
from time import sleep

'''
Simple Concept:
Take screenshot (every 1 second)
Check Image:
    Yes: Click on Image
    No: Click on Quest
        Check Image Q1:
            Change: Q = Q1, Click on Q
            No Change: Q = Q1 + 1, Click on Q
Recursive Loop
'''

class Automation():
    def __init__(self):
        '''
        Defind window to take screenshot,
        Image to click on,
        Location of quest
        '''
        # Target window location to take screenshot
        windows = gw.getAllTitles()
        target_window_title = 'BlueStacks App Player'
        target_window = gw.getWindowsWithTitle(target_window_title)
        target_window = target_window[0]
        self.left, self.top, self.width, self.height = target_window.left, target_window.top, \
            target_window.width, target_window.height
        
        # Search image to click on
        self.dict_image = {}
        list_files = glob.glob('./DetectionObjects/*.png')
        for index, file in enumerate(list_files):
            self.dict_image[index] = cv2.imread(file)
        self.threshold = 0.7

        # Number of click
        self.n_clicks = 1000
        self.list_quests = [(319,303), (319,422), (319,510)]
        self.list_screenshot = []
        self.previous_main = []
        self.quest_number = 0

    def take_screenshot(sel, left, top, width, height):
        # Take screenshot of window
        return np.array(pyautogui.screenshot(region = (left, top, width, height)))

    def recursive_process(self):
        # Check current screen
        screen = self.take_screenshot(self.left, self.top, self.width, self.height)
        main_quest = cv2.cvtColor(self.take_screenshot(225, 243, 531, 350), cv2.COLOR_BGR2GRAY)
        self.list_screenshot.append(screen)
        self.previous_main.append(main_quest)
        if len(self.list_screenshot) > 3:
            del self.list_screenshot[0]
        if len(self.previous_main) > 3:
            del self.previous_main[0]

        # Check image
        for key,value in self.dict_image.items():     
            similarity = cv2.matchTemplate(screen, value, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(similarity)
            bottom_right = (max_loc[0] + 190, max_loc[1] + 50)  # (Where w, h are dimensions of the template)
            print('Check image %s' %key, max_val, end = '\r')
            if max_val >= 0.60: # Check similarity & click on image
                pyautogui.click(bottom_right)
                if key == 3:
                    sleep(0.5)
                sleep(0.5)
            else: # Click on Quest
                try:
                    score, _ = structural_similarity(self.previous_main[-1], self.previous_main[-2], full = True)
                    if (score >= 0.9) & (self.quest_number <= len(self.list_quests)):
                        self.quest_number += 1
                        self.xloc, self.yloc = self.list_quests[self.quest_number]
                        pyautogui.leftClick(x = self.xloc, y = self.yloc)
                        sleep(5)
                    else:
                        # Do Main Quest
                        self.quest_number = 0
                        self.xloc, self.yloc = self.list_quests[0]
                        pyautogui.leftClick(x = self.xloc, y = self.yloc)
                        sleep(5)
                except:
                    print('Not Enough Data: Failure')
                    pass

        self.recursive_process()

if __name__ == '__main__':
     print('Running')
     initiate = Automation()
     initiate.recursive_process()