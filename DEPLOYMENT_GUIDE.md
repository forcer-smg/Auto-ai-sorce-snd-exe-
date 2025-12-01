# 🚀 Deployment Guide - Railway, cPanel, Supabase

## 📋 Overview

This guide shows how to deploy Auto_Punch IDE to:
- **Railway** (Recommended - Easy, auto-deploy from Git)
- **cPanel** (Traditional hosting)
- **Supabase** (Backend-as-a-Service with PostgreSQL)

## 🚂 Railway Deployment

### Step 1: Prepare Repository
```bash
# Ensure these files exist:
- railway.json
- Procfile
- requirements.txt
- app_server.py
```

### Step 2: Deploy to Railway

1. **Go to Railway.app** and sign in
2. **New Project** → **Deploy from GitHub repo**
3. **Select your repository**
4. **Railway will auto-detect** Python and deploy

### Step 3: Configure Environment Variables

In Railway dashboard, add:
```
PORT=5001
FLASK_ENV=production
HOST=0.0.0.0
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Step 4: Get Your URL

Railway provides: `https://your-app.railway.app`

### Step 5: Update Electron App

Update `electron/main.js` to use Railway URL:
```javascript
const FLASK_URL = process.env.FLASK_URL || 'https://your-app.railway.app';
```

## 🗄️ Supabase Deployment

### Step 1: Create Supabase Project

1. Go to **supabase.com**
2. **New Project**
3. Note your **URL** and **API keys**

### Step 2: Install Supabase Client

```bash
pip install supabase
```

### Step 3: Configure Environment

Add to `.env`:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
```

### Step 4: Use Supabase in App

```python
from supabase_config import get_supabase_client

supabase = get_supabase_client()
# Use Supabase for database, auth, storage, etc.
```

### Step 5: Deploy Backend

Deploy your Flask app to Railway/Heroku/cPanel and connect to Supabase.

## 📦 cPanel Deployment

### Step 1: Prepare Files

1. **Upload all files** via FTP/cPanel File Manager
2. **Structure:**
   ```
   public_html/
   ├── app.py
   ├── app_server.py
   ├── requirements.txt
   ├── templates/
   ├── static/
   └── .htaccess
   ```

### Step 2: Create .htaccess

```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ app_server.py/$1 [L]

# Python configuration
AddHandler fcgid-script .py
FCGIWrapper /usr/bin/python3 app_server.py
```

### Step 3: Setup Python App

1. **cPanel** → **Setup Python App**
2. **Python Version:** 3.11+
3. **App Directory:** `public_html`
4. **App File:** `app_server.py`
5. **Start Command:** `python app_server.py`

### Step 4: Install Dependencies

In cPanel Python App:
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

Add environment variables in cPanel Python App settings.

## 🔧 Update Electron App for Remote Server

### Option 1: Environment Variable

Update `electron/main.js`:
```javascript
// Get server URL from environment or use default
const FLASK_URL = process.env.FLASK_URL || 
                  process.env.RAILWAY_URL || 
                  'https://your-app.railway.app';

// Or use localhost for development
const isDev = process.env.NODE_ENV === 'development';
const FLASK_URL = isDev 
  ? 'http://localhost:5001'
  : 'https://your-app.railway.app';
```

### Option 2: Configuration File

Create `electron/config.json`:
```json
{
  "serverUrl": "https://your-app.railway.app",
  "useLocalServer": false
}
```

Load in `main.js`:
```javascript
const config = require('./config.json');
const FLASK_URL = config.useLocalServer 
  ? 'http://localhost:5001'
  : config.serverUrl;
```

## 📝 Environment Configuration

### For Local Development:
```env
FLASK_ENV=development
PORT=5001
HOST=localhost
```

### For Production (Railway/Supabase):
```env
FLASK_ENV=production
PORT=5001
HOST=0.0.0.0
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_key
```

## 🔐 Security Considerations

1. **CORS Configuration:**
   ```python
   CORS(app, origins=[
       "https://yourdomain.com",
       "https://your-app.railway.app"
   ])
   ```

2. **Environment Variables:**
   - Never commit `.env` to Git
   - Use Railway/cPanel environment variables
   - Keep secrets secure

3. **HTTPS:**
   - Railway provides HTTPS automatically
   - cPanel: Use Let's Encrypt SSL
   - Supabase: Always uses HTTPS

## 🚀 Quick Deploy Commands

### Railway:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Git Push (Auto-deploy):
```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
# Railway auto-deploys on push
```

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] Dependencies in requirements.txt
- [ ] Database configured (if using Supabase)
- [ ] CORS configured for your domain
- [ ] SSL/HTTPS enabled
- [ ] Electron app updated with server URL
- [ ] Tested locally first
- [ ] Error handling configured

## 📚 Resources

- **Railway:** https://railway.app/docs
- **Supabase:** https://supabase.com/docs
- **cPanel Python:** https://docs.cpanel.net/knowledge-base/python-apps/

## 🎯 Recommended Setup

**Best for Auto_Punch IDE:**
1. **Backend:** Railway (easy deployment)
2. **Database:** Supabase (PostgreSQL + Auth)
3. **Frontend:** Electron app connects to Railway URL

This gives you:
- ✅ Easy deployment
- ✅ Auto-scaling
- ✅ Database + Auth
- ✅ HTTPS included
- ✅ Free tier available


