"""
Utility script to analyze scraped JSON files
Shows statistics about the scraped data
"""

import json
import os
from pathlib import Path
from collections import Counter

def analyze_scraped_data(data_dir="scraped_data"):
    """Analyze all JSON files in the scraped data directory"""
    
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"❌ Directory '{data_dir}' not found!")
        print(f"Run the scraper first: python dime_scraper.py")
        return
    
    json_files = list(data_path.glob("**/*.json"))
    
    if not json_files:
        print(f"❌ No JSON files found in '{data_dir}'")
        return
    
    print("="*60)
    print(f"📊 Analysis of Scraped Data in '{data_dir}'")
    print("="*60)
    
    total_projects = 0
    statuses = Counter()
    regions = Counter()
    implementing_offices = Counter()
    source_of_funds = Counter()
    total_cost = 0
    
    for json_file in sorted(json_files):
        print(f"\n📄 Processing: {json_file.name}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            projects = data.get('projects', [])
            metadata = data.get('metadata', {})
            
            print(f"   Projects in file: {len(projects)}")
            
            if metadata:
                print(f"   File {metadata.get('file_number', '?')} of {metadata.get('total_files', '?')}")
            
            for project in projects:
                total_projects += 1
                
                # Count statuses
                status = project.get('status', 'Unknown')
                statuses[status] += 1
                
                # Count regions
                region = project.get('region', 'Unknown')
                regions[region] += 1
                
                # Count implementing offices
                offices = project.get('implementingOffices', [])
                for office in offices:
                    office_name = office.get('name', 'Unknown')
                    implementing_offices[office_name] += 1
                
                # Count source of funds
                funds = project.get('sourceOfFunds', [])
                for fund in funds:
                    fund_name = fund.get('name', 'Unknown')
                    source_of_funds[fund_name] += 1
                
                # Sum costs
                cost = project.get('cost', 0) or 0
                total_cost += cost
                
        except Exception as e:
            print(f"   ⚠️  Error processing file: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("📈 SUMMARY STATISTICS")
    print("="*60)
    
    print(f"\n📁 Total JSON files: {len(json_files)}")
    print(f"📊 Total projects: {total_projects:,}")
    print(f"💰 Total cost: ₱{total_cost:,.2f}")
    
    print(f"\n📍 By Status:")
    for status, count in statuses.most_common():
        percentage = (count / total_projects * 100) if total_projects > 0 else 0
        print(f"   {status}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n🗺️  Top 10 Regions:")
    for region, count in regions.most_common(10):
        percentage = (count / total_projects * 100) if total_projects > 0 else 0
        print(f"   {region}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n🏢 Top 10 Implementing Offices:")
    for office, count in implementing_offices.most_common(10):
        print(f"   {office}: {count:,}")
    
    print(f"\n💵 Top 5 Sources of Funds:")
    for fund, count in source_of_funds.most_common(5):
        print(f"   {fund}: {count:,}")
    
    print("\n" + "="*60)

def main():
    import sys
    
    # Check if custom directory provided
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = "scraped_data"
    
    analyze_scraped_data(data_dir)

if __name__ == "__main__":
    main()
