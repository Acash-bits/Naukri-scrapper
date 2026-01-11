import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

# Naukri.com URL to get the data from it
url = 'https://www.naukri.com/business-analyst-jobs-in-delhi-ncr?k=business%20analyst&l=delhi%20%2F%20ncr%2C%20gurugram%2C%20noida&experience=4&nignbevent_src=jobsearchDeskGNB'

# Setup Headless Chrome options
# 2. Setup Headless Options
chrome_options = Options()
chrome_options.add_argument("--headless=new") # Runs in background
chrome_options.add_argument("--window-size=1920,1080") # Set size so it "sees" the layout correctly
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Using the selenium driver to get the selenium HTML source code
driver = webdriver.Chrome(options=chrome_options)
print("Opening the Naukri URL in Chrome")
driver.get(url)

# Time stoppage to load the data before processing of data is started
time.sleep(10)

soup = BeautifulSoup(driver.page_source,'html.parser')

job_cards = soup.find_all('div', class_= 'srp-jobtuple-wrapper')

job_data = [] # List to hold all job data

for job in job_cards:
    # Job Tittle 
    title_tag = job.find('a', class_='title')
    # Company Name
    company_tag = job.find('a', class_='comp-name' )
    # Experience for the job
    experience_tag = job.find('span', class_ ='exp-wrap')
    # Location of the job
    location_tag = job.find('span', class_='loc-wrap')

    if title_tag:
        job_dict = {
            'Title': title_tag.text.strip() if company_tag else 'N/A',
            'Company': company_tag.text.strip() if company_tag else 'N/A',
            'Experience': experience_tag.text.strip() if experience_tag else 'N/A',
            'Location': location_tag.text.strip() if location_tag else 'N/A',
            'Link': title_tag.get('href', 'N/A')
        }
        job_data.append(job_dict)


# Display the date in the terminal
if job_data:
    df = pd.DataFrame(job_data)

    # Settings to show ALL columns and rows in terminal
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 50)

    print("\n" + "="*50)
    print(f"FOUND {len(job_data)} JOBS")
    print("="*50 + "\n")
    print(df)

driver.quit()