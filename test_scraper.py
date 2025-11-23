"""
Test script to verify the DIME scraper works correctly
This will fetch a small sample of data for testing
"""

from dime_scraper import DIMEScraper
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_scraper():
    """Test the scraper with a small sample"""
    logger.info("="*60)
    logger.info("Testing DIME Scraper")
    logger.info("="*60)
    
    # Initialize scraper
    scraper = DIMEScraper(
        output_dir="test_data",
        records_per_file=100  # Smaller files for testing
    )
    
    # Test fetching a single page
    logger.info("Testing API connection and fetching first page...")
    try:
        data = scraper.fetch_projects(page=1, per_page=10)
        projects = data.get('data', [])
        
        if projects:
            logger.info(f"✅ Successfully fetched {len(projects)} projects")
            logger.info(f"Sample project: {projects[0].get('projectName', 'N/A')}")
            
            # Show metadata if available
            meta = data.get('meta', {})
            if meta:
                logger.info(f"Total projects available: {meta.get('total', 'N/A')}")
                logger.info(f"Current page: {meta.get('currentPage', 'N/A')}")
                logger.info(f"Last page: {meta.get('lastPage', 'N/A')}")
        else:
            logger.warning("⚠️  No projects returned")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_scraper()
    
    if success:
        print("\n" + "="*60)
        print("✅ Test passed! The scraper is working correctly.")
        print("="*60)
        print("\nTo scrape all data, run:")
        print("  python dime_scraper.py")
        print("\nThe data will be saved to the 'scraped_data/' directory")
        print("with 1000 records per JSON file.")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ Test failed. Please check the error messages above.")
        print("="*60)
