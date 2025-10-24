# x_api.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_SECRET")
)

def x_hesap_ac(email, phone):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    
    driver.get("https://x.com/i/flow/signup")
    time.sleep(5)
    
    driver.find_element(By.NAME, "name").send_keys(f"Bot{random.randint(1,999)}")
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(2)
    
    driver.find_element(By.NAME, "phone_number").send_keys(phone[1:])
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(5)
    
    return driver