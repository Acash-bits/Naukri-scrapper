import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

# Naukri.com URL to get the data from it
job_urls = {
    'Business Analyst': 'https://www.naukri.com/business-analyst-jobs-in-delhi-ncr?k=business%20analyst&l=delhi%20%2F%20ncr%2C%20gurugram%2C%20noida&experience=4',
    'Senior Business Analyst': 'https://www.naukri.com/senior-business-analyst-jobs-in-delhi-ncr?k=senior%20business%20analyst&l=delhi%20%2F%20ncr%2C%20gurugram%2C%20noida&experience=4',
    'Data Analyst': 'https://www.naukri.com/data-analyst-jobs-in-delhi-ncr?k=data%20analyst&l=delhi%20%2F%20ncr%2C%20gurugram%2C%20noida&experience=4',
    'Product Manager': 'https://www.naukri.com/product-manager-jobs-in-delhi-ncr?k=product%20manager&l=delhi%20%2F%20ncr%2C%20gurugram%2C%20noida&experience=4'
}

# Setup Headless Chrome options
# 2. Setup Headless Options
chrome_options = Options()
chrome_options.add_argument("--headless=new") # Runs in background
chrome_options.add_argument("--window-size=1920,1080") # Set size so it "sees" the layout correctly
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Using the selenium driver to get the selenium HTML source code
driver = webdriver.Chrome(options=chrome_options)
all_job_data = [] # List to hold all job data from different URLs
print("Opening the Naukri URL in Chrome")

for category, url in job_urls.items():
    print(f"Scraping jobs for: {category}")
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    soup = BeautifulSoup(driver.page_source,'html.parser')
    job_cards = soup.find_all('div', class_= 'srp-jobtuple-wrapper')

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
            'Category': category, # To track the category of the job
            'Title': title_tag.text.strip() if company_tag else 'N/A',
            'Company': company_tag.text.strip() if company_tag else 'N/A',
            'Experience': experience_tag.text.strip() if experience_tag else 'N/A',
            'Location': location_tag.text.strip() if location_tag else 'N/A',
            'Link': title_tag.get('href', 'N/A')
        }
        all_job_data.append(job_dict)


# Display the date in the terminal
if all_job_data:
    df = pd.DataFrame(all_job_data)

    # Settings to show ALL columns and rows in terminal
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.max_colwidth', None)

    print("\n" + "="*50)
    print(f"FOUND {len(all_job_data)} JOBS")
    print("="*80 + "\n")
    print(df)
else:
    print("No job data found. Check the site structure or your selectors or block status")

driver.quit()