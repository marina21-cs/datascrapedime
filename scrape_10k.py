"""
Scrape exactly 10,000 project records from DIME Philippines Dashboard
Saves data in JSON files with 1000 records each (10 files total if 10k records available)
"""

from dime_scraper import DIMEScraper
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scrape_10k.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("="*60)
    logger.info("DIME Philippines - Scraping 10,000+ Records")
    logger.info("="*60)
    
    # Initialize scraper
    scraper = DIMEScraper(
        output_dir="scraped_data",
        records_per_file=1000  # 1000 records per JSON file
    )
    
    logger.info("Starting scrape to collect at least 10,000 project records...")
    logger.info("This will create multiple JSON files with 1000 records each")
    
    try:
        # Scrape all projects - API will return all available data
        all_projects = scraper.scrape_all_projects(
            status=None,        # No filter - get all projects
            per_page=100,       # Fetch 100 records per API call
            max_retries=3,      # Retry failed requests 3 times
            retry_delay=5       # Wait 5 seconds between retries
        )
        
        total_scraped = len(all_projects)
        logger.info(f"="*60)
        logger.info(f"✅ Successfully scraped {total_scraped:,} projects")
        
        if total_scraped >= 10000:
            logger.info(f"✅ TARGET REACHED: {total_scraped:,} records (10,000+ goal achieved!)")
        elif total_scraped > 0:
            logger.info(f"⚠️  Only {total_scraped:,} projects available (less than 10,000)")
            logger.info(f"   This is all the data available from the DIME dashboard")
        else:
            logger.error(f"❌ No projects were scraped. Check the logs for errors.")
            return
        
        # Save to JSON files
        logger.info(f"="*60)
        logger.info("Saving data to JSON files...")
        scraper.save_projects_to_json(all_projects, prefix="dime_projects_all")
        
        # Calculate file count
        num_files = (total_scraped + 999) // 1000  # Round up
        logger.info(f"="*60)
        logger.info(f"✅ SCRAPING COMPLETE!")
        logger.info(f"="*60)
        logger.info(f"📊 Total Records: {total_scraped:,}")
        logger.info(f"📁 Total Files: {num_files}")
        logger.info(f"📂 Location: scraped_data/")
        logger.info(f"💾 Records per file: 1,000 (last file may have fewer)")
        logger.info(f"="*60)
        
    except Exception as e:
        logger.error(f"❌ Error during scraping: {e}")
        logger.error(f"Check 'scrape_10k.log' for detailed error information")
        return

if __name__ == "__main__":
    main()
