# 🚀 API Quick Start Guide

Get your secure Medical Data Analysis API running in 5 minutes!

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- S3 bucket with data files

---

## Step 1: Generate Your API Token

**Mac/Linux:**
```bash
openssl rand -hex 32
```

**Windows (PowerShell):**
```powershell
-join ((48..57) + (97..102) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**Python (any platform):**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Save this token** - you'll need it to authenticate API requests!

---

## Step 2: Configure Environment

Create `.env` file in the project root:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=sa-east-1
S3_BUCKET_NAME=your_bucket_name_here

# Bedrock Configuration
BEDROCK_REGION=us-east-1
BEDROCK_MODEL=cohere.command-r-plus-v1:0

# API Token (paste your generated token)
API_TOKEN=paste_your_generated_token_here
```

---

## Step 3: Run the API

**Mac/Linux:**
```bash
./run_api.sh
```

**Windows:**
```cmd
run_api.bat
```

**Or manually:**
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run API
python api.py
```

---

## Step 4: Test It!

### Open Interactive Docs

Visit in your browser:
```
http://localhost:8000/docs
```

### Try a Query

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/query" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cuántos estudios hay en total?"}'
```

**Using the test script:**
```bash
./test_api.sh YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "answer": "Hay un total de 21 estudios en el archivo Excel.",
  "tokens_used": 2145,
  "estimated_cost": 0.0068
}
```

---

## 🎉 You're Ready!

Your API is now running securely with token authentication!

### Next Steps:

1. **Test queries** - Try different questions in the docs at `/docs`
2. **Integrate** - Use the API in your applications
3. **Deploy** - Move to production (AWS EC2, ECS, etc.)
4. **Monitor** - Track token usage and costs

---

## 📝 Example Queries to Try

```bash
# Count studies
"¿Cuántos estudios hay en total?"

# Most expensive
"What was the most expensive study?"

# Find patient
"¿Qué estudios tiene Maria Magnolia Cortes Aguirre?"

# Date range
"¿Cuántos estudios se hicieron en julio?"

# Average cost
"What is the average cost of all studies?"
```

---

## 🔒 Security Reminders

✅ **DO:**
- Keep your `.env` file secure
- Use strong random tokens
- Rotate tokens regularly
- Use HTTPS in production

❌ **DON'T:**
- Commit `.env` to git
- Share your API token
- Use default tokens
- Expose port 8000 publicly without HTTPS

---

## 🆘 Troubleshooting

### API won't start

1. Check `.env` file exists and has all variables
2. Verify AWS credentials are correct
3. Ensure S3 bucket is accessible
4. Check Bedrock model access is enabled

### 401 Unauthorized

- Verify your token matches the `API_TOKEN` in `.env`
- Check `Authorization: Bearer TOKEN` header format
- Ensure no extra spaces in token

### 503 Service Unavailable

- Check AWS credentials have Bedrock permissions
- Verify S3 bucket name is correct
- Ensure files exist in the bucket
- Check internet connection

---

## 📚 Full Documentation

See `docs/API_DOCUMENTATION.md` for complete API reference.

---

**Need help?** Check the logs - the API outputs detailed information about each request and any errors.

