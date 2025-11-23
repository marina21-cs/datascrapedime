"""
Example: Scrape only Completed projects
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scraper.dime_scraper import DIMEScraper
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('completed_projects_scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("="*60)
    logger.info("Scraping COMPLETED projects only")
    logger.info("="*60)
    
    # Initialize scraper
    scraper = DIMEScraper(
        output_dir="scraped_data/completed",
        records_per_file=1000
    )
    
    # Scrape only completed projects
    scraper.scrape_by_status(statuses=["Completed"])
    
    logger.info("="*60)
    logger.info("Completed! Check 'scraped_data/completed/' directory")
    logger.info("="*60)

if __name__ == "__main__":
    main()
