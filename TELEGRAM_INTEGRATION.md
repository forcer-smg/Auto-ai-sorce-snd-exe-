# Telegram Bot Integration Guide

## Current Setup

Your Telegram bot is connected to:
- **GitHub Repo:** `SMG-Dawn/Auto-pounch-ai`
- **Railway:** Auto-deploys on push
- **Supabase:** Database and storage

## Integration Strategy

### Option 1: Separate Repos (Recommended)
- **Web Version:** Current repo (`Auto-pounch-ai`) → Railway
- **Desktop Version:** New repo (`Auto-Punch-IDE-Desktop`) → GitHub Releases

### Option 2: Monorepo
- Single repo with branches/folders
- More complex but unified

## Telegram Bot Commands

### Current Commands (Keep)
- `/start` - Welcome message
- `/help` - Show help
- `/status` - Check bot status
- `/deploy` - Trigger deployment

### New Commands (Add)
- `/desktop` - Get desktop app download link
- `/desktop-version` - Check desktop app version
- `/desktop-update` - Check for desktop updates
- `/sync-settings` - Sync settings between web and desktop
- `/notify-update` - Notify users of new desktop version

## Implementation

### 1. Update Telegram Bot

Add to your bot's command handler:

```python
@bot.command('desktop')
def desktop_command(message):
    """Get desktop app download link"""
    latest_release = get_latest_github_release('SMG-Dawn/Auto-Punch-IDE-Desktop')
    reply = f"""
🖥️ **Auto_Punch IDE Desktop**

📦 **Latest Version:** {latest_release['version']}
📥 **Download:**
• MSI Installer: {latest_release['msi_url']}
• EXE Installer: {latest_release['exe_url']}

💡 The desktop app runs locally without a browser!
    """
    bot.reply_to(message, reply, parse_mode='Markdown')

@bot.command('desktop-update')
def desktop_update_command(message):
    """Check for desktop app updates"""
    current_version = get_user_desktop_version(message.from_user.id)
    latest_version = get_latest_github_release('SMG-Dawn/Auto-Punch-IDE-Desktop')
    
    if current_version < latest_version['version']:
        reply = f"🆕 Update available! Version {latest_version['version']} is ready."
    else:
        reply = "✅ You're on the latest version!"
    
    bot.reply_to(message, reply)
```

### 2. GitHub Release Webhook

Set up webhook in GitHub:
1. Go to repo settings → Webhooks
2. Add webhook: `https://your-telegram-bot.railway.app/webhook/github`
3. Events: Releases

### 3. Webhook Handler

```python
@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """Handle GitHub release webhook"""
    data = request.json
    
    if data.get('action') == 'published':
        release = data.get('release', {})
        version = release.get('tag_name')
        
        # Notify all users with desktop app
        notify_desktop_users(version, release.get('html_url'))
    
    return jsonify({'status': 'ok'})
```

### 4. Supabase Integration

Store user preferences:
```python
# Sync settings
def sync_settings(user_id, settings):
    supabase.table('user_settings').upsert({
        'user_id': user_id,
        'settings': settings,
        'updated_at': datetime.now()
    })

# Get settings
def get_user_settings(user_id):
    result = supabase.table('user_settings').select('*').eq('user_id', user_id).execute()
    return result.data[0]['settings'] if result.data else {}
```

## Update Notification Flow

1. **Developer releases new version** on GitHub
2. **GitHub webhook triggers** → Telegram bot
3. **Bot checks Supabase** for desktop app users
4. **Bot sends notification** to all desktop users
5. **Desktop app checks for updates** (on startup or manually)
6. **User approves update** → Auto-install

## Settings Sync

### Web → Desktop
- User changes settings in web version
- Settings saved to Supabase
- Desktop app checks Supabase on startup
- Desktop app applies settings

### Desktop → Web
- User changes settings in desktop app
- Settings saved to Supabase
- Web version loads settings from Supabase

## Database Schema (Supabase)

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

## Testing

1. **Test bot commands:**
   - `/desktop` - Should return download links
   - `/desktop-update` - Should check version

2. **Test webhook:**
   - Create test release on GitHub
   - Verify webhook triggers
   - Check notifications sent

3. **Test sync:**
   - Change settings in web
   - Verify saved to Supabase
   - Check desktop app loads settings

## Deployment

### Update Bot Code
1. Add new commands to bot
2. Deploy to Railway
3. Test commands
4. Set up GitHub webhook

### Monitor
- Check webhook deliveries in GitHub
- Monitor bot logs in Railway
- Verify Supabase connections


