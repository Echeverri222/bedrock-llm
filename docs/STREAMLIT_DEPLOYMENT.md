# 📱 Deploy Streamlit Documentation Interface

Deploy the interactive API documentation interface to Streamlit Cloud.

## Prerequisites

- GitHub repository (already have it ✅)
- Streamlit Cloud account (free)

## Step-by-Step Deployment

### 1. Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Continue with GitHub"
3. Authorize Streamlit Cloud

### 2. Deploy New App

1. Click "New app"
2. Fill in:
   - **Repository:** `Echeverri222/bedrock-llm`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
3. Click "Advanced settings" before deploying

### 3. Configure Secrets (Important!)

In the "Secrets" section, paste:

```toml
API_URL = "https://web-production-a2ec4d.up.railway.app"

# Optional: Pre-configure token for easy testing
# API_TOKEN = "your-token-here"
```

**Note:** The API URL is already set to your Railway production API. Users will need to paste their own token in the sidebar.

### 4. Deploy!

Click "Deploy!" button. Streamlit will:
- Clone your repository
- Install dependencies from `requirements.txt`
- Start the app

**Build time:** ~2-3 minutes

### 5. Get Your URL

Your app will be available at:
```
https://echeverri222-bedrock-llm.streamlit.app
```

Or similar (Streamlit generates the URL based on your repo name)

### 6. Share Your Documentation

Now you have three public URLs:

1. **🔒 Production API:** https://web-production-a2ec4d.up.railway.app
2. **📖 Swagger Docs:** https://web-production-a2ec4d.up.railway.app/docs
3. **📱 Interactive Docs:** https://your-app.streamlit.app

## 🔧 Configuration

### Default API URL

The Streamlit app is pre-configured to use your Railway API:
```python
API_URL = "https://web-production-a2ec4d.up.railway.app"
```

### For Local Development

To test locally with localhost API:

1. Edit sidebar in Streamlit
2. Change API URL to: `http://localhost:8000`
3. Or set environment variable:
   ```bash
   export API_URL="http://localhost:8000"
   streamlit run streamlit_app.py
   ```

## 🔄 Automatic Updates

Every time you push to GitHub `main` branch, Streamlit Cloud automatically:
1. Detects the changes
2. Rebuilds the app
3. Redeploys (takes ~1-2 minutes)

## 🎨 Customization

### Update Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

Push to GitHub and Streamlit will auto-update.

### Update Content

Edit `streamlit_app.py` and push to GitHub. Changes appear automatically.

## 📊 Monitoring

### View Logs

1. Go to your app on Streamlit Cloud
2. Click "Manage app" (bottom right)
3. View logs, metrics, and errors

### Check Status

- **Green:** App is running
- **Yellow:** Building/restarting
- **Red:** Error (check logs)

## 🆘 Troubleshooting

### App Won't Start

**Check logs for errors:**
- Missing dependencies → Check `requirements.txt`
- Import errors → Check file paths
- Module not found → Verify package versions

### API Connection Fails

**Verify secrets are set:**
1. Manage app → Settings → Secrets
2. Ensure `API_URL` is correct
3. Test API URL in browser: https://web-production-a2ec4d.up.railway.app/docs

### Token Authentication Fails

**Common issues:**
- Token has extra spaces → Trim whitespace
- Wrong token → Verify in `.env` on Railway
- Token not set → Add in sidebar

## 🔐 Security

### What's Public

✅ **Public (Safe):**
- API documentation interface
- Code examples
- Endpoint descriptions

❌ **NOT Public:**
- API Token (users must enter their own)
- AWS credentials (stay on Railway)
- Actual data (requires valid token)

### Sharing Access

To give someone API access:
1. Generate a new API token (rotate the existing one)
2. Share the token securely (not in public channels)
3. They can use it in the Streamlit interface or directly via API

## 💰 Cost

**Streamlit Cloud:**
- **Free:** Unlimited public apps
- **Pro:** $7/month for private apps

Your documentation interface is free on Streamlit Cloud! 🎉

## 🚀 Production Setup

Your complete production stack:

```
┌─────────────────────────────────────────┐
│  Streamlit Cloud (Free)                 │
│  https://your-app.streamlit.app         │
│  📱 Interactive API Documentation       │
└─────────────┬───────────────────────────┘
              │
              ▼ API Calls with Token
┌─────────────────────────────────────────┐
│  Railway ($5-20/month)                  │
│  https://web-production-a2ec4d...       │
│  🔒 Secure REST API                     │
└─────────────┬───────────────────────────┘
              │
              ▼ Queries S3 & Bedrock
┌─────────────────────────────────────────┐
│  AWS                                    │
│  S3 Bucket + Bedrock AI                 │
│  ☁️ Data Storage & AI Processing       │
└─────────────────────────────────────────┘
```

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud](https://share.streamlit.io)
- [Streamlit Community](https://discuss.streamlit.io)

## 🎯 Next Steps

After deploying:
1. ✅ Test the app with your API token
2. ✅ Share the URL with your team
3. ✅ Monitor usage in Streamlit Cloud dashboard
4. ✅ Rotate API tokens regularly for security

