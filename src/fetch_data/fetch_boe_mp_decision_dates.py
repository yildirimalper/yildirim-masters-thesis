from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import pandas as pd
import datetime
from pathlib import Path

driver = webdriver.Chrome()  # or whichever browser you're using
driver.get("https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/monetary-policy-summary-and-minutes")

# Open the CSV file for writing
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Repeat the following steps for each page
    for _ in range(12):  # adjust the range depending on the number of pages
        time.sleep(10)  # wait for the page to load

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # wait for the page to load

        # Extract dates and tags
        date_elements = driver.find_elements(By.XPATH, '//*[@id="SearchResults"]//div/a//time')
        tag_elements = driver.find_elements(By.XPATH, '//*[@id="SearchResults"]//div/a//div')

        # Write dates to the CSV file
        for date, tag in zip(date_elements, tag_elements):
            if tag.text == "News // Monetary Policy Committee (MPC)":
                writer.writerow([date.get_attribute('datetime')])

        # Click the "next" button to go to the next page
        try:
            next_button = driver.find_element(By.XPATH, '//li[@class="list-pagination__list-item"]/a[contains(text(), "Next")]')  # adjust the XPath as needed
            next_button.click()
        except NoSuchElementException:
            break  # no more pages

driver.quit()

# ============================================================
# ! Simply, use the Excel file

PROJECT_DIR = Path().resolve()

data = pd.read_excel(PROJECT_DIR / 'original_data' / 'mpcvoting.xlsx')
data.to_csv(PROJECT_DIR / 'processed_data' / 'monetary_policy_dates' / 'boe_mpd.csv', index=False)