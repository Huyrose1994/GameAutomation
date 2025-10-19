from glob import glob
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
        target_window = gw.getWindowsWithTitle(target_window_title)[0]
        self.left, self.top, self.width, self.height = target_window.left, target_window.top, target_window.width, target_window.height
        
        # List all clickable images
        self.dict_image = {}
        list_files = glob('./click_photos/*.png')
        for index, file in enumerate(list_files):
            self.dict_image[index] = cv2.imread(file)

        # Threshold for template matching
        self.threshold = 0.78

        # Coordinates for quests
        self.list_quests = [
            (self.left + 100, self.top + 200), 
            (self.left + 100, self.top + 260), 
            (self.left + 100, self.top + 350)
        ]

        # Initialize click parameters
        self.n_clicks = 500
        self.i = 0

        # Main quest location
        self.xloc, self.yloc = self.list_quests[0] # Initialize quest location
        
        # Comparing screenshots
        self.list_screenshot = []
        self.previous_main = []
        self.quest_number = 0
        

    def take_screenshot(self):
        return np.array(
            pyautogui.screenshot(region = (self.left, self.top, self.width, self.height))
        )
    
    def click_on_result(self, result, template_w, template_h):
        _1, max_val, _2, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= self.threshold:
            # Calculate center of match relative to the screenshot
            relative_x = max_loc[0] + template_w // 2
            relative_y = max_loc[1] + template_h // 2
            
            # Convert to ABSOLUTE screen coordinates
            absolute_x = self.left + relative_x + 20
            absolute_y = self.top + relative_y - 10
            
            pyautogui.click(absolute_x, absolute_y)
            print(f"Clicked Skip button with confidence: {max_val:.3f}")
            return True # Indicate that a click was performed
        return False # Indicate no click was performed

    def recursive_process(self):
        print(f"--- Running cycle {self.i + 1} ---")

        # Take a screenshot
        screenshot = self.take_screenshot()
        main_quest_capture = pyautogui.screenshot(region = (self.left + 40, self.top + 170, 300, 50))
        main_quest_np = np.array(main_quest_capture)
        main_quest = cv2.cvtColor(
            main_quest_np, cv2.COLOR_BGR2GRAY
            )
        self.list_screenshot.append(screenshot)
        self.previous_main.append(main_quest)
        
        if len(self.list_screenshot) > 3:
            del self.list_screenshot[0]
        if len(self.previous_main) > 3:
            del self.previous_main[0]

        for key, value in self.dict_image.items():
            similarity = cv2.matchTemplate(screenshot, value, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(similarity)
            print('Check image %s' %key, max_val, end = '\r')
            bottom_right = (max_loc[0], max_loc[1])
            result = cv2.matchTemplate(screenshot, value, cv2.TM_CCOEFF_NORMED)
            if max_val >= 0.60: 
                self.click_on_result(result, value.shape[1], value.shape[0])
                sleep(0.5)
                    
        pyautogui.click(self.xloc, self.yloc)
        sleep(5)
        self.recursive_process()

if __name__ == '__main__':
     print('Running')
     initiate = Automation()
     initiate.recursive_process()
