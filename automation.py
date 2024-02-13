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
            print(cv2.imread(file))
        self.threshold = 0.7

        # Number of click
        self.n_clicks = 1000
        self.list_quests = [(319,303)]
        self.list_screenshot = []
        self.previous_main = []
        self.i = 0

    def take_screenshot(sel, left, top, width, height):
        # Take screenshot of window
        return np.array(pyautogui.screenshot(region = (left, top, width, height)))

    def recursive_process(self):
        # Check current screen
        screen = self.take_screenshot(self.left, self.top, self.width, self.height)
        main_quest = self.take_screenshot(225, 243, 531, 350)
        self.list_screenshot.append(screen)
        self.previous_main.append(main_quest)
        if len(self.list_screenshot) > 3:
            del self.list_screenshot[0]
        if len(self.previous_main) > 3:
            del self.previous_main[0]
        print(len(self.previous_main))

        # Check image
        for key,value in self.dict_image.items():     
            similarity = cv2.matchTemplate(screen, value, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(similarity)
            bottom_right = (max_loc[0] + 180, max_loc[1] + 50)  # (Where w, h are dimensions of the template)
        
            if max_val >= 0.95: # Check similarity & click on image
                pyautogui.click(bottom_right)
                sleep(0.5)
            else: # Click on Quest
                try:
                    score, _ = structural_similarity(self.previous_main[-1], self.previous_main[-2], full = True)
                    print(score)
                except:
                    print('Failure')
                    # try:
                    #     print(self.previous_main[-1])
                    #     print(self.previous_main[-2])
                    # except:
                    pass
                self.xloc, self.yloc = self.list_quests[-self.i]
                pyautogui.leftClick(x = self.xloc, y = self.yloc)
                sleep(5)
            self.recursive_process()



    # def skip_quest(self):
    #     '''
    #     Check if the screen doesn't change that much after 3 seconds
    #     '''

    #     # Click second quest if first quest doesn't move
    #     screenshot = self.take_screenshot()
    #     self.list_screenshot.append(screenshot)
    #     __corr = cv2.matchTemplate(screenshot, self.list_screenshot[-1], cv2.TM_CCOEFF_NORMED)
    #     # Do multiple quests
    #     if __corr > 0.999:
    #         self.i += 1
    #         self.xloc, self.yloc = self.list_quests[-self.i]
    #         print(self.i)
        
    #     # Only do the first quest
    #     self.xloc, self.yloc = self.list_quests[0]
    #     result_1 = cv2.matchTemplate(screenshot, self.image_1, cv2.TM_CCOEFF_NORMED)
    #     result_2 = cv2.matchTemplate(screenshot, self.image_2, cv2.TM_CCOEFF_NORMED)

    #     pyautogui.leftClick(x = self.xloc, y = self.yloc)
    #     print('Click Quest', end = '\r')
    #     self.click_on_result(result_1)
    #     self.click_on_result(result_2)     
    #     sleep(5)
    #     self.skip_quest()
    
    # def start(self):
    #     while self.i < self.n_clicks:
    #         pyautogui.leftClick(x = self.xloc, y = self.yloc)



if __name__ == '__main__':
     print('Running')
     initiate = Automation()
     initiate.recursive_process()
