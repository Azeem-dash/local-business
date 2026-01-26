# Quick Start Guide - Simple Workflow

## 🚀 Get Started in 3 Steps

### Step 1: Get API Key (5 minutes)
1. Go to https://serpapi.com
2. Sign up (free - 250 searches/month)
3. Copy your API key from dashboard
4. Add to `.env` file: `SERPAPI_KEY=your_key_here`

### Step 2: Find Leads
```bash
# Search for businesses
python pipeline.py --category "barber shops" --location "Manchester UK" --limit 20
```

### Step 3: View Leads
```bash
# Terminal view
python view_leads.py

# Browser view (clickable links!)
python view_leads.py --html
```

---

## 📋 Simple Workflow

### 1. Search for Businesses
```bash
# Find barber shops
python pipeline.py -c "barber shops" -l "Birmingham UK" --limit 20

# Find auto repair
python pipeline.py -c "auto repair" -l "London UK" --limit 15

# Find restaurants
python pipeline.py -c "restaurants" -l "Leeds UK" --limit 10
```

This saves qualified leads (4+ stars, 20+ reviews, no website) to the database.

### 2. View Your Leads

**In Terminal:**
```bash
python view_leads.py
```

**In Browser (Better!):**
```bash
python view_leads.py --html
```

This opens a beautiful HTML report with:
- ✅ All business details
- 🗺️ **Clickable Google Maps links**
- 📞 Click-to-call phone numbers
- 🎯 Lead scores

### 3. Manually Verify & Contact

1. **Click the Google Maps link** → Verify business exists
2. **Check their current presence** → Confirm no website
3. **Look at reviews** → Read what customers say
4. **Call or visit** → Make your pitch!

---

## 📊 Example Output

After running `python view_leads.py --html`, you'll see:

```
1. Victors cuts Unisex
   📍 Location: 25 Union St, Birmingham
   ⭐ Rating: 5.0★ (443 reviews)
   📞 Phone: +44 7480 484558
   🌐 Website: No Website
   🎯 Score: 100/100
   
   [View on Google Maps] [Call Now]
```

---

## 🎯 Tips for Success

1. **Search multiple locations** - More leads = More opportunities
2. **Check Google Maps first** - Verify before calling
3. **Focus on high scores** - 90-100 = Best prospects
4. **Look for "No Website"** - Easier conversion than "Social Only"
5. **Call during business hours** - Higher connect rate

---

## 🔄 Typical Workflow

```bash
# Morning: Find new leads
python pipeline.py -c "nail salons" -l "Manchester UK" --limit 20

# View in browser
python view_leads.py --html

# Click through each Google Maps link
# Verify business exists and has no website
# Call or visit the top 5

# Repeat with different categories/locations
```

---

## 📞 When You Call

**Simple pitch:**
> "Hi, I saw your great reviews on Google (4.8 stars!) and noticed you don't have a website. I'm a web developer and I'd love to help you get more customers online. Do you have 2 minutes to chat?"

---

## 💡 Quick Commands Reference

| Command | What it does |
|---------|-------------|
| `python pipeline.py -c "barber" -l "London UK"` | Find leads |
| `python view_leads.py` | Terminal view |
| `python view_leads.py --html` | Browser view |
| `python view_leads.py --limit 5` | Show top 5 only |

---

## ✨ What Makes This Simple

✅ **No automatic demos** - You control everything  
✅ **Clean output** - Easy to read and use  
✅ **Clickable links** - One click to verify  
✅ **Manual verification** - Check before reaching out  
✅ **Your workflow** - Search → View → Verify → Contact

---

**That's it! Simple, manual, and effective.** 🎉
