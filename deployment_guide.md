# Deployment Guide: Vantage (100% Free)

Your Vantage system is now configured for **100% free cloud deployment**!

## ✅ What's Already Done

1.  **Turso Database Created**: `prospect-vantage-db` 
    - **URL**: `libsql://prospect-vantage-db-azeem-dash.aws-ap-northeast-1.turso.io`
    - **All your local data migrated** (370 businesses, 28 searches, 6 demos)

2.  **Security Files Created**:
    - ✅ `.gitignore` created (prevents `.env` from being committed)
    - ✅ `.env` removed from Git tracking

> **🚨 CRITICAL SECURITY NOTE**: 
> The `.env` file contains sensitive credentials and should **NEVER** be committed to Git!
> I've removed it from tracking and created a `.gitignore` to protect it.
> You'll add these variables directly in Render's dashboard instead.

## 🚀 Final Deployment Steps (Render)

Since the Render CLI doesn't support creating new services from scratch, you'll need to use the Render Dashboard for the initial setup. Here's how:

### Step 1: Push to GitHub

First, initialize a git repository and push your code:

```bash
cd "/Users/a1/Documents/office/AI-scripts and tools/find local business"
git init
git add .
git commit -m "Initial commit: Vantage system"
# Create a new repository on GitHub, then:
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Create Render Service

1.  Go to [Render Dashboard](https://dashboard.render.com/)
2.  Click **"New +"** → **"Web Service"**
3.  Connect your GitHub repository
4.  Configure the service:
    - **Name**: `prospect-vantage`
    - **Root Directory**: Leave empty (or set to `find local business` if you keep the folder structure)
    - **Environment**: `Python`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `python server.py`
    - **Instance Type**: `Free`

### Step 3: Add Environment Variables

In the Render service settings, add these environment variables:

```
SERPAPI_KEY=4a4063a7ff24990d1810d8d9dd2e5d6d69718d300f4523926e1a9c3b5f609935
TURSO_DATABASE_URL=libsql://prospect-vantage-db-azeem-dash.aws-ap-northeast-1.turso.io
TURSO_AUTH_TOKEN=eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NzA2NDQxNTQsImlkIjoiZDM0MTVlZGYtNzFjYy00MTY1LTg3OWUtYzdlM2YxZjQ0ODk2IiwicmlkIjoiODEwNDAyMDEtNmVmYi00OTBmLTlmMDQtNDFmZTM1ZGY5YWM5In0.IIInFVSHYEirLY-BdoFXc5_lxru9C5Vg9vZhGJHjnyf4CzYjM-2oeE3YpCN0r82rOsmgIm1p5qWBA8zQq2vTCQ
MIN_RATING=4.0
MIN_REVIEWS=20
```

### Step 4: Deploy

Click **"Create Web Service"** and Render will automatically build and deploy your application!

---

## 🔒 Security Reminder

Your app is protected by the **Access Gateway** (Code: `5354`). When you visit your Render URL, enter the code to unlock the system.

## 🎉 Going Live

Once the Render build completes (usually 2-3 minutes), your app will be online at:
`https://prospect-vantage.onrender.com` (or your custom chosen name)

Your leads will be permanently stored in the Turso cloud database, surviving all Render restarts!
