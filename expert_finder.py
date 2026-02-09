"""
Expert finder for non-Google Maps lead sources using LinkedIn X-Ray and Clutch.
"""
from serpapi import GoogleSearch
from typing import List, Dict
from config import Config
import urllib.parse


class ExpertFinder:
    """Find leads via LinkedIn X-Ray and specialized directories."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.SERPAPI_KEY
        if not self.api_key:
            raise ValueError("SerpApi key not found. Set SERPAPI_KEY in .env file")

    def linkedin_xray_search(self, role: str, industry: str, location: str = "", limit: int = 10) -> List[Dict]:
        """
        Search for specific professional roles using LinkedIn X-Ray.
        
        Args:
            role: Job title (e.g., "Bid Manager")
            industry: Industry for the firm (e.g., "Civil Engineering")
            location: Optional geographic focus
            limit: Number of results to return
        """
        print(f"🕵️  Running LinkedIn X-Ray for '{role}' in '{industry}'...")
        
        # Build X-Ray query
        # site:linkedin.com/in "Bid Manager" "Civil Engineering" "Manchester"
        query_parts = [f'site:linkedin.com/in', f'"{role}"', f'"{industry}"']
        if location:
            query_parts.append(f'"{location}"')
            
        search_query = " ".join(query_parts)
        
        params = {
            "q": search_query,
            "engine": "google",
            "api_key": self.api_key,
            "num": limit
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "error" in results:
                print(f"❌ API Error: {results['error']}")
                return []
            
            organic_results = results.get("organic_results", [])
            leads = []
            
            for result in organic_results:
                # Basic parsing of LinkedIn profile title: "Name - Job Title - Company | LinkedIn"
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                link = result.get('link', '')
                
                # Simple name extraction
                name = title.split(' - ')[0] if ' - ' in title else "Unknown"
                
                leads.append({
                    'name': name,
                    'category': industry,
                    'location': location or "LinkedIn",
                    'address': location or "Remote/LinkedIn",
                    'phone': '',  # Not easily extractable via search
                    'rating': 0.0,
                    'review_count': 0,
                    'website': link,
                    'website_status': 'social_only',
                    'google_maps_url': '',
                    'source': 'linkedin',
                    'notes': f"Title: {title}\nSnippet: {snippet}",
                    'lead_score': 90  # High score because it's a direct role match
                })
                
            print(f"✅ Found {len(leads)} LinkedIn profiles")
            return leads
            
        except Exception as e:
            print(f"❌ LinkedIn X-Ray failed: {str(e)}")
            return []

    def clutch_search(self, service_category: str, location: str = "", limit: int = 10) -> List[Dict]:
        """
        Find firms on Clutch directory (good for B2B specialized services).
        
        Args:
            service_category: e.g., "IT Services", "UX Design"
            location: geography focus
        """
        print(f"🔍 Searching Clutch Directory for '{service_category}' firms...")
        
        # Query for Clutch: site:clutch.co "service_category" "location"
        search_query = f'site:clutch.co/profile "{service_category}"'
        if location:
            search_query += f' "{location}"'
            
        params = {
            "q": search_query,
            "engine": "google",
            "api_key": self.api_key,
            "num": limit
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            organic_results = results.get("organic_results", [])
            leads = []
            
            for result in organic_results:
                title = result.get('title', '')
                link = result.get('link', '')
                snippet = result.get('snippet', '')
                
                # Parse Clutch title: "Company Name - Location - Reviews | Clutch.co"
                biz_name = title.split(' - ')[0].replace(' Reviews', '')
                
                leads.append({
                    'name': biz_name,
                    'category': service_category,
                    'location': location or "Clutch",
                    'address': "Check Clutch Profile",
                    'phone': '',
                    'rating': 0.0, # Could be parsed from title if needed
                    'review_count': 0,
                    'website': link,
                    'website_status': 'has_website',
                    'google_maps_url': '',
                    'source': 'clutch',
                    'notes': snippet,
                    'lead_score': 85
                })
                
            print(f"✅ Found {len(leads)} firms via Clutch")
            return leads
            
        except Exception as e:
            print(f"❌ Clutch search failed: {str(e)}")
            return []

if __name__ == '__main__':
    # Test
    finder = ExpertFinder()
    results = finder.linkedin_xray_search("Bid Manager", "IT Consulting", "UK", limit=3)
    for r in results:
        print(f"- {r['name']} ({r['source']})")
