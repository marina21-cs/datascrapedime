# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test the Scraper
```bash
python test_scraper.py
```

This will verify that:
- ✅ The API is accessible
- ✅ Your internet connection works
- ✅ The scraper can fetch data

### Step 3: Run the Full Scraper

Choose one of these options:

#### Option A: Scrape ALL Projects (Recommended)
```bash
python dime_scraper.py
```
- Scrapes all projects regardless of status
- Saves to `scraped_data/` directory
- Creates files with 1000 records each

#### Option B: Scrape Only Completed Projects
```bash
python scrape_completed.py
```
- Scrapes only projects with "Completed" status
- Saves to `scraped_data/completed/` directory

#### Option C: Scrape Only Incomplete Projects
```bash
python scrape_incomplete.py
```
- Scrapes only projects with "Incomplete" status
- Saves to `scraped_data/incomplete/` directory

## 📊 What You'll Get

After running the scraper, you'll have:

1. **JSON Files** in the `scraped_data/` directory
   - Each file contains up to 1000 project records
   - Files are named with timestamps and part numbers
   - Example: `dime_projects_all_20231123_143022_part_001_of_005.json`

2. **Log File** (`dime_scraper.log`)
   - Detailed execution log
   - Error messages (if any)
   - Progress tracking

## 📁 Output Structure

```
scraped_data/
├── dime_projects_all_20231123_143022_part_001_of_005.json  (1000 records)
├── dime_projects_all_20231123_143022_part_002_of_005.json  (1000 records)
├── dime_projects_all_20231123_143022_part_003_of_005.json  (1000 records)
├── dime_projects_all_20231123_143022_part_004_of_005.json  (1000 records)
└── dime_projects_all_20231123_143022_part_005_of_005.json  (532 records)
```

## 🔍 Each Project Contains

- **Basic Info**: Name, code, description, status
- **Location**: Coordinates, address, region, province, city, barangay
- **Financial**: Cost, utilized amount
- **Organizations**: Implementing offices, contractors, source of funds
- **Timeline**: Date started, completion dates
- **Progress**: Latest progress information
- And more...

## ⚡ Quick Tips

1. **Internet Connection**: Make sure you have a stable connection
2. **Time**: Scraping all projects might take 10-30 minutes depending on your connection
3. **Logs**: Check `dime_scraper.log` if something goes wrong
4. **Resume**: If scraping fails, just run it again - it creates new timestamped files

## ❓ Common Questions

**Q: How long does it take?**
A: Depends on the total number of projects and your internet speed. Usually 10-30 minutes for all data.

**Q: Can I stop and resume?**
A: The scraper doesn't resume from where it stopped. It will create new files with a new timestamp if you run it again.

**Q: How much disk space do I need?**
A: Each project is roughly 1-2 KB in JSON format. 5000 projects ≈ 5-10 MB.

**Q: What if I get errors?**
A: Check the log file for details. Most errors are due to internet connection issues.

## 🛠️ Troubleshooting

**Problem: "Connection refused" or "Timeout"**
- Check your internet connection
- Try again in a few minutes
- The DIME server might be temporarily down

**Problem: "No data retrieved"**
- Verify the website is accessible: https://www.dime.gov.ph
- Check your firewall settings
- Review the log file for specific errors

**Problem: Script stops in the middle**
- This is usually due to network issues
- The script saves what it collected before stopping
- Just run it again to get a fresh complete dataset

## 📞 Need Help?

1. Check the log file: `dime_scraper.log`
2. Read the full README: `README.md`
3. Test with the test script: `python test_scraper.py`

---

**Ready to start?** Run `python test_scraper.py` first!
