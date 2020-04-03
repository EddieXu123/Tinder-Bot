from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from secrets import phone_num
import pytesseract
from PIL import Image
import pyscreenshot as ImageGrab
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller

# Global variable to control our keyboard
keyboard = Controller()


def screen_shot():
    # coordinate of message notification gotten by sending dozens of messages to phone
    # and then using a notepad to mark where the key is on my screen. Then, trial and error to
    # pinpoint where the code is on my screen to extract to text using OCR
    image = ImageGrab.grab(bbox=(2240, 140, 2565, 210))
    image.save('code4.png')

    # Using our OCR
    im = Image.open('code4.png')
    text = pytesseract.image_to_string(im, lang="eng")
    print(text)

    write_file = open("output1.txt", "w")
    write_file.write(text)
    write_file.close()

    # Extracting the code from the screen shot
    screen = open("output1.txt", "r")
    output = screen.readline()
    output2 = output.split()
    code = output2[4]
    return code


class TinderBot:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def log_on(self):
        # Log onto Tinder
        self.driver.get('https://tinder.com')

        # Wait for the login screen to popup
        sleep(5)

        # Close Cookies popup on web page
        close_stalker = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/button')
        close_stalker.click()

        # Tinder changes the welcome page so that the phone log in option is in a different path (1, 2, 3) each time
        # First try to log in by phone in first path:
        try:
            log_in_by_text = self.driver.find_element_by_xpath(
                '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[1]/button'
            )
            log_in_by_text.click()
            # If the first path doesn't work, that means the phone log in is either in the second or third path
        except NoSuchElementException:
            # Try the second path, if it works, the number of windows that appear is still 1 (Window to enter phone #)
            log_in_by_text = self.driver.find_element_by_xpath(
                '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'
            )
            log_in_by_text.click()
            sleep(3)

            # If first path isn't the phone number and the second path isn't the phone number,
            # The second path is the Facebook login, which pops up a second window.
            # To deal with this second window, command+w out of it and select the third option
            if len(self.driver.window_handles) >= 2:  # important in order to reload page b/c you get error page after exiting Facebook popup
                # switch the Facebook window
                self.driver.switch_to.window(self.driver.window_handles[1])

                # close the window through command w
                keyboard.press(Key.cmd)
                keyboard.press('w')
                keyboard.release('w')
                keyboard.release(Key.cmd)
                sleep(2)
                # After you close window, you need to refresh page
                # because you are given new UI
                keyboard.press(Key.cmd)
                keyboard.press('r')
                keyboard.release('r')
                keyboard.release(Key.cmd)

                sleep(5)
                # Important: We need to command tab a new window in order to keep the if condition true
                keyboard.press(Key.cmd)
                keyboard.press('t')
                keyboard.release('t')
                keyboard.release(Key.cmd)
                # switch back to tinder (aka command+1)
                self.driver.switch_to.window(self.driver.window_handles[0])

                # Select the third option which should be the phone login screen
                log_in_by_text = self.driver.find_element_by_xpath(
                    '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[3]/button'
                )
                log_in_by_text.click()

        sleep(1)
        # Now, we have the phone number screen up and we can enter our phone number
        self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/div[2]/div/input').send_keys(phone_num)
        login = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button')
        login.click()

        # My computer takes 6 seconds for the Tinder message notification to pop up in the top right screen
        sleep(6)
        # This line calls the screen_shot() method above, which takes a screen shot of the top right corner of the screen
        # With tesseract-OCR and returns the code that Tinder sends you. It then enters that code into the login popup
        self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/div[3]/input[1]').send_keys(screen_shot())
        sleep(1)
        # Press the continue login button after entering the Tinder 6-digit code
        enter = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        enter.click()

        """When you log in, a bunch of stuff pops up, such as location enabling, premium member upgrades, etc."""
        sleep(5)
        # Allow location tracking
        allow = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        allow.click()

        sleep(3)
        # Not interested in being a premium member
        not_interested = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        not_interested.click()

        sleep(5)
        # No thanks enable location
        no_thanks_loc = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button')
        no_thanks_loc.click()

    @staticmethod
    def like():
        keyboard.press(Key.right)
        keyboard.release(Key.right)
        sleep(0.5)

    def auto_swipe(self):
        while True:
            sleep(0.5)
            try:
                self.like()
            except NoSuchElementException:
                try:
                    self.close_popup()
                except NoSuchElementException:
                    self.close_match()

    def close_popup(self):
        popup = self.driver.find_element_by_xpath(self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]'))
        popup.close()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.close()


# Call the bot
bot = TinderBot()
bot.log_on()



