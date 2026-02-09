# ProspectVantage: Growth System 🚀

**The ultimate lead generation ecosystem for discovering, validating, and converting high-intent business prospects.**

ProspectVantage streamlines the entire outreach lifecycle—from automated Google Maps discovery to AI-powered lead scoring and personalized demo generation.

---

## ✨ System Features

- **🔍 Unified Command Center**: A premium central dashboard to orchestrate all your lead generation engines.
- **⚡ Real-time Log Streaming**: Transparent, live processing visible directly in your browser.
- **✅ Validation Intelligence**: Multi-stage validation logic to identify the highest quality prospects.
- **🌐 Forge Demo Engine**: Automatically generate professionally designed demo sites for your leads.
- **📊 Adaptive Listing UI**: A high-scannability, row-based interface for deep-dive lead management.
- **🎯 Smart Scoring**: Rank prospects using 0-100 logic-driven Trust Scores.

---

## 🎯 Who Is This For?

- **Web Developers** selling website services
- **Digital Agencies** prospecting for clients
- **Freelancers** building their portfolio
- **Marketing Consultants** offering digital services

---

## 🚀 Deployment Guide

### 1. Environment Configuration

```bash
# Register with ProspectVantage local environment
cd "/Users/a1/Documents/office/AI-scripts and tools/find local business"
pip install -r requirements.txt

# Setup credentials
cp .env.example .env
# Edit .env and add your SerpApi key (https://serpapi.com)
```

### 2. Launching the System

Simply start the unified server to access the Command Center:

```bash
python server.py
```

### 3. Accessing the Dashboard

