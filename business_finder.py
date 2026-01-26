"""
Business search using SerpApi Google Maps integration.
"""
from serpapi import GoogleSearch
from typing import List, Dict, Optional
from config import Config


class BusinessFinder:
    """Search for local businesses using SerpApi."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.SERPAPI_KEY
        if not self.api_key:
            raise ValueError("SerpApi key not found. Set SERPAPI_KEY in .env file")
    
    def search(self, query: str, location: str, limit: int = 20) -> List[Dict]:
        """
        Search for businesses matching query in a specific location.
        
        Args:
            query: Search term (e.g., "restaurants", "tech repair")
            location: Location string (e.g., "Manchester UK", "Austin TX")
            limit: Maximum number of results to return
        
        Returns:
            List of business dictionaries with parsed data
        """
        print(f"🔍 Searching for '{query}' in '{location}'...")
        
        # Combine query and location for SerpApi Google Maps
        search_query = f"{query} in {location}"
        
        params = {
            "engine": "google_maps",
            "q": search_query,
            "type": "search",
            "api_key": self.api_key,
            "num": min(limit, 20)  # SerpApi max per request
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "error" in results:
                print(f"❌ API Error: {results['error']}")
                return []
            
            local_results = results.get("local_results", [])
            
            if not local_results:
                print(f"⚠️ No results found for '{query}' in '{location}'")
                return []
            
            # Parse and normalize results
            businesses = []
            for result in local_results[:limit]:
                business = self._parse_business(result, query, location)
                businesses.append(business)
            
            print(f"✅ Found {len(businesses)} businesses")
            return businesses
        
        except Exception as e:
            print(f"❌ Search failed: {str(e)}")
            return []
    
    def _parse_business(self, result: Dict, category: str, location: str) -> Dict:
        """Parse a single business result from SerpApi."""
        
        # Get place_id for Google Maps link
        place_id = result.get('place_id', '')
        
        # Build Google Maps URL
        # Priority: 1. Direct link 2. Place ID 3. Coordinates 4. Search query
        google_maps_url = result.get('link', '')
        
        if not google_maps_url and place_id:
            # Build URL from place_id
            google_maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        elif not google_maps_url:
            # Fallback: build search URL from name and address
            name = result.get('title', '')
            address = result.get('address', '')
            if name and address:
                import urllib.parse
                query = f"{name} {address}"
                encoded_query = urllib.parse.quote(query)
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        
        # Extract basic info
        business = {
            'name': result.get('title', 'Unknown'),
            'category': category,
            'location': location,
            'address': result.get('address', ''),
            'phone': result.get('phone', ''),
            'rating': result.get('rating', 0.0),
            'review_count': result.get('reviews', 0),
            'website': result.get('website'),
            'google_maps_url': google_maps_url,
            'latitude': result.get('gps_coordinates', {}).get('latitude'),
            'longitude': result.get('gps_coordinates', {}).get('longitude'),
            'place_id': place_id,
            'type': result.get('type', ''),
            'hours': result.get('hours', ''),
        }
        
        return business
    
    def search_multiple_locations(self, query: str, locations: List[str], limit_per_location: int = 10) -> List[Dict]:
        """
        Search across multiple locations.
        
        Args:
            query: Search term
            locations: List of location strings
            limit_per_location: Max results per location
        
        Returns:
            Combined list of all businesses found
        """
        all_businesses = []
        
        for location in locations:
            businesses = self.search(query, location, limit_per_location)
            all_businesses.extend(businesses)
        
        print(f"\n📊 Total found across all locations: {len(all_businesses)}")
        return all_businesses
    
    def search_multiple_categories(self, categories: List[str], location: str, limit_per_category: int = 10) -> List[Dict]:
        """
        Search for multiple business categories in one location.
        
        Args:
            categories: List of business types to search
            location: Location string
            limit_per_category: Max results per category
        
        Returns:
            Combined list of all businesses found
        """
        all_businesses = []
        
        for category in categories:
            businesses = self.search(category, location, limit_per_category)
            all_businesses.extend(businesses)
        
        print(f"\n📊 Total found across all categories: {len(all_businesses)}")
        return all_businesses


if __name__ == '__main__':
    # Test the business finder
    print("Testing BusinessFinder...")
    
    try:
        finder = BusinessFinder()
        
        # Test single search
        results = finder.search('restaurants', 'Manchester UK', limit=5)
        
        if results:
            print(f"\n📋 Sample result:")
            sample = results[0]
            print(f"  Name: {sample['name']}")
            print(f"  Rating: {sample['rating']}★")
            print(f"  Reviews: {sample['review_count']}")
            print(f"  Phone: {sample['phone']}")
            print(f"  Website: {sample['website']}")
            print(f"  Address: {sample['address']}")
        
    except ValueError as e:
        print(f"❌ {e}")
        print("\n💡 To fix this:")
        print("1. Copy .env.example to .env")
        print("2. Sign up at https://serpapi.com (free tier: 250 searches/month)")
        print("3. Add your API key to .env file")
