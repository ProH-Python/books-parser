# Books to Scrape — Web Scraper & Catalog Analytics

A Python script for automated data extraction from [Books to Scrape](https://toscrape.com), data cleaning, database storage, and generating an analytical Excel report.

## 🚀 Features

- **Full Catalog Crawling:** Scrapes all 50 catalog pages (1,000 books) and visits each individual product page.
- **Detailed Data Extraction:**
  - Book title (`Name`)
  - Category (`Category`)
  - Price in GBP (`Price`)
  - Star rating from 1 to 5 (`Rate`)
  - Available stock quantity (`Stock`)
- **Data Processing:** Removes duplicate entries and sorts records by rating (descending) and price (ascending).
- **Multi-Format Export:**
  - `books_store.db` — SQLite database (`books` table).
  - `clean_books.csv` — Cleaned dataset in CSV format.
  - `report.xlsx` — Excel workbook containing two sheets:
    - `All_Books` — Complete list of scraped books.
    - `Category_Stats` — Aggregated statistics by category (number of titles, average price, maximum price, and total stock).

## 🛠 Tech Stack

- **Python 3.x**
- `requests` — HTTP requests
- `beautifulsoup4` — HTML parsing
- `pandas` — Data manipulation, aggregation, and CSV/Excel export
- `sqlite3` — Local SQLite database management
- `openpyxl` — Engine for writing `.xlsx` files (used under the hood by `pandas`)

## 📦 Installation & Usage

1. **Clone the repository or download the script:**
   ```bash
   git clone <your_repository_url>
   cd <project_folder>
   ```

2. **Install the required dependencies:**
   ```bash
   pip install requests beautifulsoup4 pandas openpyxl
   ```

3. **Run the script:**
   ```bash
   python main.py
   ```
   *(Replace `main.py` with your actual filename if different).*

> **Note:** A `time.sleep(0.2)` delay is included between product page requests to avoid overwhelming the server. A full scraping run of all 1,000 books takes approximately 4–5 minutes.

## 📂 Output Structure

Once the script finishes running, the following files will be generated in the root directory:

```text
├── books_store.db    # SQLite database
├── clean_books.csv   # Cleaned dataset in CSV format
└── report.xlsx       # Final report with category analytics
```
