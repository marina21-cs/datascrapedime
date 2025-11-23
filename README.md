# DIME Philippines Data Scraper

A Python web scraper to extract project data from the DIME (Digital Information for Monitoring and Evaluation) Philippines Dashboard at https://www.dime.gov.ph

## Features

- ✅ Scrapes all project data from DIME Philippines dashboard
- ✅ Automatic pagination handling
- ✅ Saves data in JSON format with 1000 records per file
- ✅ Comprehensive error handling and retry logic
- ✅ Progress logging to both console and file
- ✅ Respects server with rate limiting between requests
- ✅ Filters by project status (Completed, Incomplete, or All)
- ✅ Extracts complete project information including:
  - Project name, code, and description
  - Location details (coordinates, address, region, province, city, barangay)
  - Cost and utilized amount
  - Status and progress
  - Implementing offices
  - Contractors and source of funds
  - Timeline information
  - And more...

## Installation

1. **Clone or download this repository**

2. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper to get all projects:

```bash
python dime_scraper.py
```

This will:
- Scrape all projects from the DIME dashboard
- Save them to the `scraped_data/` directory
- Split the data into JSON files with 1000 records each
- Create a log file `dime_scraper.log` with detailed execution logs

### Advanced Usage

You can customize the scraper by modifying the `main()` function in `dime_scraper.py`:

**Option 1: Scrape all projects (default)**
```python
scraper.scrape_by_status(statuses=[None])
```

**Option 2: Scrape by specific status**
```python
scraper.scrape_by_status(statuses=["Completed"])
```

**Option 3: Scrape multiple statuses**
```python
scraper.scrape_by_status(statuses=["Completed", "Incomplete"])
```

**Option 4: Customize records per file**
```python
scraper = DIMEScraper(
    output_dir="my_data",
    records_per_file=500  # 500 records per file instead of 1000
)
```

## Output Format

### File Structure

The scraper creates files with the following naming pattern:
```
dime_projects_[status]_[timestamp]_part_[number]_of_[total].json
```

Example:
```
scraped_data/
├── dime_projects_all_20231123_143022_part_001_of_005.json
├── dime_projects_all_20231123_143022_part_002_of_005.json
├── dime_projects_all_20231123_143022_part_003_of_005.json
├── dime_projects_all_20231123_143022_part_004_of_005.json
└── dime_projects_all_20231123_143022_part_005_of_005.json
```

### JSON Structure

Each JSON file contains:

```json
{
  "metadata": {
    "total_projects_in_file": 1000,
    "file_number": 1,
    "total_files": 5,
    "records_range": "1-1000",
    "total_projects": 4532,
    "scraped_at": "20231123_143022",
    "source": "DIME Philippines Dashboard",
    "url": "https://www.dime.gov.ph"
  },
  "projects": [
    {
      "id": 23,
      "projectName": "Metro Manila Flood Management Project, Phase I",
      "projectCode": null,
      "description": "...",
      "latitude": 14.624562,
      "longitude": 120.96609,
      "status": "Incomplete",
      "cost": 23500000,
      "utilizedAmount": 0,
      "streetAddress": "...",
      "city": "Manila City",
      "barangay": "Barangay 147",
      "province": "First District",
      "region": "(National Capital Region) NCR",
      "implementingOffices": [...],
      "contractors": [...],
      "sourceOfFunds": [...],
      ...
    }
  ]
}
```

## Logging

The scraper creates a log file `dime_scraper.log` that tracks:
- Pages fetched
- Number of projects retrieved
- Any errors or retries
- File save operations
- Overall progress

Example log output:
```
2023-11-23 14:30:22,123 - INFO - Starting scrape for status: All
2023-11-23 14:30:22,456 - INFO - Fetching page 1 (status: All)
2023-11-23 14:30:23,789 - INFO - Retrieved 100 projects from page 1. Total so far: 100
2023-11-23 14:30:24,123 - INFO - Total pages to fetch: 46
...
2023-11-23 14:35:45,678 - INFO - Saved 1000 projects to dime_projects_all_20231123_143022_part_001_of_005.json
```

## Error Handling

The scraper includes robust error handling:
- **Automatic retries**: Failed requests are retried up to 3 times
- **Retry delays**: 5-second delay between retry attempts
- **Graceful failures**: If a page fails after all retries, the scraper continues and saves what it has collected
- **Rate limiting**: 1-second delay between successful requests to respect the server

## Customization

You can customize the scraper behavior by modifying the `DIMEScraper` class:

```python
scraper = DIMEScraper(
    base_url="https://www.dime.gov.ph",  # Base URL
    output_dir="scraped_data",            # Output directory
    records_per_file=1000                 # Records per JSON file
)

projects = scraper.scrape_all_projects(
    status="Completed",    # Filter by status
    per_page=100,          # Records per API request
    max_retries=3,         # Maximum retry attempts
    retry_delay=5          # Delay between retries
)
```

## Project Information

**Source:** DIME (Digital Information for Monitoring and Evaluation) - Department of Budget and Management, Philippines

**Website:** https://www.dime.gov.ph

**Description:** DIME is a project that aims to augment the management arm of the Department of Budget and Management. DIME leverages the use of modern technologies such as satellites, drones and geotagging in monitoring and evaluating the status, progress, and activities of big-ticket government projects.

## Requirements

- Python 3.7+
- requests library

## License

This scraper is for educational and research purposes. Please respect the DIME dashboard's terms of service and be mindful of server load.

## Troubleshooting

**Issue: Connection errors**
- Check your internet connection
- The DIME server might be temporarily unavailable
- Try again later or reduce the `per_page` parameter

**Issue: No data retrieved**
- The API endpoint might have changed
- Check if the website is accessible
- Review the log file for detailed error messages

**Issue: Incomplete data**
- Check the log file to see which pages failed
- Re-run the scraper - it will create new files with a new timestamp
- The scraper saves progress, so partial data is not lost

## Support

For issues or questions, please check:
1. The log file (`dime_scraper.log`) for detailed error messages
2. Your internet connection
3. That the DIME website is accessible at https://www.dime.gov.ph