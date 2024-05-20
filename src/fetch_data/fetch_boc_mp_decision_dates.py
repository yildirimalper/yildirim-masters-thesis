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
driver.get("https://www.fxstreet.com/economic-calendar/event/7035bb7e-d65f-4e72-a0ba-f77baede0207")
# /html/body/section/div/div/div[2]/div[5]/table/tbody/tr[4]/td[1]/span
# //*[@id="Content_C025_Col00"]/div[2]/div/div/div[3]/div/div/div/div/table[2]/tbody/tr[9]/td[1]/span

# Open the CSV file for writing
with open('processed_data/monetary_policy_dates/boc_mpd_raw.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Repeat the following steps for each page
    for _ in range(2):  # adjust the range depending on the number of pages
        time.sleep(6)  # wait for the page to load

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)  # wait for the page to load

        # Extract dates
        for i in range(1, 500):  # adjust the range depending on the number of dates on each page
            xpath = f'//*[@id="Content_C025_Col00"]/div[2]/div/div/div[3]/div/div/div/div/table[2]/tbody/tr[{i}]/td[1]/span'
            date_elements = driver.find_elements(By.XPATH, xpath)

            # Write dates to the CSV file
            for date_element in date_elements:
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