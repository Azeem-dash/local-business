"""
Main pipeline orchestrator - end-to-end automation.
"""
import argparse
from typing import List, Dict
from config import Config
from database import Database
from business_finder import BusinessFinder
from expert_finder import ExpertFinder
from validator import Validator
from demo_generator import DemoGenerator
from outreach_tracker import OutreachTracker


class Pipeline:
    """Main automation pipeline."""
    
    def __init__(self):
        self.config = Config
        self.db = Database()
        self.finder = BusinessFinder()
        self.expert_finder = ExpertFinder()
        self.validator = Validator()
        self.demo_gen = DemoGenerator()
        self.tracker = OutreachTracker(self.db)
    
    def run(self, category: str, location: str, limit: int = 20, 
            generate_demos: bool = False, search_id: int = None) -> Dict:
        """
        Execute the full pipeline.
        
        Args:
            category: Business category to search
            location: Location to search in
            limit: Maximum number of results
            generate_demos: Whether to generate demo websites
        
        Returns:
            Summary statistics
        """
        print(f"\n{'='*80}")
        print(f"🚀 BUSINESS LEAD AUTOMATION PIPELINE")
        print(f"{'='*80}\n")
        
        # Step 1: Search for businesses
        print(f"Step 1: Searching for '{category}' in '{location}'...")
        businesses = self.finder.search(category, location, limit)
        
        if not businesses:
            print("❌ No businesses found")
            return {'error': 'No businesses found'}
        
        # Step 2: Validate businesses
        print(f"\nStep 2: Validating {len(businesses)} businesses...")
        valid_leads = self.validator.filter_valid_leads(businesses)
        
        print(f"✅ Found {len(valid_leads)} valid leads\n")
        
        if not valid_leads:
            print("⚠️ No valid leads found after filtering")
            return {'businesses_found': len(businesses), 'valid_leads': 0, 'engine': 'google_maps'}
        
        # Step 3: Save to database
        print(f"Step 3: Saving to database...")
        saved_count = 0
        for business in valid_leads:
            try:
                if search_id:
                    business['search_id'] = search_id
                business_id = self.db.add_business(business)
                business['id'] = business_id
                saved_count += 1
            except Exception as e:
                print(f"⚠️ Error saving {business.get('name')}: {e}")
        
        print(f"✅ Saved {saved_count} leads to database\n")
        
        # Step 4: Generate demos (optional)
        demos_generated = 0
        if generate_demos:
            print(f"Step 4: Generating demo websites...")
            for business in valid_leads[:5]:  # Limit to top 5 for demo
                try:
                    demo_info = self.demo_gen.generate_and_save(business, self.db)
                    demos_generated += 1
                    print(f"   ✅ {business['name']}: {demo_info['filename']}")
                except Exception as e:
                    print(f"   ⚠️ Error generating demo for {business.get('name')}: {e}")
            print()
        
        # Step 5: Display summary
        print(f"{'='*80}")
        print(f"📊 PIPELINE SUMMARY")
        print(f"{'='*80}\n")
        
        summary = {
            'businesses_found': len(businesses),
            'valid_leads': len(valid_leads),
            'saved_to_db': saved_count,
            'demos_generated': demos_generated,
            'top_leads': valid_leads[:5],
            'engine': 'google_maps'
        }
        
        print(f"Total businesses found: {summary['businesses_found']}")
        print(f"Valid leads:  {summary['valid_leads']}")
        print(f"Saved to database: {summary['saved_to_db']}")
        if generate_demos:
            print(f"Demos generated: {summary['demos_generated']}")
        
        # Display top leads
        print(f"\n🎯 TOP LEADS (by score):")
        print(f"{'='*80}")
        for idx, lead in enumerate(summary['top_leads'], 1):
            print(f"\n{idx}. {lead['name']}")
            print(f"   📍 {lead['location']}")
            print(f"   ⭐ {lead['rating']}★ ({lead['review_count']} reviews)")
            print(f"   📞 {lead['phone']}")
            print(f"   🎯 Score: {lead['lead_score']}/100")
            print(f"   📝 {lead.get('validation_notes', '')}")
        
        print(f"\n{'='*80}")
        print(f"✅ Pipeline complete!")
        print(f"{'='*80}\n")
        
        return summary

    def run_expert_search(self, search_type: str, query: str, industry: str = "", 
                          location: str = "", limit: int = 10, search_id: int = None) -> Dict:
        """
        Run specialized search for experts/firms (LinkedIn or Clutch).
        """
        print(f"\n{'='*80}")
        print(f"🚀 SPECIALIZED LEAD SEARCH: {search_type.upper()}")
        print(f"{'='*80}\n")
        
        if search_type == 'linkedin':
            leads = self.expert_finder.linkedin_xray_search(query, industry, location, limit)
        elif search_type == 'clutch':
            leads = self.expert_finder.clutch_search(query, location, limit)
        else:
            print(f"❌ Unknown search type: {search_type}")
            return {'error': 'Unknown search type'}

        if not leads:
            print("❌ No leads found")
            return {'error': 'No leads found'}
            
        # These are usually high quality, but we can still validate
        print(f"\nStep 2: Validating {len(leads)} leads...")
        valid_leads = self.validator.filter_valid_leads(leads)
        
        print(f"Step 3: Saving to database...")
        saved_count = 0
        for lead in valid_leads:
            try:
                # Expert finder results already have 'source'
                if search_id:
                    lead['search_id'] = search_id
                lead_id = self.db.add_business(lead)
                lead['id'] = lead_id
                saved_count += 1
            except Exception as e:
                print(f"⚠️ Error saving {lead.get('name')}: {e}")
                
        print(f"✅ Saved {saved_count} leads from {search_type} to database\n")
        return {
            'leads_found': len(leads), 
            'valid_leads': len(valid_leads),
            'saved_to_db': saved_count,
            'engine': search_type
        }
    
    def run_multi_location(self, category: str, locations: List[str] = None, 
                          limit_per_location: int = 10, generate_demos: bool = False) -> Dict:
        """Run pipeline across multiple locations."""
        locations = locations or Config.get_location_list()
        
        all_results = []
        for location in locations:
            print(f"\n\n{'#'*80}")
            print(f"# Processing: {location}")
            print(f"{'#'*80}")
            
            result = self.run(category, location, limit_per_location, False)
            all_results.append(result)
        
        # Optionally generate demos for top leads across all locations
        if generate_demos:
            print(f"\n{'='*80}")
            print(f"Generating demos for top leads...")
            print(f"{'='*80}\n")
            
            all_leads = self.db.get_all_businesses(limit=10)
            for lead in all_leads:
                try:
                    self.demo_gen.generate_and_save(lead, self.db)
                except Exception as e:
                    print(f"⚠️ Error: {e}")
        
        return {'locations_processed': len(locations), 'results': all_results}
    
    def close(self):
        """Clean up resources."""
        self.db.close()


