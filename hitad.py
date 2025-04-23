from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# === CONFIG ===
MAX_PAGES = 3 # Number of pages to scrape

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === SCRAPER FUNCTION ===
def scrape_hitad_page(url):
    driver.get(url)
    time.sleep(3)  

    soup = BeautifulSoup(driver.page_source, 'lxml')
    ads = soup.find_all('div', class_='item-info')
    results = []

    for ad in ads:
        try:
            title_tag = ad.find('h4', class_='item-title').find('a')
            title = title_tag['title'].strip()
            link = title_tag['href'].strip()
            if not link.startswith('http'):
                link = "https://www.hitad.lk" + link
        except:
            title, link = 'N/A', 'N/A'

        try:
            price = ad.find('h3', class_='item-price').text.strip().replace('\n', ' ')
        except:
            price = 'N/A'

        try:
            location = ad.find('div', class_='item-cat').find_all('span')[0].text.strip()
        except:
            location = 'N/A'

        try:
            date_text = ad.find('span', class_='dated').find('a').text.strip()
            if "Approved on:" in date_text:
                date = date_text.replace("Approved on:", "").strip()
            else:
                date = 'N/A'
        except:
            date = 'N/A'

        results.append({
            'Title': title,
            'Price': price,
            'Location': location,
            'Date Posted': date,
            'Link': link
        })

    return results

# === MAIN LOOP ===
all_ads = []
for page in range(1, MAX_PAGES + 1):
    print(f"Scraping page {page}...")
    url = f"https://www.hitad.lk/search-sl?keyword=vehicles&page={page}"
    ads = scrape_hitad_page(url)
    if not ads:
        print("No ads found, stopping.")
        break
    all_ads.extend(ads)

driver.quit()

# === SAVE TO CSV ===
df = pd.DataFrame(all_ads)
df.to_csv('hitad_vehicles_data.csv', index=False)
print(df.head())
print("✅ Data saved to hitad_vehicles_data.csv")
