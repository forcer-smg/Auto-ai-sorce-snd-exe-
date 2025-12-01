# Telegram Integration Setup Guide

## Overview

Telegram integration allows your desktop app to:
- Receive notifications via Telegram
- Sync settings between web and desktop versions
- Get automatic update notifications
- Register desktop installations

## Setup Steps

### 1. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Supabase Configuration (for settings sync)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key_here
```

### 2. Get Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy the bot token you receive
4. Set it as `TELEGRAM_BOT_TOKEN`

### 3. Get Chat ID

**Option A: Using Bot**
1. Start a chat with your bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find `"chat":{"id":123456789}` in the response
5. Use that number as `TELEGRAM_CHAT_ID`

**Option B: Using @userinfobot**
1. Search for `@userinfobot` in Telegram
2. Start a chat and send `/start`
3. It will show your chat ID

### 4. Configure Supabase (Optional but Recommended)

**For Settings Sync:**

1. Create a Supabase project at https://supabase.com
2. Get your project URL and API key
3. Create the following tables:

```sql
-- User settings table
CREATE TABLE user_settings (
    user_id BIGINT PRIMARY KEY,
    settings JSONB,
    desktop_version TEXT,
    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Desktop app registrations
CREATE TABLE desktop_registrations (
    user_id BIGINT,
    device_id TEXT,
    app_version TEXT,
    registered_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, device_id)
);
```

4. Set `SUPABASE_URL` and `SUPABASE_KEY` in environment

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `supabase>=2.0.0` (for settings sync)
- `requests` (already included)

### 6. Test Integration

Start the app and check console output:
- ✅ `Telegram bot integration enabled` - Success!
- ⚠️ `Telegram bot not configured` - Check environment variables

## API Endpoints

### Check Status
```bash
GET /api/telegram/status
```

### Send Notification
```bash
POST /api/telegram/send
{
    "message": "Your message here",
    "priority": "info"  # info, success, warning, error, update
}
```

### Check for Updates
```bash
GET /api/telegram/update-check
```

### Sync Settings
```bash
POST /api/settings/sync
{
    "user_id": 123456789,
    "settings": {
        "theme": "dark",
        "font_size": 14
    }
}
```

### Get Settings
```bash
GET /api/settings/get?user_id=123456789
```

### Register Desktop App
```bash
POST /api/desktop/register
{
    "user_id": 123456789,
    "device_id": "unique-device-id",
    "app_version": "1.0.0"
}
```

## GitHub Webhook Setup

### 1. Create Webhook in GitHub

1. Go to your repository: `SMG-Dawn/Auto-Punch-IDE-Desktop`
2. Settings → Webhooks → Add webhook
3. Payload URL: `https://your-app-url.com/webhook/github`
4. Content type: `application/json`
5. Events: Select "Releases"
6. Save webhook

### 2. Test Webhook

1. Create a test release on GitHub
2. Check webhook deliveries in GitHub settings
3. Verify notification sent to Telegram

## Telegram Bot Commands

Add these commands to your Telegram bot:

### `/desktop`
Get desktop app download link

### `/desktop-update`
Check for desktop app updates

### `/desktop-status`
Check desktop app integration status

### `/sync-settings`
Sync settings between web and desktop

## Integration with Existing Bot

If you already have a Telegram bot, add these commands:

```python
from telegram_commands import register_commands

# Register all desktop app commands
register_commands(your_bot)
```

Or add commands individually:

```python
from telegram_commands import (
    handle_desktop_command,
    handle_desktop_update_command,
    handle_desktop_status_command,
    handle_sync_settings_command
)

@bot.message_handler(commands=['desktop'])
def desktop_cmd(message):
    handle_desktop_command(bot, message)
```

## Usage Examples

### Send Notification from Desktop App

```python
from telegram_bot import telegram_bot

# Send simple notification
telegram_bot.send_notification(
    "Build Complete",
    "Your app has been built successfully!",
    priority="success"
)
```

### Check for Updates

```python
from telegram_bot import github_release

release = github_release.get_latest_release()
if release:
    assets = github_release.get_release_assets(release)
    print(f"Latest version: {assets['version']}")
```

### Sync Settings

```python
from telegram_bot import settings_sync

# Save settings
settings_sync.save_settings(
    user_id=123456789,
    settings={"theme": "dark", "font_size": 14}
)

# Get settings
settings = settings_sync.get_settings(user_id=123456789)
```

## Troubleshooting

### Bot Not Sending Messages
- Check `TELEGRAM_BOT_TOKEN` is correct
- Check `TELEGRAM_CHAT_ID` is correct
- Verify bot is started (send `/start` to bot)

### Settings Sync Not Working
- Check Supabase credentials
- Verify tables exist in Supabase
- Check network connectivity

### Webhook Not Triggering
- Verify webhook URL is accessible
- Check GitHub webhook deliveries
- Ensure "Releases" event is selected

## Next Steps

1. ✅ Configure environment variables
2. ✅ Test Telegram notifications
3. ✅ Set up GitHub webhook
4. ✅ Add commands to your bot
5. ✅ Test settings sync
6. ✅ Deploy and test end-to-end

## Support

For issues or questions:
- Check logs in console output
- Verify environment variables
- Test API endpoints manually
- Check Telegram bot status

