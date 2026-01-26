"""
Demo website generator using Jinja2 templates.
"""
import os
import shutil
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Optional
from config import Config
from database import Database


class DemoGenerator:
    """Generate demo websites from templates."""
    
    def __init__(self):
        self.templates_dir = Config.TEMPLATES_DIR
        self.output_dir = Config.DEMO_OUTPUT_DIR
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Setup Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
    
    def select_template(self, business: Dict) -> str:
        """
        Select appropriate template based on business category.
        
        Returns:
            Template filename
        """
        category = business.get('category', '').lower()
        
        # Map categories to templates
        if any(keyword in category for keyword in ['restaurant', 'food', 'cafe', 'burger', 'pizza']):
            return 'restaurant.html'
        elif any(keyword in category for keyword in ['tech', 'repair', 'computer', 'phone', 'electronic']):
            return 'tech_repair.html'
        else:
            return 'service.html'
    
    def generate_demo(self, business: Dict, output_filename: str = None) -> str:
        """
        Generate a demo website for a business.
        
        Args:
            business: Business dictionary with all required fields
            output_filename: Custom output filename (optional)
        
        Returns:
            Path to generated demo file
        """
        # Select template
        template_name = self.select_template(business)
        template = self.env.get_template(template_name)
        
        # Prepare template variables
        context = {
            'business_name': business.get('name', 'Your Business'),
            'business_category': business.get('category', 'Business'),
            'location': business.get('location', ''),
            'address': business.get('address', ''),
            'phone': business.get('phone', ''),
            'rating': business.get('rating', 0.0),
            'review_count': business.get('review_count', 0),
            'website': business.get('website'),
            'google_maps_url': business.get('google_maps_url', '#'),
            'latitude': business.get('latitude'),
            'longitude': business.get('longitude'),
        }
        
        # Render template
        html_content = template.render(**context)
        
        # Generate output filename if not provided
        if not output_filename:
            safe_name = self._sanitize_filename(business.get('name', 'demo'))
            output_filename = f"{safe_name}.html"
        
        # Ensure .html extension
        if not output_filename.endswith('.html'):
            output_filename += '.html'
        
        # Write to file
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Copy CSS file to output directory
        css_source = os.path.join(self.templates_dir, 'styles.css')
        css_dest = os.path.join(self.output_dir, 'styles.css')
        if os.path.exists(css_source):
            shutil.copy2(css_source, css_dest)
        
        print(f"✅ Demo generated: {output_path}")
        return output_path
    
    def generate_and_save(self, business: Dict, db: Database = None) -> Dict:
        """
        Generate demo and optionally save to database.
        
        Returns:
            Dictionary with demo path and template info
        """
        template_used = self.select_template(business)
        demo_path = self.generate_demo(business)
        
        result = {
            'demo_path': demo_path,
            'template_used': template_used,
            'filename': os.path.basename(demo_path)
        }
        
        # Save to database if provided
        if db and 'id' in business:
            db.add_demo(
                business_id=business['id'],
                template=template_used,
                local_path=demo_path
            )
        
        return result
    
    def _sanitize_filename(self, name: str) -> str:
        """Convert business name to safe filename."""
        # Remove special characters
        safe = ''.join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in name)
        # Replace spaces with underscores
        safe = safe.replace(' ', '_')
        # Convert to lowercase
        safe = safe.lower()
        # Remove multiple underscores
        while '__' in safe:
            safe = safe.replace('__', '_')
        return safe[:50]  # Limit length
    
    def get_demo_url(self, demo_path: str) -> str:
        """
        Get a file:// URL for local demo viewing.
        
        In production, this would return a deployed URL (GitHub Pages, Vercel, etc.)
        """
        abs_path = os.path.abspath(demo_path)
        return f"file://{abs_path}"


if __name__ == '__main__':
    # Test demo generator
    print("Testing DemoGenerator...")
    
    generator = DemoGenerator()
    
    # Test business
    test_business = {
        'name': 'Test Restaurant',
        'category': 'restaurant',
        'location': 'Manchester UK',
        'address': '123 Test Street, Manchester M1 1AA',
        'phone': '+44 161 123 4567',
        'rating': 4.7,
        'review_count': 89,
        'google_maps_url': 'https://maps.google.com/?q=test',
        'latitude': 53.4808,
        'longitude': -2.2426
    }
    
    print(f"\n📝 Generating demo for: {test_business['name']}")
    print(f"   Category: {test_business['category']}")
    print(f"   Template: {generator.select_template(test_business)}")
    
    demo_path = generator.generate_demo(test_business)
    demo_url = generator.get_demo_url(demo_path)
    
    print(f"\n🌐 Demo URL: {demo_url}")
    print(f"\n💡 Open this URL in your browser to view the demo!")
    print(f"   Or run: open '{demo_path}'")
