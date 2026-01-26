"""
Outreach tracking and management system.
"""
from typing import Dict, List
from database import Database
from datetime import datetime, timedelta


class OutreachTracker:
    """Track outreach efforts and manage leads."""
    
    def __init__(self, db: Database = None):
        self.db = db or Database()
    
    def log_contact(self, business_id: int, method: str, notes: str = '') -> int:
        """
        Log an outreach attempt.
        
        Args:
            business_id: ID of the business contacted
            method: Contact method ('email', 'phone', 'whatsapp', 'in_person')
            notes: Additional notes about the contact
        
        Returns:
            Outreach record ID
        """
        outreach_id = self.db.add_outreach(business_id, method, notes)
        print(f"✅ Logged {method} outreach for business ID {business_id}")
        return outreach_id
    
    def update_response(self, outreach_id: int, status: str, notes: str = ''):
        """
        Update outreach with response information.
        
        Args:
            outreach_id: ID of the outreach record
            status: Response status ('interested', 'not_interested', 'callback', 'won', 'lost')
            notes: Response details
        """
        self.db.update_outreach_response(outreach_id, status, notes)
        print(f"✅ Updated outreach {outreach_id}: {status}")
    
    def get_contact_history(self, business_id: int) -> List[Dict]:
        """Get all outreach attempts for a business."""
        return self.db.get_outreach_history(business_id)
    
    def get_pending_followups(self, days_since_contact: int = 3) -> List[Dict]:
        """
        Get businesses that need follow-up.
        
        Args:
            days_since_contact: Number of days since last contact
        
        Returns:
            List of businesses needing follow-up
        """
        # This is a simplified version - in production, you'd want more sophisticated logic
        all_businesses = self.db.get_all_businesses()
        
        pending = []
        for business in all_businesses:
            history = self.get_contact_history(business['id'])
            
            if not history:
                # Never contacted
                pending.append({
                    **business,
                    'reason': 'Never contacted',
                    'days_since_contact': None
                })
            else:
                # Check if needs follow-up
                last_contact = history[0]  # Most recent
                if not last_contact['response_received']:
                    contact_date = datetime.fromisoformat(last_contact['contact_date'])
                    days_ago = (datetime.now() - contact_date).days
                    
                    if days_ago >= days_since_contact:
                        pending.append({
                            **business,
                            'reason': f'No response in {days_ago} days',
                            'days_since_contact': days_ago,
                            'last_method': last_contact['method']
                        })
        
        return pending
    
    def generate_outreach_message(self, business: Dict, template_type: str = 'initial') -> str:
        """
        Generate a personalized outreach message.
        
        Args:
            business: Business dictionary
            template_type: 'initial', 'followup', or 'demo'
        
        Returns:
            Personalized message text
        """
        name = business.get('name', 'there')
        category = business.get('category', 'business')
        location = business.get('location', '')
        rating = business.get('rating', 0)
        reviews = business.get('review_count', 0)
        
        if template_type == 'initial':
            return f"""Hi {name} team,

I noticed you have an impressive {rating}★ rating from {reviews} customers on Google - congratulations!

I also noticed you don't currently have a website. I'm a web developer specializing in {category} businesses, and I'd love to help you reach more customers online.

I've created a FREE demo website specifically for {name} to show you what your online presence could look like. Would you be interested in seeing it?

Best regards"""

        elif template_type == 'followup':
            return f"""Hi {name},

Following up on my previous message. I've built a demo website for {name} that showcases your {rating}★ rating and makes it easy for customers to find and contact you.

Would you like me to send you the link? No obligation - just wanted to show you what's possible.

Thanks!"""

        elif template_type == 'demo':
            return f"""Hi {name},

Here's the demo website I created for you:
[DEMO_LINK_HERE]

It includes:
• Your {rating}★ Google rating and {reviews} reviews
• Easy click-to-call button
• Google Maps integration
• Mobile-responsive design

Let me know what you think!

Best regards"""
        
        return ''
    
    def get_statistics(self) -> Dict:
        """Get outreach statistics."""
        stats = self.db.get_statistics()
        
        # Calculate response rate
        if stats['outreach_attempts'] > 0:
            stats['response_rate'] = (stats['responses_received'] / stats['outreach_attempts']) * 100
        else:
            stats['response_rate'] = 0
        
        return stats
    
    def export_leads_csv(self, filepath: str = 'leads_export.csv'):
        """Export leads to CSV for use in spreadsheets."""
        import csv
        
        businesses = self.db.get_all_businesses()
        
        if not businesses:
            print("⚠️ No businesses to export")
            return
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name', 'category', 'location', 'phone', 'rating', 
                         'review_count', 'website_status', 'lead_score', 'address']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for business in businesses:
                writer.writerow({k: business.get(k, '') for k in fieldnames})
        
        print(f"✅ Exported {len(businesses)} leads to {filepath}")


if __name__ == '__main__':
    # Test outreach tracker
    print("Testing OutreachTracker...")
    
    with Database() as db:
        tracker = OutreachTracker(db)
        
        # Add test business
        test_business = {
            'name': 'Test Restaurant',
            'category': 'restaurant',
            'location': 'Manchester UK',
            'phone': '+44 161 123 4567',
            'rating': 4.7,
            'review_count': 89,
            'address': '123 Test St',
            'website': None,
            'website_status': 'no_website',
            'google_maps_url': 'https://maps.google.com/test',
            'lead_score': 85
        }
        
        business_id = db.add_business(test_business)
        print(f"\n✅ Added test business (ID: {business_id})")
        
        # Test message generation
        print("\n📧 Initial outreach message:")
        print("-" * 60)
        message = tracker.generate_outreach_message(test_business, 'initial')
        print(message)
        print("-" * 60)
        
        # Test contact logging
        outreach_id = tracker.log_contact(business_id, 'email', 'Sent initial proposal')
        
        # Get statistics
        stats = tracker.get_statistics()
        print(f"\n📊 Statistics:")
        print(f"   Total businesses: {stats['total_businesses']}")
        print(f"   Outreach attempts: {stats['outreach_attempts']}")
        
        # Clean up
        db.clear_test_data()
        print("\n🧹 Test complete!")
