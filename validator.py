"""
Business validation and website detection logic.
"""
import requests
from typing import Dict, Optional
from urllib.parse import urlparse
from config import Config


class Validator:
    """Validate businesses against quality criteria."""
    
    def __init__(self):
        self.min_rating = Config.MIN_RATING
        self.min_reviews = Config.MIN_REVIEWS
        self.social_patterns = Config.SOCIAL_ONLY_PATTERNS
    
    def validate_business(self, business: Dict) -> Dict:
        """
        Validate a business against all criteria.
        
        Returns:
            Updated business dict with validation results
        """
        # Check rating
        rating_valid = self._check_rating(business.get('rating', 0))
        
        # Check review count
        reviews_valid = self._check_reviews(business.get('review_count', 0))
        
        # Check website status
        website_status = self.check_website(business.get('website'))
        
        # Calculate lead score (0-100)
        lead_score = self._calculate_lead_score(business, rating_valid, reviews_valid, website_status)
        
        # Determine if this is a valid lead
        is_valid_lead = (
            rating_valid and 
            reviews_valid and 
            website_status in ['no_website', 'social_only']
        )
        
        # Update business dict
        business['website_status'] = website_status
        business['lead_score'] = lead_score
        business['is_valid_lead'] = is_valid_lead
        business['validation_notes'] = self._get_validation_notes(
            rating_valid, reviews_valid, website_status
        )
        
        return business
    
    def _check_rating(self, rating: float) -> bool:
        """Check if rating meets minimum threshold."""
        return rating >= self.min_rating
    
    def _check_reviews(self, review_count: int) -> bool:
        """Check if review count meets minimum threshold."""
        return review_count >= self.min_reviews
    
    def check_website(self, website: Optional[str]) -> str:
        """
        Determine website status.
        
        Returns:
            'no_website', 'social_only', 'has_website', or 'broken'
        """
        if not website:
            return 'no_website'
        
        # Check if it's a social media URL
        parsed = urlparse(website.lower())
        domain = parsed.netloc or parsed.path
        
        for pattern in self.social_patterns:
            if pattern in domain:
                return 'social_only'
        
        # Check if website is accessible (optional - can be slow)
        # Uncomment if you want to verify website accessibility
        # if self._is_website_accessible(website):
        #     return 'has_website'
        # else:
        #     return 'broken'
        
        return 'has_website'
    
    def _is_website_accessible(self, url: str, timeout: int = 5) -> bool:
        """
        Check if a website is accessible (optional validation).
        
        Note: This makes HTTP requests and can slow down processing.
        Use only if you want to verify website accessibility.
        """
        try:
            # Ensure URL has a scheme
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            return response.status_code < 400
        except:
            return False
    
    def _calculate_lead_score(self, business: Dict, rating_valid: bool, 
                             reviews_valid: bool, website_status: str) -> int:
        """
        Calculate a lead score from 0-100.
        
        Higher score = better prospect
        """
        score = 0
        
        # Base points for meeting criteria
        if rating_valid:
            score += 20
        if reviews_valid:
            score += 20
        
        # Bonus points for excellent rating
        rating = business.get('rating', 0)
        if rating >= 4.5:
            score += 15
        elif rating >= 4.2:
            score += 10
        
        # Bonus points for high review count
        reviews = business.get('review_count', 0)
        if reviews >= 100:
            score += 20
        elif reviews >= 50:
            score += 15
        elif reviews >= 30:
            score += 10
        
        # Website status impact
        if website_status == 'no_website':
            score += 25  # Best prospects - no website at all
        elif website_status == 'social_only':
            score += 15  # Good prospects - only social media
        elif website_status == 'broken':
            score += 10  # Potential prospects - broken website
        else:
            score = 0  # Has working website - not a prospect
        
        return min(score, 100)
    
    def _get_validation_notes(self, rating_valid: bool, reviews_valid: bool, 
                             website_status: str) -> str:
        """Generate human-readable validation notes."""
        notes = []
        
        if not rating_valid:
            notes.append(f"Rating below {self.min_rating}")
        if not reviews_valid:
            notes.append(f"Reviews below {self.min_reviews}")
        
        status_messages = {
            'no_website': '🎯 No website - Prime prospect!',
            'social_only': '⭐ Social media only - Good prospect',
            'has_website': '❌ Has website - Not a prospect',
            'broken': '⚠️ Broken website - Potential prospect'
        }
        
        notes.append(status_messages.get(website_status, 'Unknown status'))
        
        return ' | '.join(notes)
    
    def filter_valid_leads(self, businesses: list[Dict]) -> list[Dict]:
        """
        Filter a list of businesses to only valid leads.
        
        Returns:
            List of validated businesses, sorted by lead score
        """
        validated = [self.validate_business(b) for b in businesses]
        valid_leads = [b for b in validated if b.get('is_valid_lead', False)]
        
        # Sort by lead score (highest first)
        valid_leads.sort(key=lambda x: x.get('lead_score', 0), reverse=True)
        
        return valid_leads


if __name__ == '__main__':
    # Test the validator
    print("Testing Validator...")
    
    validator = Validator()
    
    # Test cases
    test_businesses = [
        {
            'name': 'Great Restaurant',
            'rating': 4.5,
            'review_count': 50,
            'website': None
        },
        {
            'name': 'Tech Repair Shop',
            'rating': 4.7,
            'review_count': 100,
            'website': 'https://facebook.com/techrepair'
        },
        {
            'name': 'Low Rated Place',
            'rating': 3.5,
            'review_count': 30,
            'website': None
        },
        {
            'name': 'Has Website',
            'rating': 4.8,
            'review_count': 200,
            'website': 'https://example.com'
        }
    ]
    
    print("\n📋 Validation Results:")
    print("-" * 80)
    
    for business in test_businesses:
        validated = validator.validate_business(business)
        print(f"\n{validated['name']}")
        print(f"  Rating: {validated['rating']}★ | Reviews: {validated['review_count']}")
        print(f"  Website Status: {validated['website_status']}")
        print(f"  Lead Score: {validated['lead_score']}/100")
        print(f"  Valid Lead: {'✅ YES' if validated['is_valid_lead'] else '❌ NO'}")
        print(f"  Notes: {validated['validation_notes']}")
    
    print("\n" + "=" * 80)
    valid_leads = validator.filter_valid_leads(test_businesses)
    print(f"\n✅ Valid Leads Found: {len(valid_leads)}/{len(test_businesses)}")
    
    if valid_leads:
        print("\n🎯 Top Lead:")
        top = valid_leads[0]
        print(f"  {top['name']} (Score: {top['lead_score']}/100)")
