from selenium import webdriver
import selenium
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()


PROMISED_DOWN = 1000
PROMISED_UP = 100
edge_driver_path = "PATH TO DRIVER"
TWITTER_EMAIL = os.getenv("email")
TWITTER_PASSWORD = os.getenv("password")
TWITTER_USERNAME = os.getenv("user")

class InternetSpeedTwitterBot:

    def __init__(self, down, up):
        self.driver = webdriver.Edge(executable_path=edge_driver_path)
        self.down = down
        self.up = up
        self.actual_down = 0
        self.actual_up = 0
    
    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        go_btn = self.driver.find_element_by_class_name("js-start-test")
        go_btn.click()
        sleep(40)
        self.actual_down = self.driver.find_element_by_css_selector(".download-speed").text
        self.actual_up = self.driver.find_element_by_css_selector(".upload-speed").text
        print(f"Down : {self.actual_down}")
        print(f"Up : {self.actual_up}")
        

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/home")
        sleep(3)
        #First page
        self.email = self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[5]/label/div/div[2]/div/input')
        self.email.send_keys(TWITTER_EMAIL)
        self.driver.find_element_by_css_selector("div.css-18t94o4:nth-child(6) > div:nth-child(1)").click()
        sleep(3)
        #Second Page - only apears sometimes.
        try:
            self.username = self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
            self.username.send_keys(TWITTER_USERNAME)
            self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div').click()
        except selenium.common.exceptions.ElementNotInteractableException:
            pass
        sleep(3)
        #Third Page
        self.password = self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input')
        self.password.send_keys(TWITTER_PASSWORD)
        self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div').click()
        sleep(5)
        #Tweet
        self.box = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div')
        self.box.send_keys(f"Hey Partner! Why is my internet speed {self.actual_down}down/{self.actual_up} when I pay for {self.down}down/{self.up}up?")
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]').click()


bot = InternetSpeedTwitterBot(PROMISED_DOWN, PROMISED_UP)
internet_speed = bot.get_internet_speed()
bot.tweet_at_provider()
    