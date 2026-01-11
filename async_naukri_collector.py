import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import pandas as pd
from bs4 import BeautifulSoup

job_urls = {
    'Business Analyst': 'https://www.naukri.com/business-analyst-jobs-in-delhi-ncr?k=business+analyst&l=delhi+%2F+ncr%2C+gurugram%2C+noida&experience=4',
    'Senior Business Analyst': 'https://www.naukri.com/senior-business-analyst-jobs-in-delhi-ncr?k=senior+business+analyst&l=delhi+%2F+ncr%2C+gurugram%2C+noida&experience=4',
    'Data Analyst': 'https://www.naukri.com/data-analyst-jobs-in-delhi-ncr?k=data+analyst&l=delhi+%2F+ncr%2C+gurugram%2C+noida&experience=4',
    'Product Manager': 'https://www.naukri.com/product-manager-jobs-in-delhi-ncr?k=product+manager&l=delhi+%2F+ncr%2C+gurugram%2C+noida&experience=4'
}

# CONFIGURE HOW MANY PAGES TO SCRAPE
MAX_PAGES = 5  # Set to desired number of pages to scrape per category

def generate_page_url(base_url, page_num):
    if page_num ==1:
        return base_url
    
    # Split URL at '?' to insert page number
    if '?' in base_url:
        base_part, query_part = base_url.split('?', 1)
        return f"{base_part}-{page_num}?{query_part}"
    return f"{base_url}-{page_num}"


async def scrape_tab(context, category, base_url, max_pages):
    """Scrapes multiple pages for a single job category"""
    page = await context.new_page()
    
    # Apply stealth
    stealth_config = Stealth()
    await stealth_config.apply_stealth_async(page)
    
    print(f"🚀 Scraping: {category} Page-1 to Page{max_pages}")

    all_results = [] # Aggregate results from all pages
    
    try:
        # Loop through each page
        for page_num in range(1, max_pages + 1):
            # Generate URL for current page
            url=generate_page_url(base_url, page_num)
            print(f"   📄 Page {page_num}: {url}")

            try:
                # Navigate to the page
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # Wait for the page to load
                await asyncio.sleep(5)
                
                # Get the page HTML content
                html_content = await page.content()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                job_cards = soup.find_all('div', class_='srp-jobtuple-wrapper')
                
                page_results = []
                
                for job in job_cards:
                    # Job Title
                    title_tag = job.find('a', class_='title')
                    # Company Name
                    company_tag = job.find('a', class_='comp-name')
                    # Experience for the job
                    experience_tag = job.find('span', class_='exp-wrap')
                    # Location of the job
                    location_tag = job.find('span', class_='loc-wrap')
                    
                    if title_tag:
                        job_dict = {
                            'Category': category,
                            'Title': title_tag.text.strip() if title_tag else 'N/A',
                            'Company': company_tag.text.strip() if company_tag else 'N/A',
                            'Experience': experience_tag.text.strip() if experience_tag else 'N/A',
                            'Location': location_tag.text.strip() if location_tag else 'N/A',
                            'Link': title_tag.get('href', 'N/A')
                        }
                        page_results.append(job_dict)
                
                print(f"✅ Found {len(page_results)} jobs for {category}")
                
                # Add page results to all results
                all_results.extend(page_results)
            
                if page_num < max_pages:
                    delay = 10 # 10 Seconds delay between pages
                    print(f'⏳ Waiting for {delay} seconds before next page...')
                    await asyncio.sleep(delay)
            
            except Exception as e:
                print(f"⚠️ Error while scraping {category} Page-{page_num}: {e}")
                # Continue to next page
                continue
            
        print(f"✅ Total: {len(all_results)} jobs for {category} across {max_pages} pages\n")
        return all_results

    except Exception as e:
        print(f"⚠️ Error in {category}: {e}")
        return all_results
    finally:
        await page.close()

async def main():
    async with async_playwright() as p:
        # Launch with additional anti-detection flags
        browser = await p.chromium.launch(
            headless=False,
            args=[
                # '--headless=new', # Uncomment to run in headless mode
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        # Create context with more realistic settings
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='Asia/Kolkata',  # Match your location
            permissions=['geolocation'],
            geolocation={'latitude': 28.6139, 'longitude': 77.2090},  # Delhi coordinates
            color_scheme='light',
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        
        # Scrape all URLs concurrently
        tasks = [scrape_tab(context, cat, url, MAX_PAGES) for cat, url in job_urls.items()]
        all_pages_data = await asyncio.gather(*tasks)
        
        # Flatten the results
        all_job_data = [item for sublist in all_pages_data for item in sublist]
        
        # Display the data in the terminal
        if all_job_data:
            df = pd.DataFrame(all_job_data)
            
            # Settings to show ALL columns and rows in terminal
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 2000)
            pd.set_option('display.max_colwidth', None)
            
            print("\n" + "="*80)
            print(f"FOUND {len(all_job_data)} JOBS")
            print("="*80 + "\n")

            # Show summary by category
            print('Summary by Category:')
            print(df.groupby('Category').size())
            print('\n' + "="*80 + "\n")

            print(df)
        else:
            print("No job data found. Check the site structure or your selectors or block status")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())