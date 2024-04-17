import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Setup Selenium
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

# Load the page
driver.get('https://www.ecb.europa.eu/press/govcdec/mopo/html/index.en.html')

# Wait for the page to load
time.sleep(5)

# Scroll down the page
for _ in range(100):  # Adjust this value based on how much you need to scroll
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)  # Pause in between scrolls

# Find the dates
dates = driver.find_elements(By.XPATH, '//dt[@isodate]/div[@class="date"]')

# Open a CSV file in write mode
with open('processed_data/monetary_policy_decision_dates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the dates to the CSV file
    for date in dates:
        date_text = date.text
        if date_text:  # Only write dates that are not empty
            writer.writerow([date_text])

# Close the driver
driver.quit()