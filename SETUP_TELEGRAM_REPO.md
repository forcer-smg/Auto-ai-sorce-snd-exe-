# Setup Telegram Integration Repository

## Overview

The Telegram integration will be in a **separate repository** for:
- Independent deployment to Railway
- Separate versioning and updates
- Easier maintenance
- Isolated configuration

## Repository Structure

```
telegram-integration/
├── telegram_bot.py          # Telegram bot class
├── telegram_commands.py      # Bot commands
├── app.py                    # Flask app for webhooks (minimal)
├── requirements.txt          # Python dependencies
├── railway.json              # Railway deployment config
├── .env.example              # Environment variables template
└── README.md                 # Documentation
```

## Setup Steps

### 1. Create New Private Repository

```powershell
# Using GitHub CLI
gh repo create Auto-Punch-IDE-Telegram --private --description "Telegram integration for Auto_Punch IDE"

# Or create via web: https://github.com/new
```

### 2. Copy Telegram Files

Files to copy from main repo:
- `telegram_bot.py`
- `telegram_commands.py`
- `requirements.txt` (or create minimal one)

### 3. Create Minimal Flask App

Create `app.py` for Railway webhooks:

```python
from flask import Flask, request, jsonify
from telegram_bot import telegram_bot, github_release, settings_sync

app = Flask(__name__)

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """Handle GitHub release webhooks"""
    data = request.json
    
    if data.get('action') == 'published':
        release = data.get('release', {})
        version = release.get('tag_name', '')
        download_url = release.get('html_url', '')
        changelog = release.get('body', '')
        
        if telegram_bot.enabled:
            telegram_bot.notify_update(version, download_url, changelog)
        
        return jsonify({'status': 'ok', 'notified': telegram_bot.enabled})
    
    return jsonify({'status': 'ok'})

@app.route('/api/telegram/status', methods=['GET'])
def telegram_status():
    """Check Telegram bot status"""
    return jsonify({
        'enabled': telegram_bot.enabled,
        'configured': bool(telegram_bot.bot_token and telegram_bot.chat_id)
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check for Railway"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

### 4. Create Railway Configuration

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 5. Create Requirements

Create `requirements.txt`:

```txt
flask==3.0.0
requests==2.31.0
python-telegram-bot==20.7
supabase-py==2.0.0
python-dotenv==1.0.0
```

### 6. Environment Variables (Railway)

Set these in Railway dashboard:

```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GITHUB_REPO=SMG-Dawn/Auto-Punch-IDE  # Main repo to watch
```

### 7. Deploy to Railway

```powershell
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

Or use Railway web interface:
1. Connect GitHub repo
2. Set environment variables
3. Deploy

### 8. Configure GitHub Webhook

1. Go to main repo: `https://github.com/YOUR_USERNAME/Auto-Punch-IDE/settings/hooks`
2. Add webhook:
   - URL: `https://your-railway-app.railway.app/webhook/github`
   - Content type: `application/json`
   - Events: `Releases`
   - Secret: (optional, add to Railway env vars)

## Integration Points

### From Main Repo
- GitHub releases trigger webhooks
- Webhooks call Railway endpoint
- Railway bot sends Telegram notifications

### To Main Repo
- Telegram bot can check for updates
- Settings sync via Supabase
- Desktop app registration

## Testing

### Test Webhook Locally

```powershell
# Run Flask app
python app.py

# Test webhook (in another terminal)
curl -X POST http://localhost:5000/webhook/github `
  -H "Content-Type: application/json" `
  -d '{"action":"published","release":{"tag_name":"v1.0.0","html_url":"https://github.com/...","body":"Release notes"}}'
```

### Test Telegram Bot

```python
from telegram_bot import telegram_bot

# Test notification
telegram_bot.send_notification("Test", "This is a test", "info")
```

## Maintenance

### Update Telegram Integration

```powershell
# In telegram-integration repo
git pull origin main
# Make changes
git add .
git commit -m "Update integration"
git push origin main
# Railway auto-deploys
```

### Update Main Repo

```powershell
# In main repo
# Make changes, build, push
# GitHub webhook triggers Telegram notification
```

## Benefits of Separate Repo

1. ✅ Independent deployment
2. ✅ Separate versioning
3. ✅ Easier to maintain
4. ✅ Can update without touching main repo
5. ✅ Isolated environment variables
6. ✅ Separate scaling/configuration

## Files to Extract

From main repo, copy these to telegram repo:
- `telegram_bot.py` - Full file
- `telegram_commands.py` - Full file
- Relevant parts of `app.py` (webhook handlers)
- `requirements.txt` - Minimal version

## Next Steps

1. Create telegram-integration repo
2. Copy files
3. Set up Railway
4. Configure webhooks
5. Test integration
6. Deploy

