# 🚂 Deploy to Railway

Deploy your Medical Data Analysis API to Railway in 5 minutes!

## Prerequisites

- GitHub account (already have it ✅)
- Railway account (free to create)

## Step-by-Step Deployment

### 1. Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### 2. Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Select your repository: `Echeverri222/bedrock-llm`
4. Click "Deploy Now"

### 3. Configure Environment Variables

Railway will start building. While it builds, add your environment variables:

1. Click on your service
2. Go to "Variables" tab
3. Click "Add Variable" or use "RAW Editor" and paste:

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=sa-east-1
S3_BUCKET_NAME=invoice-transcript
BEDROCK_REGION=us-east-1
BEDROCK_MODEL=cohere.command-r-plus-v1:0
API_TOKEN=6a12a1f2250df9edcea50e7b00b30142f353749c1965960770a32ed2e61d3c64
PORT=8000
```

4. Click "Save"

### 4. Get Your Public URL

1. Go to "Settings" tab
2. Scroll to "Networking" section
3. Click "Generate Domain"
4. Copy your URL (e.g., `https://your-app.up.railway.app`)

### 5. Test Your API

```bash
# Replace with your Railway URL
API_URL="https://your-app.up.railway.app"
TOKEN="6a12a1f2250df9edcea50e7b00b30142f353749c1965960770a32ed2e61d3c64"

curl -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cuántos estudios hay en total?"}'
```

### 6. Update Streamlit to Use Production API

Edit `.env` or Streamlit Cloud secrets:

```bash
API_URL=https://your-app.up.railway.app
```

## 🎉 Done!

Your API is now running 24/7 on Railway!

**Access:**
- **API:** `https://your-app.up.railway.app`
- **Docs:** `https://your-app.up.railway.app/docs`

## 💰 Pricing

- **Free Tier:** $5 credit/month (enough for ~100-200 hours)
- **Hobby Plan:** $5/month (500 hours execution time)
- **Pro Plan:** $20/month (unlimited)

## 🔧 Automatic Deployments

Every time you push to `main` branch on GitHub, Railway automatically:
1. Pulls the latest code
2. Rebuilds the application
3. Redeploys with zero downtime

## 📊 Monitoring

Railway dashboard shows:
- **Logs:** Real-time application logs
- **Metrics:** CPU, RAM, Network usage
- **Deployments:** History of all deployments

## 🔄 Rollback

If something breaks:
1. Go to "Deployments" tab
2. Click on a previous working deployment
3. Click "Redeploy"

## 🆘 Troubleshooting

### Build Fails

Check "Deploy Logs" tab for errors. Common issues:
- Missing dependencies in `requirements.txt`
- Environment variables not set

### API Returns 503

- Check if S3 bucket is accessible from Railway
- Verify Bedrock permissions
- Check logs for detailed error messages

### High Memory Usage

Edit Railway settings:
- Go to Settings → Resources
- Increase memory limit (512MB → 1GB)

## 🔐 Security Best Practices

1. **Never commit `.env` to git** (already in `.gitignore` ✅)
2. **Rotate API token regularly** (update in Railway variables)
3. **Use Railway's secret management** (encrypted at rest)
4. **Enable 2FA** on your Railway account

## 🚀 Advanced: Custom Domain

1. Go to Settings → Networking
2. Click "Custom Domain"
3. Add your domain (e.g., `api.yourdomain.com`)
4. Update DNS records as shown
5. Railway auto-provisions SSL certificate

## 📚 Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)

