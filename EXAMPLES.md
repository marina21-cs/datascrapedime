# Usage Examples

This document provides practical examples of how to use the DIME scraper.

## Basic Examples

### 1. Test the Connection
Before scraping all data, test that everything works:

```bash
python test_scraper.py
```

This will:
- Test the API connection
- Fetch 10 sample projects
- Display sample project information
- Confirm the scraper is working

---

### 2. Scrape All Projects
Get all projects regardless of status:

```bash
python dime_scraper.py
```

**Output:**
- Directory: `scraped_data/`
- Files: `dime_projects_all_YYYYMMDD_HHMMSS_part_XXX_of_YYY.json`
- Each file: 1000 projects (except the last one)

---

### 3. Scrape Only Completed Projects
Get projects that have been completed:

```bash
python scrape_completed.py
```

**Output:**
- Directory: `scraped_data/completed/`
- Files: `dime_projects_completed_YYYYMMDD_HHMMSS_part_XXX_of_YYY.json`

---

### 4. Scrape Only Incomplete Projects
Get projects that are still ongoing:

```bash
python scrape_incomplete.py
```

**Output:**
- Directory: `scraped_data/incomplete/`
- Files: `dime_projects_incomplete_YYYYMMDD_HHMMSS_part_XXX_of_YYY.json`

---

### 5. Analyze Scraped Data
After scraping, analyze the data to see statistics:

```bash
python analyze_data.py
```

Or analyze a specific directory:

```bash
python analyze_data.py scraped_data/completed
```

**This will show:**
- Total number of projects
- Total cost
- Projects by status
- Projects by region
- Top implementing offices
- Source of funds statistics

---

## Advanced Examples

### Custom Python Script

Create your own script for custom scraping:

```python
from dime_scraper import DIMEScraper

# Initialize with custom settings
scraper = DIMEScraper(
    output_dir="my_custom_data",
    records_per_file=500  # 500 records per file instead of 1000
)

# Scrape all projects
all_projects = scraper.scrape_all_projects(
    status=None,           # No status filter
    per_page=100,          # 100 records per API call
    max_retries=5,         # Retry 5 times on error
    retry_delay=10         # Wait 10 seconds between retries
)

print(f"Retrieved {len(all_projects)} projects")

# Save to JSON
scraper.save_projects_to_json(all_projects, prefix="custom_scrape")
```

---

### Scrape Multiple Statuses

```python
from dime_scraper import DIMEScraper

scraper = DIMEScraper(output_dir="scraped_data/by_status")

# Scrape both completed and incomplete
scraper.scrape_by_status(statuses=["Completed", "Incomplete"])
```

---

### Process Data After Scraping

```python
import json
from pathlib import Path

# Load all JSON files
data_dir = Path("scraped_data")
all_projects = []

for json_file in data_dir.glob("*.json"):
    with open(json_file, 'r') as f:
        data = json.load(f)
        all_projects.extend(data.get('projects', []))

print(f"Total projects loaded: {len(all_projects)}")

# Filter projects by region
ncr_projects = [p for p in all_projects if "NCR" in p.get('region', '')]
print(f"Projects in NCR: {len(ncr_projects)}")

# Calculate total cost
total_cost = sum(p.get('cost', 0) or 0 for p in all_projects)
print(f"Total cost: ₱{total_cost:,.2f}")

# Find most expensive project
most_expensive = max(all_projects, key=lambda p: p.get('cost', 0) or 0)
print(f"Most expensive project: {most_expensive.get('projectName')}")
print(f"Cost: ₱{most_expensive.get('cost', 0):,.2f}")
```

---

### Export to CSV

```python
import json
import csv
from pathlib import Path

# Load all projects
data_dir = Path("scraped_data")
all_projects = []

for json_file in data_dir.glob("*.json"):
    with open(json_file, 'r') as f:
        data = json.load(f)
        all_projects.extend(data.get('projects', []))

# Export to CSV
with open('projects.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow([
        'ID', 'Project Name', 'Status', 'Cost', 'Region', 
        'Province', 'City', 'Description'
    ])
    
    # Write data
    for project in all_projects:
        writer.writerow([
            project.get('id', ''),
            project.get('projectName', ''),
            project.get('status', ''),
            project.get('cost', 0),
            project.get('region', ''),
            project.get('province', ''),
            project.get('city', ''),
            project.get('description', '')[:100]  # First 100 chars
        ])

print(f"Exported {len(all_projects)} projects to projects.csv")
```

