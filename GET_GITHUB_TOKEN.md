# How to Get GitHub Personal Access Token

## Step-by-Step Guide

### Step 1: Go to GitHub Settings
1. Open your browser and go to: **https://github.com**
2. Make sure you're logged in as **SMG-Dawn**
3. Click your **profile picture** (top right corner)
4. Click **Settings**

### Step 2: Navigate to Developer Settings
1. In the left sidebar, scroll down to the bottom
2. Click **Developer settings**

### Step 3: Go to Personal Access Tokens
1. In the left sidebar, click **Personal access tokens**
2. Click **Tokens (classic)** (or just "Tokens" if that's the only option)

### Step 4: Generate New Token
1. Click the **"Generate new token"** button
2. Select **"Generate new token (classic)"** (if you see both options)

### Step 5: Configure Token
Fill in the form:

1. **Note** (name for the token):
   ```
   Auto_Punch IDE
   ```
   (This helps you remember what the token is for)

2. **Expiration**:
   - Choose how long the token should last
   - Options: 7 days, 30 days, 90 days, or **No expiration**
   - For development, you can choose **No expiration** or **90 days**

3. **Select scopes** (permissions):
   - ✅ Check **`repo`** - This gives full control of private repositories
   - This is the most important one for pushing to private repos
   - You can also check:
     - ✅ `workflow` (if you use GitHub Actions)
     - ✅ `write:packages` (if you publish packages)

### Step 6: Generate and Copy Token
1. Scroll down and click **"Generate token"** button (green button at bottom)
2. **IMPORTANT:** GitHub will show you the token **ONCE**
3. **Copy the token immediately** - it looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
4. **Save it somewhere safe** - you won't be able to see it again!

### Step 7: Use the Token
When you push to GitHub and it asks for password:
- **Username:** `SMG-Dawn`
- **Password:** **Paste your Personal Access Token** (NOT your GitHub password)

## Quick Link
Direct link to create token: **https://github.com/settings/tokens/new**

## Security Tips
1. ✅ **Never share your token** - treat it like a password
2. ✅ **Don't commit tokens to Git** - they're in `.gitignore` already
3. ✅ **Revoke old tokens** if you think they're compromised
4. ✅ **Use different tokens** for different projects if needed

## Troubleshooting

### "Token has expired"
- Generate a new token with longer expiration

### "Bad credentials"
- Make sure you're using the **token** as password, not your GitHub password
- Check that the token has `repo` scope

### "Permission denied"
- Make sure the token has `repo` scope checked
- Verify you're using the correct username: `SMG-Dawn`

## Alternative: Use GitHub CLI
If you prefer command line:
```bash
# Install GitHub CLI first, then:
gh auth login
```

But Personal Access Token is easier for most users.