Open your browser and navigate to the local portal:
[**http://localhost:8000**](http://localhost:8000)

---

## 📁 Core Architecture

```
ProspectVantage/
├── server.py              # Unified API & UI Portal
├── dashboard.html         # Slate & Indigo Dashboard UI
├── pipeline.py            # Growth Orchestrator
├── business_finder.py     # Local Engine (Google Maps)
├── expert_finder.py       # High Fidelity Engine (LinkedIn/Clutch)
├── validator.py           # Intelligence & Scoring
├── demo_generator.py      # Forge Demo Engine
├── database.py            # Persistence Layer
├── config.py              # System Configuration
└── templates/             # UI Templates for Demos
```

---

## 📁 Project Structure

```
find local business/
├── config.py              # Configuration and settings
├── database.py            # SQLite database management
├── business_finder.py     # SerpApi Google Maps search
├── validator.py           # Business validation and scoring
├── demo_generator.py      # Website template renderer
├── outreach_tracker.py    # CRM and contact tracking
├── pipeline.py            # Main orchestrator (CLI)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment config template
├── .env                   # Your API keys (gitignored)
├── templates/             # Website templates
│   ├── styles.css         # Shared design system
│   ├── restaurant.html    # Restaurant template
│   ├── tech_repair.html   # Tech/repair template
│   └── service.html       # General service template
├── generated_demos/       # Output folder for demos
└── leads_database.db      # SQLite database (auto-created)
```

---

## 💡 Usage Examples

### Example 1: Find Tech Repair Shops

```bash
python pipeline.py \
  --category "computer repair" \
  --location "Manchester UK" \
  --limit 20 \
  --demos
```

**Output**: 
- Finds 20 computer repair shops
- Filters for 4.0+ stars, 20+ reviews, no website
- Generates demo websites for top 5
- Saves all leads to database

### Example 2: Multi-Location Restaurant Search

```bash
python pipeline.py \
  --category "restaurants" \
  --multi-location
```

Uses locations from `.env` file (Manchester, London, Birmingham, Austin, Portland)

### Example 3: Just Search (No Demos)

```bash
python pipeline.py \
  --category "barber" \
  --location "Austin TX" \
  --limit 15
```

---

## 🧪 Testing Individual Modules

### Test Configuration
```bash
python config.py
```

### Test Database
```bash
python database.py
```

### Test Business Finder
```bash
python business_finder.py
```

### Test Validator
```bash
python validator.py
```

### Test Demo Generator
```bash
python demo_generator.py
```

### Test Outreach Tracker
```bash
python outreach_tracker.py
```

---

## 📊 Working with the Database

### View Your Leads

Use any SQLite browser (e.g., [DB Browser for SQLite](https://sqlitebrowser.org/)):

```bash
# Open the database
open leads_database.db

# Or query from command line
sqlite3 leads_database.db "SELECT name, rating, phone FROM businesses ORDER BY lead_score DESC LIMIT 10;"
```

### Export to CSV

```python
from outreach_tracker import OutreachTracker

tracker = OutreachTracker()
tracker.export_leads_csv('my_leads.csv')
```

---

## 🎨 Demo Website Templates

Three professionally designed templates:

### 1. **Restaurant Template** (`restaurant.html`)
- Menu showcase
- Reviews section
- Click-to-call CTA
- Google Maps integration

### 2. **Tech Repair Template** (`tech_repair.html`)
- Emergency contact banner
- Services grid
- Trust badges
- Testimonials

### 3. **Service Template** (`service.html`)
- General purpose (barbers, plumbing, auto repair)
- Service area showcase
- Contact forms ready
- Professional design

All templates feature:
- ✨ Modern glassmorphism design
- 📱 Fully responsive (mobile-first)
- 🎨 Vibrant gradients and animations
- ⚡ Fast loading

---

## 📧 Outreach Workflow

### 1. Generate Message

```python
from outreach_tracker import OutreachTracker

tracker = OutreachTracker()
business = {...}  # Your business data

# Get personalized message
message = tracker.generate_outreach_message(business, 'initial')
print(message)
```

### 2. Log Contact

```python
tracker.log_contact(
    business_id=1,
    method='email',
    notes='Sent demo link'
)
```

### 3. Track Response

```python
tracker.update_response(
    outreach_id=1,
    status='interested',
    notes='Wants to schedule call'
)
```

---

## ⚙️ Configuration Options

Edit `.env` to customize:

```bash
# Quality thresholds
MIN_RATING=4.0          # Minimum Google rating
MIN_REVIEWS=20          # Minimum review count

# Search locations (comma-separated)
TARGET_LOCATIONS=Manchester UK,London UK,Birmingham UK

# Business categories (comma-separated)
TARGET_CATEGORIES=restaurants,tech repair,barber,plumbing
```

---

## 📈 Lead Scoring System

Leads are automatically scored 0-100 based on:

| Criteria | Points |
|----------|--------|
| Rating ≥ 4.0 | 20 |
| Reviews ≥ 20 | 20 |
| Rating ≥ 4.5 | +15 bonus |
| Reviews ≥ 100 | +20 bonus |
| No website | 25 |
| Social media only | 15 |

**85-100**: 🎯 Prime prospects  
**70-84**: ⭐ Good prospects  
**50-69**: 💼 Potential prospects  

---

## 🔍 API Costs

### SerpApi Pricing

- **Free Tier**: 250 searches/month (perfect for testing)
- **Starter**: $25/month = 1,000 searches
- **Developer**: $75/month = 5,000 searches

**Tip**: Each business category + location = 1 search

---

## 🚨 Troubleshooting

### "SERPAPI_KEY not set"
```bash
# Make sure you've created .env file
cp .env.example .env
# Then add your API key to .env
```

### "No results found"
- Try broader search terms ("restaurants" vs "italian restaurants")
- Verify location spelling ("Manchester UK" not "Manchester England")
- Check your SerpApi dashboard for quota

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

## 📝 Next Steps

1. **Get your API key**: Sign up at [serpapi.com](https://serpapi.com)
2. **Run your first search**: `python pipeline.py --category "restaurants" --location "your city" --limit 10`
3. **Review leads**: Open `leads_database.db` in a SQLite browser
4. **Generate demos**: Add `--demos` flag to your search
5. **Start outreach**: Use the generated messages and demo websites

---

## 🤝 Tips for Success

1. **Start local**: Search your own city first - easier to call/visit
2. **Focus on one niche**: Master restaurants before expanding
3. **Customize demos**: Edit templates to match each business
4. **Track everything**: Log every call, email, and response
5. **Follow up**: Businesses are busy - persistence pays off

---

## 📄 License

MIT License - feel free to use for commercial purposes

---

## 🙋 Support

Questions? Check:
- SerpApi documentation: https://serpapi.com/google-maps-api
- Python Jinja2 docs: https://jinja.palletsprojects.com/

---

**Happy prospecting! 🚀**
