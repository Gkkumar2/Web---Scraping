from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# === SETUP OPTIONS ===
MAX_PAGES = 5  

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Adjust if needed

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === SCRAPER FUNCTION ===
def scrape_page(url):
    driver.get(url)
    time.sleep(3) 
    soup = BeautifulSoup(driver.page_source, 'lxml')
    ads = soup.find_all('div', class_='result-item')
    carList = []

    for ad in ads:
        try:
            name = ad.find('h4', class_='result-title').text.strip()
        except:
            name = 'N/A'

        try:
            price = ad.find('label', style=lambda value: value and '#8f4299' in value).text.strip()
        except:
            price = 'N/A'

        try:
            date = ad.find('strong').text.strip()
        except:
            date = 'N/A'

        try:
            link_tag = ad.find('div', class_='result-img').find('a', href=True)
            link = link_tag['href']
            if not link.startswith('http'):
                link = "https://www.patpat.lk" + link
        except:
            link = 'N/A'

        carList.append({
            'Name': name,
            'Price': price,
            'Date Posted': date,
            'Link': link
        })

    return carList

# === MAIN SCRAPING LOOP ===
allCars = []
for page in range(1, MAX_PAGES + 1):
    print(f"Scraping page {page}...")
    page_url = f"https://www.patpat.lk/vehicle?page={page}"
    cars = scrape_page(page_url)
    if not cars:
        print("No more ads found, stopping.")
        break
    allCars.extend(cars)

driver.quit()

# === SAVE RESULTS ===
df = pd.DataFrame(allCars)
print(df.head())
df.to_csv('patpat_car_data_all_pages.csv', index=False)
print("✅ Data saved to patpat_car_data_all_pages.csv")
