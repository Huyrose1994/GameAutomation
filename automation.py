from glob import glob
import numpy as np
import cv2
import pyautogui
import pygetwindow as gw
import keyboard
import logging
import sys

from time import sleep

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')

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
            (self.left + 100, self.top + 320)
        ]

        # Initialize click parameters
        self.i = 0

        # Comparing screenshots
        self.list_screenshot = []
        self.previous_main = []
        self.quest_number = 0
        self.stop = False

    def stop_execution(self):
        logging.info("Stopping execution...")
        self.stop = True

    def setup_key_listener(self, key_to_use = 'esc'):
        logging.info(f"Press '{key_to_use}' to stop the automation.")
        keyboard.add_hotkey(key_to_use, self.stop_execution)

    def clean_up(self):
        keyboard.remove_all_hotkeys()
        logging.info("Cleaned up key listeners.")

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
            logging.info(f"Clicked Skip button with confidence: {max_val:.3f}")
            return True
        return False

    def recursive_process(self):
        if self.stop:
            logging.info("Automation stopped by user.")
            return
        logging.info(f"--- Running cycle {self.i + 1} ---")

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

        temp_similarity = 1
        while temp_similarity > 0.65:
            for key, skip_photos in self.dict_image.items():
                similarity = cv2.matchTemplate(self.take_screenshot(), skip_photos, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(similarity)
                logging.info('Check image %s: %s' % (key, max_val))
                result = cv2.matchTemplate(self.take_screenshot(), skip_photos, cv2.TM_CCOEFF_NORMED)
                if max_val >= 0.60: 
                    self.click_on_result(result, skip_photos.shape[1], skip_photos.shape[0])
                    sleep(1)
                temp_similarity = max_val

        # If the screen is the same, move to the next quest
        if len(self.previous_main) == 3:
            similarity_1 = cv2.matchTemplate(
                self.previous_main[0], self.previous_main[1], cv2.TM_CCOEFF_NORMED
                )
            similarity_2 = cv2.matchTemplate(
                self.previous_main[1], self.previous_main[2], cv2.TM_CCOEFF_NORMED
                )
            _, max_val_1, _, _ = cv2.minMaxLoc(similarity_1)
            _, max_val_2, _, _ = cv2.minMaxLoc(similarity_2)
            logging.info(f'Similarity check: {max_val_1:.3f}, {max_val_2:.3f}')
            if max_val_1 > 0.65 and max_val_2 > 0.65:
                self.quest_number += 1
                if self.quest_number >= len(self.list_quests):
                    self.quest_number = 0
                    logging.info('All quests completed.')
                    pyautogui.press('tab')
                    return
                logging.info(f'Moving to quest {self.quest_number + 1}')
                self.xloc, self.yloc = self.list_quests[self.quest_number]
                pyautogui.click(self.xloc, self.yloc)
                sleep(5)
                self.previous_main = []

        self.i += 1
        self.recursive_process()


if __name__ == '__main__':
     logging.info('Running')
     initiate = Automation()
     initiate.setup_key_listener('esc')
     initiate.recursive_process()
     initiate.clean_up()