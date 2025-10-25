# API Setup Guide

Complete guide for setting up all required APIs for the AI Agent GUI.

---

## Table of Contents
1. [OpenAI API (Sora 2)](#openai-api-sora-2)
2. [Google Gemini API](#google-gemini-api)
3. [YouTube Data API v3](#youtube-data-api-v3)
4. [Cost Breakdown](#cost-breakdown)
5. [Security Best Practices](#security-best-practices)

---

## OpenAI API (Sora 2)

### Step 1: Create OpenAI Account

1. Visit [platform.openai.com](https://platform.openai.com/)
2. Click "Sign Up" (or "Log In" if you have an account)
3. Complete the registration process
4. Verify your email address

### Step 2: Add Payment Method

1. Navigate to **Settings** → **Billing**
2. Click **Add payment method**
3. Enter your payment information
4. Set up usage limits (recommended: $10-50/month to start)

### Step 3: Request Sora Access

**Important**: Sora may be in limited beta access.

1. Check [openai.com/sora](https://openai.com/sora) for current status
2. Join the waitlist if available
3. Wait for approval email

### Step 4: Create API Key

1. Go to **API Keys** section
2. Click **Create new secret key**
3. Name it: "AI Agent GUI"
4. Copy the key immediately (you won't see it again!)
5. Paste it in the AI Agent GUI Settings tab

### Step 5: Test the API

```python
from openai import OpenAI
client = OpenAI(api_key="your-key-here")

# Test with a simple request
# (Sora API endpoints may vary)
```

### Troubleshooting

- **Error: "Invalid API Key"**: Verify you copied the complete key
- **Error: "Insufficient quota"**: Add payment method or increase limits
- **Error: "Model not found"**: Check if you have Sora API access

---

## Google Gemini API

### Step 1: Access Google AI Studio

1. Visit [ai.google.dev](https://ai.google.dev/)
2. Click **Sign in** with your Google account
3. Accept the terms of service

### Step 2: Create API Key

1. Click **Get API Key** button
2. Select **Create API key in new project** (or use existing)
3. Copy the API key
4. Paste it in the AI Agent GUI Settings tab

### Step 3: Test the API

```python
import google.generativeai as genai

genai.configure(api_key="your-key-here")
model = genai.GenerativeModel('gemini-2.5-flash')

# Test
response = model.generate_content("Hello!")
print(response.text)
```

### Free Tier Limits

- **Gemini 2.5 Flash**: 
  - 15 requests per minute
  - 1 million tokens per minute
  - 1,500 requests per day
  - Free tier available!

### Troubleshooting

- **Error: "API Key invalid"**: Check you copied the full key (starts with "AIza")
- **Error: "Quota exceeded"**: Wait for rate limit reset or upgrade to paid plan
- **Error: "Model not available"**: Verify you're using "gemini-2.5-flash"

---

## YouTube Data API v3

This is the most complex setup but essential for automated uploads.

### Step 1: Create Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click **Select a project** → **New Project**
4. Name: "AI Agent YouTube"
5. Click **Create**

### Step 2: Enable YouTube Data API v3

1. In the Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for "YouTube Data API v3"
3. Click on it
4. Click **Enable**

### Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (unless you have a Google Workspace)
3. Click **Create**

**Fill in the form:**
- App name: "AI Agent GUI"
- User support email: Your email
- Developer contact: Your email
- Click **Save and Continue**

**Scopes:**
- Click **Add or Remove Scopes**
- Search for "YouTube"
- Select: `https://www.googleapis.com/auth/youtube.upload`
- Click **Update**
- Click **Save and Continue**

**Test users:**
- Click **Add Users**
- Add your Gmail address
- Click **Save and Continue**

### Step 4: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: "AI Agent Desktop"
5. Click **Create**
6. Click **Download JSON**
7. Save the file

### Step 5: Rename and Place Credentials

1. Rename downloaded file to `client_secrets.json`
2. Move it to the `ai_agent_gui` folder
3. **Never share this file publicly!**

### Step 6: First Time Authentication

1. Run the AI Agent GUI
2. Try to upload a video (or test YouTube connection)
3. A browser window will open
4. Sign in with the Google account associated with your YouTube channel
5. Click **Allow** to grant permissions
6. The app will create `token.pickle` for future use

### YouTube API Quotas

**Free Tier:**
- 10,000 units per day
- Each video upload: ~1,600 units
- Allows ~6 uploads per day
- Quota resets at midnight Pacific Time

**If you need more:**
- Apply for quota increase in Google Cloud Console
- Or use multiple projects

### Troubleshooting

- **Error: "client_secrets.json not found"**: Check file is in ai_agent_gui folder
- **Error: "OAuth error"**: Delete token.pickle and re-authenticate
- **Error: "Quota exceeded"**: Wait until midnight PT or request increase
- **Error: "Insufficient permissions"**: Add youtube.upload scope in OAuth consent screen

---

## Cost Breakdown

### Monthly Cost Estimates

**Scenario 1: Light Use (3 videos/week)**
- OpenAI Sora: ~$30-60/month (varies by video length)
- Google Gemini: $0 (free tier sufficient)
- YouTube API: $0 (free tier sufficient)
- **Total: ~$30-60/month**

**Scenario 2: Regular Use (1 video/day)**
- OpenAI Sora: ~$100-200/month
- Google Gemini: $0 (free tier sufficient)
- YouTube API: $0 (free tier sufficient)
- **Total: ~$100-200/month**

**Scenario 3: Heavy Use (Multiple videos/day)**
- OpenAI Sora: ~$300-500/month
- Google Gemini: ~$10-20/month (may exceed free tier)
- YouTube API: $0 (may need quota increase)
- **Total: ~$310-520/month**

**Note**: Sora pricing is estimated as the API is not fully public yet. Actual costs may vary.

---

## Security Best Practices

### 1. API Key Storage

✅ **DO:**
- Store keys in `settings.json` (gitignored)
- Use environment variables for production
- Rotate keys regularly

❌ **DON'T:**
- Commit keys to version control
- Share keys in screenshots
- Use the same key across multiple apps

### 2. OAuth Credentials

✅ **DO:**
- Keep `client_secrets.json` private
- Store `token.pickle` securely
- Use separate projects for development/production

❌ **DON'T:**
- Share OAuth credentials
- Commit credentials to Git
- Use production credentials for testing

### 3. Monitoring

- Enable billing alerts in OpenAI dashboard
- Monitor Google Cloud billing
- Set up quota alerts
- Review API usage regularly

### 4. Access Control

- Use least-privilege principle
- Create service accounts for automation
- Enable 2FA on all accounts
- Regularly audit access logs

---

## API Testing Checklist

Before running the full workflow, test each API:

- [ ] OpenAI API responds successfully
- [ ] Gemini generates text correctly
- [ ] YouTube authentication completes
- [ ] Test video upload succeeds
- [ ] All quotas are within limits
- [ ] Billing alerts are configured

---

## Quick Reference

### OpenAI API
- **Dashboard**: [platform.openai.com](https://platform.openai.com/)
- **Docs**: [platform.openai.com/docs](https://platform.openai.com/docs)
- **Pricing**: [openai.com/pricing](https://openai.com/pricing)

### Google Gemini API
- **Dashboard**: [ai.google.dev](https://ai.google.dev/)
- **Docs**: [ai.google.dev/docs](https://ai.google.dev/docs)
- **Pricing**: [ai.google.dev/pricing](https://ai.google.dev/pricing)

### YouTube Data API
- **Console**: [console.cloud.google.com](https://console.cloud.google.com/)
- **Docs**: [developers.google.com/youtube/v3](https://developers.google.com/youtube/v3)
- **Quota**: [console.cloud.google.com/apis/api/youtube.googleapis.com/quotas](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)

---

## Support

If you encounter issues:

1. Check the [README.md](README.md) troubleshooting section
2. Review API documentation
3. Check your quotas and billing
4. Verify credentials are correctly placed
5. Check application logs in the Logs tab

---

**Important**: Always review each API's terms of service and acceptable use policies before automating content creation and uploads.

