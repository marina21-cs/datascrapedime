"""
Example: Scrape only Incomplete projects
"""

from dime_scraper import DIMEScraper
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('incomplete_projects_scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("="*60)
    logger.info("Scraping INCOMPLETE projects only")
    logger.info("="*60)
    
    # Initialize scraper
    scraper = DIMEScraper(
        output_dir="scraped_data/incomplete",
        records_per_file=1000
    )
    
    # Scrape only incomplete projects
    scraper.scrape_by_status(statuses=["Incomplete"])
    
    logger.info("="*60)
    logger.info("Completed! Check 'scraped_data/incomplete/' directory")
    logger.info("="*60)

if __name__ == "__main__":
    main()
