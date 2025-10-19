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
        
        # Load templates and get their dimensions
        self.image_1 = cv2.imread('./click_photos/Skip(1).png')
        self.w1, self.h1, _ = self.image_1.shape[::-1] # Template width and height
        
        self.image_2 = cv2.imread('./click_photos/Skip(2).png')
        self.w2, self.h2, _ = self.image_2.shape[::-1]
        
        self.threshold = 0.7
        self.list_quests = [
            (self.left + 100, self.top + 200), 
            (self.left + 100, self.top + 260), 
            (self.left + 100, self.top + 350)
        ] # Store ABSOLUTE coordinates for quests
        self.n_clicks = 500
        self.i = 0
        self.xloc, self.yloc = self.list_quests[0] # Initialize quest location
        

    def take_screenshot(self):
        return np.array(pyautogui.screenshot(region = (self.left, self.top, self.width, self.height)))
    
    def click_on_result(self, result, template_w, template_h):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= self.threshold:
            # Calculate center of match relative to the screenshot
            relative_x = max_loc[0] + template_w // 2
            relative_y = max_loc[1] + template_h // 2
            
            # Convert to ABSOLUTE screen coordinates
            absolute_x = self.left + relative_x
            absolute_y = self.top + relative_y
            
            pyautogui.click(absolute_x, absolute_y)
            print(f"Clicked Skip button with confidence: {max_val:.3f}")
            sleep(5)
            return True # Indicate that a click was performed
        return False # Indicate no click was performed

    def Skips(self):
        while self.i < self.n_clicks:
            print(f"--- Running cycle {self.i + 1} ---")
            
            # 1. Update Quest Target Location
            self.xloc, self.yloc = self.list_quests[self.i % len(self.list_quests)] 

            # 2. Click the Quest button (using ABSOLUTE stored coordinates)
            pyautogui.leftClick(x=self.xloc, y=self.yloc)
            print(f'Clicking Quest at ({self.xloc}, {self.yloc})')
            sleep(2) # Wait for the next screen to load

            # 3. Take Screenshot of the game window
            screenshot = self.take_screenshot()

            # 4. Check for Skip buttons
            result_1 = cv2.matchTemplate(screenshot, self.image_1, cv2.TM_CCOEFF_NORMED)
            clicked = self.click_on_result(result_1, self.w1, self.h1)

            if not clicked:
                # If image_1 was not found, try image_2
                result_2 = cv2.matchTemplate(screenshot, self.image_2, cv2.TM_CCOEFF_NORMED)
                self.click_on_result(result_2, self.w2, self.h2)
            
            # Increment and wait for next cycle
            self.i += 1
            sleep(5) # Delay before starting the next quest cycle

if __name__ == '__main__':
     print('Running')
     initiate = Automation()
     initiate.Skips()
