"""
DIME Philippines Dashboard Data Scraper
Scrapes project data from the DIME (Digital Information for Monitoring and Evaluation) Philippines dashboard
and saves it to JSON files with 1000 records per file.
"""

import requests
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlencode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dime_scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class DIMEScraper:
    """Scraper for DIME Philippines Dashboard"""
    
    def __init__(self, base_url: str = "https://www.dime.gov.ph", 
                 output_dir: str = "scraped_data",
                 records_per_file: int = 1000):
        """
        Initialize the scraper
        
        Args:
            base_url: Base URL for the DIME API
            output_dir: Directory to save JSON files
            records_per_file: Number of records per JSON file
        """
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/v1/projects"
        self.output_dir = Path(output_dir)
        self.records_per_file = records_per_file
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
    def fetch_projects(self, status: Optional[str] = None, 
                      page: int = 1, 
                      per_page: int = 100,
                      sort_by: str = "cost",
                      sort_direction: str = "DESC") -> Dict:
        """
        Fetch projects from the API
        
        Args:
            status: Project status filter (e.g., "Completed", "Incomplete")
            page: Page number
            per_page: Records per page
            sort_by: Field to sort by
            sort_direction: Sort direction (ASC or DESC)
            
        Returns:
            JSON response from API
        """
        params = {
            'page': page,
            'perPage': per_page,
            'sortBy': sort_by,
            'sortDirection': sort_direction
        }
        
        if status:
            params['status'] = status
            params['statusName'] = status
            
        try:
            logger.info(f"Fetching page {page} (status: {status or 'All'})")
            response = self.session.get(self.api_endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page {page}: {e}")
            raise
            
    def scrape_all_projects(self, status: Optional[str] = None, 
                           per_page: int = 100,
                           max_retries: int = 3,
                           retry_delay: int = 5) -> List[Dict]:
        """
        Scrape all projects from the API with pagination
        
        Args:
            status: Project status filter
            per_page: Records per page
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
            
        Returns:
            List of all project records
        """
        all_projects = []
        page = 1
        total_pages = None
        
        while True:
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    data = self.fetch_projects(
                        status=status,
                        page=page,
                        per_page=per_page
                    )
                    
                    projects = data.get('data', [])
                    
                    if not projects:
                        logger.info(f"No more projects found at page {page}")
                        return all_projects
                    
                    all_projects.extend(projects)
                    logger.info(f"Retrieved {len(projects)} projects from page {page}. Total so far: {len(all_projects)}")
                    
                    # Check if there are more pages
                    pagination = data.get('meta', {})
                    if pagination:
                        total = pagination.get('total', 0)
                        current_page = pagination.get('currentPage', page)
                        last_page = pagination.get('lastPage', current_page)
                        
                        if total_pages is None:
                            total_pages = last_page
                            logger.info(f"Total pages to fetch: {total_pages}")
                        
                        if current_page >= last_page:
                            logger.info(f"Reached last page ({last_page})")
                            return all_projects
                    else:
                        # If no pagination metadata, check if we got fewer records than requested
                        if len(projects) < per_page:
                            logger.info(f"Retrieved fewer projects than requested, assuming last page")
                            return all_projects
                    
                    success = True
                    page += 1
                    
                    # Be respectful - add a small delay between requests
                    time.sleep(1)
                    
                except Exception as e:
                    retry_count += 1
                    logger.warning(f"Attempt {retry_count}/{max_retries} failed: {e}")
                    if retry_count < max_retries:
                        logger.info(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        logger.error(f"Failed to fetch page {page} after {max_retries} attempts")
                        # Return what we have so far
                        return all_projects
        
        return all_projects
    
    def save_projects_to_json(self, projects: List[Dict], prefix: str = "dime_projects"):
        """
        Save projects to JSON files, splitting into chunks
        
        Args:
            projects: List of project records
            prefix: Prefix for output filenames
        """
        total_projects = len(projects)
        logger.info(f"Saving {total_projects} projects to JSON files...")
        
        # Split into chunks
        num_files = (total_projects + self.records_per_file - 1) // self.records_per_file
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i in range(num_files):
            start_idx = i * self.records_per_file
            end_idx = min((i + 1) * self.records_per_file, total_projects)
            chunk = projects[start_idx:end_idx]
            
            filename = f"{prefix}_{timestamp}_part_{i+1:03d}_of_{num_files:03d}.json"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': {
                        'total_projects_in_file': len(chunk),
                        'file_number': i + 1,
                        'total_files': num_files,
                        'records_range': f"{start_idx + 1}-{end_idx}",
                        'total_projects': total_projects,
                        'scraped_at': timestamp,
                        'source': 'DIME Philippines Dashboard',
                        'url': self.base_url
                    },
                    'projects': chunk
                }, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(chunk)} projects to {filename}")
    
    def scrape_by_status(self, statuses: List[str] = None):
        """
        Scrape projects filtered by multiple statuses
        
        Args:
            statuses: List of status filters (e.g., ["Completed", "Incomplete"])
        """
        if statuses is None:
            statuses = [None]  # Will fetch all projects without filter
        
        for status in statuses:
            logger.info(f"{'='*60}")
            logger.info(f"Starting scrape for status: {status or 'All'}")
            logger.info(f"{'='*60}")
            
            try:
                projects = self.scrape_all_projects(status=status)
                
                if projects:
                    status_prefix = f"dime_projects_{status.lower()}" if status else "dime_projects_all"
                    self.save_projects_to_json(projects, prefix=status_prefix)
                    logger.info(f"Successfully scraped {len(projects)} projects with status: {status or 'All'}")
                else:
                    logger.warning(f"No projects found for status: {status or 'All'}")
                    
            except Exception as e:
                logger.error(f"Error scraping projects with status {status or 'All'}: {e}")
                continue
            
            # Wait a bit between different status queries
            if len(statuses) > 1:
                time.sleep(2)


def main():
    """Main execution function"""
    logger.info("="*60)
    logger.info("DIME Philippines Dashboard Data Scraper")
    logger.info("TARGET: Collect at least 10,000 project records")
    logger.info("="*60)
    
    # Initialize scraper
    scraper = DIMEScraper(
        output_dir="scraped_data",
        records_per_file=1000  # 1000 records per JSON file
    )
    
    # Scrape all projects without filter to get maximum data
    logger.info("Scraping ALL projects to reach 10,000+ records...")
    scraper.scrape_by_status(statuses=[None])
    
    logger.info("="*60)
    logger.info("Scraping completed!")
    logger.info(f"Check the 'scraped_data' directory for output files")
    logger.info(f"Each file contains up to 1,000 records")
    logger.info("="*60)


if __name__ == "__main__":
    main()
