# Scraper Scripts

This folder contains all the Python scripts used for scraping data from the DIME Philippines Dashboard.

## Scripts

### Main Scraper
- **`dime_scraper.py`** - Main scraper class and default scraping script
  - Contains the `DIMEScraper` class with all scraping functionality
  - Scrapes all projects without filters
  - Use: `python scraper/dime_scraper.py`

### Specialized Scrapers
- **`scrape_10k.py`** - Scrape 10,000+ records (recommended)
  - Specifically designed to collect at least 10,000 records
  - Provides detailed statistics and success confirmation
  - Use: `python scraper/scrape_10k.py`

- **`scrape_completed.py`** - Scrape only completed projects
  - Filters for projects with "Completed" status
  - Use: `python scraper/scrape_completed.py`

- **`scrape_incomplete.py`** - Scrape only incomplete projects
  - Filters for projects with "Incomplete" status
  - Use: `python scraper/scrape_incomplete.py`

### Testing & Analysis
- **`test_scraper.py`** - Test the scraper setup
  - Fetches a small sample to verify everything works
  - Always run this first before full scraping
  - Use: `python scraper/test_scraper.py`

- **`analyze_data.py`** - Analyze scraped data
  - Shows statistics about scraped JSON files
  - Displays project counts by status, region, implementing offices, etc.
  - Use: `python scraper/analyze_data.py`

## Quick Start

```bash
# 1. Test the scraper
python scraper/test_scraper.py

# 2. Run the main scraper
python scraper/scrape_10k.py

# 3. Analyze the results
python scraper/analyze_data.py
```

## Output

All scripts save data to the `scraped_data/` folder in the project root.