---

### Filter and Save Specific Projects

```python
from dime_scraper import DIMEScraper
import json

# Scrape all projects
scraper = DIMEScraper()
all_projects = scraper.scrape_all_projects()

# Filter projects by criteria
high_cost_projects = [
    p for p in all_projects 
    if (p.get('cost', 0) or 0) > 1000000  # Over 1 million
]

# Save filtered projects
with open('high_cost_projects.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total': len(high_cost_projects),
        'projects': high_cost_projects
    }, f, indent=2, ensure_ascii=False)

print(f"Found {len(high_cost_projects)} high-cost projects")
```

---

## Real-World Scenarios

### Scenario 1: Daily Data Backup

Create a cron job or scheduled task to scrape data daily:

```bash
#!/bin/bash
# daily_scrape.sh

cd /path/to/datascrapedime
python dime_scraper.py >> daily_scrape.log 2>&1
```

Set up cron (Linux/Mac):
```bash
# Run daily at 2 AM
0 2 * * * /path/to/daily_scrape.sh
```

---

### Scenario 2: Regional Analysis

Scrape all data and analyze by region:

```python
from dime_scraper import DIMEScraper
from collections import defaultdict
import json

# Scrape all projects
scraper = DIMEScraper()
all_projects = scraper.scrape_all_projects()

# Group by region
by_region = defaultdict(list)
for project in all_projects:
    region = project.get('region', 'Unknown')
    by_region[region].append(project)

# Save each region separately
for region, projects in by_region.items():
    safe_name = region.replace('/', '_').replace(' ', '_')
    filename = f"region_{safe_name}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({'region': region, 'projects': projects}, f, indent=2)
    
    print(f"{region}: {len(projects)} projects")
```

---

### Scenario 3: Monitor Changes

Scrape data weekly and compare changes:

```python
import json
from datetime import datetime

# Load previous scrape
with open('previous_scrape.json', 'r') as f:
    previous_data = json.load(f)
previous_projects = {p['id']: p for p in previous_data['projects']}

# Load current scrape
with open('current_scrape.json', 'r') as f:
    current_data = json.load(f)
current_projects = {p['id']: p for p in current_data['projects']}

# Find changes
new_projects = set(current_projects.keys()) - set(previous_projects.keys())
removed_projects = set(previous_projects.keys()) - set(current_projects.keys())

status_changes = []
for project_id in set(current_projects.keys()) & set(previous_projects.keys()):
    old_status = previous_projects[project_id].get('status')
    new_status = current_projects[project_id].get('status')
    
    if old_status != new_status:
        status_changes.append({
            'id': project_id,
            'name': current_projects[project_id].get('projectName'),
            'old_status': old_status,
            'new_status': new_status
        })

print(f"New projects: {len(new_projects)}")
print(f"Removed projects: {len(removed_projects)}")
print(f"Status changes: {len(status_changes)}")

for change in status_changes:
    print(f"  {change['name']}: {change['old_status']} → {change['new_status']}")
```

---

## Tips and Best Practices

1. **Always test first**: Run `python test_scraper.py` before full scraping
2. **Check logs**: Review `dime_scraper.log` for any issues
3. **Be patient**: Large scrapes can take 20-30 minutes
4. **Save bandwidth**: Don't scrape more frequently than needed
5. **Backup data**: Keep copies of scraped data with timestamps
6. **Use filters**: Scrape only what you need (by status, etc.)
7. **Monitor disk space**: Each full scrape might be 10-50 MB
8. **Parse incrementally**: Process large JSON files in chunks if needed

---

## Command Reference

| Command | Description | Output Location |
|---------|-------------|-----------------|
| `python test_scraper.py` | Test connection | `test_data/` |
| `python dime_scraper.py` | Scrape all projects | `scraped_data/` |
| `python scrape_completed.py` | Scrape completed only | `scraped_data/completed/` |
| `python scrape_incomplete.py` | Scrape incomplete only | `scraped_data/incomplete/` |
| `python analyze_data.py` | Analyze scraped data | Console output |
| `python analyze_data.py <dir>` | Analyze specific directory | Console output |

---

**Need more help?** Check:
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `dime_scraper.log` - Execution logs
