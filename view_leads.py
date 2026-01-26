"""
Simple leads viewer - displays leads in terminal and generates HTML report.
"""
import argparse
from database import Database
from datetime import datetime


def view_leads_terminal(limit=None):
    """Display leads in clean terminal format."""
    db = Database()
    businesses = db.get_all_businesses(limit=limit)
    
    if not businesses:
        print("\n⚠️  No leads found in database.")
        print("💡 Run: python pipeline.py -c 'barber shops' -l 'Manchester UK' --limit 20\n")
        return
    
    print(f"\n{'='*80}")
    print(f"📋 LEADS REPORT - {len(businesses)} Total")
    print(f"{'='*80}\n")
    
    for idx, biz in enumerate(businesses, 1):
        print(f"{idx}. {biz['name']}")
        print(f"   📍 Location: {biz['address']}")
        print(f"   ⭐ Rating: {biz['rating']}★ ({biz['review_count']} reviews)")
        print(f"   📞 Phone: {biz['phone']}")
        print(f"   🌐 Website: {biz['website_status'].replace('_', ' ').title()}")
        print(f"   🎯 Lead Score: {biz['lead_score']}/100")
        print(f"   🗺️  Google Maps: {biz['google_maps_url']}")
        print()
    
    print(f"{'='*80}")
    print(f"\n💡 Tip: Click the Google Maps links above to verify each business")
    print(f"💡 Or run: python view_leads.py --html (opens in browser)\n")


def generate_html_report():
    """Generate HTML report with clickable links."""
    db = Database()
    businesses = db.get_all_businesses()
    
    if not businesses:
        print("\n⚠️  No leads found in database.\n")
        return None
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Leads Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            background: white;
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        h1 {{
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .stats {{
            color: #64748b;
            font-size: 1.125rem;
        }}
        
        .leads-grid {{
            display: grid;
            gap: 1.5rem;
        }}
        
        .lead-card {{
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .lead-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
        }}
        
        .lead-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1.5rem;
        }}
        
        .lead-name {{
            color: #1e293b;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .lead-score {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1.125rem;
        }}
        
        .lead-info {{
            display: grid;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
        }}
        
        .info-row {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1rem;
            color: #475569;
        }}
        
        .info-row .emoji {{
            font-size: 1.25rem;
            width: 24px;
        }}
        
        .rating {{
            color: #f59e0b;
            font-weight: 600;
        }}
        
        .status {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 50px;
            font-size: 0.875rem;
            font-weight: 600;
        }}
        
        .status.no-website {{
            background: #dcfce7;
            color: #166534;
        }}
        
        .status.social-only {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .actions {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #5568d3;
            transform: translateY(-2px);
        }}
        
        .btn-secondary {{
            background: #f1f5f9;
            color: #475569;
        }}
        
        .btn-secondary:hover {{
            background: #e2e8f0;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .lead-header {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 Business Leads Report</h1>
            <p class="stats">{len(businesses)} leads found • Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </header>
        
        <div class="leads-grid">
"""
    
    for idx, biz in enumerate(businesses, 1):
        status_class = biz['website_status'].replace('_', '-')
        status_text = biz['website_status'].replace('_', ' ').title()
        
        html += f"""
            <div class="lead-card">
                <div class="lead-header">
                    <div>
                        <div class="lead-name">{idx}. {biz['name']}</div>
                        <span class="status {status_class}">🌐 {status_text}</span>
                    </div>
                    <div class="lead-score">🎯 {biz['lead_score']}/100</div>
                </div>
                
                <div class="lead-info">
                    <div class="info-row">
                        <span class="emoji">📍</span>
                        <span>{biz['address']}</span>
                    </div>
                    <div class="info-row">
                        <span class="emoji">⭐</span>
                        <span class="rating">{biz['rating']}★ ({biz['review_count']} reviews)</span>
                    </div>
                    <div class="info-row">
                        <span class="emoji">📞</span>
                        <span><a href="tel:{biz['phone']}" style="color: #667eea; text-decoration: none;">{biz['phone']}</a></span>
                    </div>
                </div>
                
                <div class="actions">
                    <a href="{biz['google_maps_url']}" target="_blank" class="btn btn-primary">
                        🗺️ View on Google Maps
                    </a>
                    <a href="tel:{biz['phone']}" class="btn btn-secondary">
                        📞 Call Now
                    </a>
                </div>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML file
    filename = f"leads_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='View business leads')
    parser.add_argument('--html', action='store_true', help='Generate HTML report and open in browser')
    parser.add_argument('--limit', type=int, help='Limit number of leads to show')
    
    args = parser.parse_args()
    
    if args.html:
        print("\n🌐 Generating HTML report...")
        filename = generate_html_report()
        if filename:
            print(f"✅ Report saved: {filename}")
            
            # Open in browser
            import subprocess
            subprocess.run(['open', filename])
            print(f"🚀 Opening in browser...\n")
    else:
        view_leads_terminal(args.limit)
