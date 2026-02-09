"""
Configuration management for business lead automation pipeline.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for the pipeline."""
    
    # API Keys
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    VERCEL_TOKEN = os.getenv('VERCEL_TOKEN')
    
    # Database - Support for Turso (Cloud SQLite)
    TURSO_DATABASE_URL = os.getenv('TURSO_DATABASE_URL')
    TURSO_AUTH_TOKEN = os.getenv('TURSO_AUTH_TOKEN')
    
    # Search Parameters
    MIN_RATING = float(os.getenv('MIN_RATING', '4.0'))
    MIN_REVIEWS = int(os.getenv('MIN_REVIEWS', '20'))
    
    # Target locations (default if not in .env)
    TARGET_LOCATIONS = os.getenv(
        'TARGET_LOCATIONS',
        'Manchester UK,London UK,Birmingham UK,Austin TX,Portland OR'
    ).split(',')
    
    # Business categories
    TARGET_CATEGORIES = os.getenv(
        'TARGET_CATEGORIES',
        'restaurants,tech repair,barber,plumbing,auto repair'
    ).split(',')
    
    # Website blacklist patterns (social media only = no real website)
    SOCIAL_ONLY_PATTERNS = [
        'facebook.com',
        'instagram.com',
        'twitter.com',
        'linkedin.com',
        'tiktok.com',
        'youtube.com'
    ]
    
    # Database
    DATABASE_PATH = 'leads_database.db'
    
    # Templates
    TEMPLATES_DIR = 'templates'
    
    # Demo deployment
    DEMO_OUTPUT_DIR = 'generated_demos'
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        errors = []
        
        if not cls.SERPAPI_KEY:
            errors.append("SERPAPI_KEY not set in .env file")
        
        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(f"- {e}" for e in errors))
        
        return True
    
    @classmethod
    def get_location_list(cls):
        """Get cleaned list of target locations."""
        return [loc.strip() for loc in cls.TARGET_LOCATIONS]
    
    @classmethod
    def get_category_list(cls):
        """Get cleaned list of target categories."""
        return [cat.strip() for cat in cls.TARGET_CATEGORIES]


if __name__ == '__main__':
    # Test configuration
    try:
        Config.validate()
        print("✅ Configuration valid!")
        print(f"Min Rating: {Config.MIN_RATING}")
        print(f"Min Reviews: {Config.MIN_REVIEWS}")
        print(f"Locations: {Config.get_location_list()}")
        print(f"Categories: {Config.get_category_list()}")
    except ValueError as e:
        print(f"❌ {e}")
