from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import pandas as pd
import datetime
from pathlib import Path

driver = webdriver.Chrome() 
driver.get("https://www.moneycontrol.com/economic-calendar/canada-boc-monetary-policy-report/3069585")
# /html/body/section/div/div/div[2]/div[5]/table/tbody/tr[4]/td[1]/span

# Open the CSV file for writing
with open('processed_data/monetary_policy_dates/boc_mpd_raw.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Repeat the following steps for each page
    for _ in range(60):  # adjust the range depending on the number of pages
        time.sleep(10)  # wait for the page to load

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)  # wait for the page to load

        # Click the "Show More" button
        show_more_button = driver.find_elements(By.XPATH, '/html/body/section/div/div/div[2]/div[5]/div[2]/div/a')[0]
        show_more_button.click()

        # Extract dates and contents
        date_elements = driver.find_elements(By.XPATH, '/html/body/section/div/div/div[2]/div[5]/table/tbody/tr/td[1]/span')
        content_elements = driver.find_elements(By.XPATH, '/html/body/section/div/div/div[2]/div[5]/table/tbody/tr/td[3]')

        # Write dates to the CSV file if the content is either "BoC Interest Rate Decision" or "Interest Rate Decision"
        for date_element, content_element in zip(date_elements, content_elements):
            if content_element.text in ["BoC Interest Rate Decision", "Interest Rate Decision", "Interest Rate Mar", "Interest Rate Apr", "Interest Rate Feb", "Interest Rate Jan", "Interest Rate Dec", "Interest Rate Nov", "Interest Rate May", "Interest Rate Jun", "Interest Rate Jul", "Interest Rate Aug", "Interest Rate Sep", "Interest Rate Oct"]:
                writer.writerow([date_element.text])

# Close the driver
driver.quit()

# ===========================

PROJECT_DIR = Path().resolve()

data = pd.read_csv('processed_data/monetary_policy_dates/boc_mpd_raw.csv', header=None)

# Drop duplicates
data2 = data.drop_duplicates()
data2 = data2.reset_index(drop=True)
data2[0] = pd.to_datetime(data2[0])
data2.to_csv(PROJECT_DIR / "processed_data" / "monetary_policy_dates" / "boc_mpd.csv", index=False) 