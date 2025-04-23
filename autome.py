from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

MAX_PAGES = 5
base_url = "https://autome.lk/search?paged="

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def wait_for_ads():
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        if soup.find_all('li', class_='rounded-lg'):
            return soup
    return None

def scrape_page(page_num):
    url = f"{base_url}{page_num}"
    print(f"🔍 Visiting: {url}")
    driver.get(url)
    soup = wait_for_ads()
    if not soup:
        print("⚠️ No content loaded.")
        return []

    cars = []
    ads = soup.find_all('li', class_='rounded-lg')
    print(f"✅ Found {len(ads)} ads on page {page_num}")

    for ad in ads:
        try:
            name_tag = ad.find('a', class_='h5')
            name = name_tag.text.strip()
            link = "https://autome.lk" + name_tag['href']
        except:
            name = link = 'N/A'

        try:
            price = ad.find('span', class_='text-danger').text.strip()
        except:
            price = 'N/A'

        try:
            # Extract location (Kandy, Colombo, etc.)
            icon_tag = ad.find('i', class_='fal fa-map-marker-alt mr-2')
            if icon_tag and icon_tag.parent:
               location = icon_tag.parent.get_text(strip=True).replace("▼", "")
            else:
             location = 'N/A'
        except:
            location = 'N/A'
        try:
            # Extract date posted from the title attribute
            date_tag = ad.find('span', class_='text-nowrap mr-3', title=True)
            date_posted = date_tag['title'].replace("Posted on ", "") if date_tag else 'N/A'
        except:
            date_posted = 'N/A'

        cars.append({
            'Name': name,
            'Price': price,
            'Location': location,
            'Date Posted': date_posted,
            'Link': link
        })

    return cars

# Main run
all_cars = []
for page in range(1, MAX_PAGES + 1):
    cars = scrape_page(page)
    if not cars:
        break
    all_cars.extend(cars)

driver.quit()

# Save to CSV
df = pd.DataFrame(all_cars)
df.to_csv("autome_car_listings.csv", index=False)
print(f"✅ Done! Saved {len(df)} listings to autome_car_listings.csv")
print(df.head(10))
