from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

driver_path = "D:/prj_test_1/chromedriver/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Không dùng user-data-dir
driver = webdriver.Chrome(service=Service(driver_path), options=options)
driver.get("https://www.google.com")
time.sleep(5)