def main():
    """CLI interface for the pipeline."""
    parser = argparse.ArgumentParser(
        description='Business Lead Automation Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for restaurants in Manchester
  python pipeline.py --category "restaurants" --location "Manchester UK" --limit 10
  
  # Search with demo generation
  python pipeline.py --category "tech repair" --location "Austin TX" --demos
  
  # Search across all configured locations
  python pipeline.py --category "barber" --multi-location
        """
    )
    
    parser.add_argument('--category', '-c', required=True, help='Business category to search')
    parser.add_argument('--location', '-l', help='Location to search in')
    parser.add_argument('--limit', type=int, default=20, help='Max results per search')
    parser.add_argument('--demos', action='store_true', help='Generate demo websites')
    parser.add_argument('--multi-location', action='store_true', help='Search across all configured locations')
    parser.add_argument('--linkedin', action='store_true', help='Search LinkedIn profiles')
    parser.add_argument('--clutch', action='store_true', help='Search Clutch directory')
    parser.add_argument('--industry', help='Industry for LinkedIn search')
    
    args = parser.parse_args()
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"\n❌ Configuration Error:\n{e}\n")
        print("💡 Setup instructions:")
        print("1. Copy .env.example to .env")
        print("2. Get a free API key from https://serpapi.com")
        print("3. Add your API key to .env file")
        return
    
    # Run pipeline
    pipeline = Pipeline()
    
    try:
        if args.linkedin:
            if not args.category or not args.industry:
                print("❌ Error: --category (Role) and --industry are required for LinkedIn search")
                return
            pipeline.run_expert_search('linkedin', args.category, args.industry, args.location, args.limit)
        elif args.clutch:
            if not args.category:
                print("❌ Error: --category is required for Clutch search")
                return
            pipeline.run_expert_search('clutch', args.category, location=args.location, limit=args.limit)
        elif args.multi_location:
            pipeline.run_multi_location(args.category, generate_demos=args.demos)
        else:
            if not args.location:
                print("❌ Error: --location is required (or use --multi-location/--linkedin/--clutch)")
                return
            
            pipeline.run(args.category, args.location, args.limit, args.demos)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Pipeline interrupted by user")
    
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        raise
    
    finally:
        pipeline.close()


if __name__ == '__main__':
    main()
