# 🚗 Sri Lankan Vehicle Listing Web Scrapers

This project includes **three independent Python scripts** that scrape vehicle listings from popular Sri Lankan marketplaces:

- 🔹 [Patpat.lk](https://www.patpat.lk/)
- 🔹 [Autome.lk](https://autome.lk/)
- 🔹 [Hitad.lk](https://www.hitad.lk/)

Each script fetches car name, price, location, date posted, and link to the listing. The data is saved into a structured CSV file for further analysis or automation purposes.

---

## 📁 Project Files

- `patpat.py` – Scrapes listings from Patpat.lk
- `autome.py` – Scrapes listings from Autome.lk
- `hitad.py` – Scrapes listings from Hitad.lk
- `requirements.txt` – Required Python dependencies
- `README.md` – Documentation and usage instructions

---

## 🛠 Installation & Setup

1. **Install Python 3.7+**

2. **Install dependencies:**

```bash
pip install -r requirements.txt
---
```
## 📦 Requirements

Make sure you have the following Python libraries installed:

### `requirements.txt`

```text
selenium
webdriver-manager
beautifulsoup4
pandas
lxml
```
## 🚀 How to Run the Scripts
1️⃣ Patpat.lk Scraper
- File: patpat.py

Output: patpat_car_data_all_pages.csv

Scrapes up to MAX_PAGES of vehicle listings and extracts:

- Title
- Price
- Date Posted
- Link

Run command:
```bash
python patpat.py
```

2️⃣ Autome.lk Scraper
- File: autome.py

Output: autome_car_listings.csv

Scrapes listings using dynamic scrolling and extracts:

- Name
- Price
- Location
- Date Posted
- Link

Run command:

```bash
python autome.py
```

3️⃣ Hitad.lk Scraper
- File: hitad_scraper.py

Output: hitad_vehicles_data.csv

Scrapes vehicle classifieds and extracts:

- Title
- Price
- Location
- Date Posted
- Link

Run command:

```bash
python hitad.py
```

### 💡 Use Cases
- 🔍 Price comparison across multiple marketplaces

- 📊 Market analysis and tracking trends in Sri Lankan vehicle pricing

- 📂 Automated data collection for dealerships and aggregators

- 🧠 Machine learning datasets for vehicle price prediction or recommendation models

### ⚠️ Notes
- All scrapers use headless Chrome for background operation.

- ChromeDriver is auto-managed via webdriver-manager.

- If the website layout changes, you may need to update the HTML selectors.

- You can control how many pages are scraped using the MAX_PAGES variable in each script.

