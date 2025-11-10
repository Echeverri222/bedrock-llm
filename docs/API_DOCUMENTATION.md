# 🔒 API Documentation

Secure REST API for querying medical data from S3 bucket with token-based authentication.

## 🔐 Authentication

All API endpoints require a **Bearer token** in the `Authorization` header.

```bash
Authorization: Bearer YOUR_API_TOKEN_HERE
```

### Generate a Secure Token

```bash
# Mac/Linux
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

Add the token to your `.env` file:

```env
API_TOKEN=your-generated-token-here
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `config/env.example` to `.env` and set:

- AWS credentials
- S3 bucket name
- Bedrock configuration
- **API_TOKEN** (your secure token)

### 3. Run the API

```bash
python api.py
```

Or with uvicorn directly:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Documentation

Open in browser:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information and status.

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "name": "Medical Data Analysis API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "authentication": "Bearer token required"
}
```

---

### 2. Health Check

**GET** `/health`

Check API health and files loaded (requires authentication).

```bash
curl -X GET "http://localhost:8000/health" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running and ready to accept queries",
  "files_loaded": 1
}
```

---

### 3. Query Data (Main Endpoint)

**POST** `/api/query`

Ask questions about the medical data in natural language.

**Headers:**
- `Authorization: Bearer YOUR_TOKEN_HERE`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "question": "¿Cuántos estudios hay en total?"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/query" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cuántos estudios hay en total?"}'
```

**Response:**
```json
{
  "answer": "Hay un total de 21 estudios en el archivo Excel.",
  "tokens_used": 2145,
  "estimated_cost": 0.0068
}
```

---

### 4. List Files

**GET** `/api/files`

List all files loaded from S3 bucket (requires authentication).

```bash
curl -X GET "http://localhost:8000/api/files" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
{
  "files": [
    "ESTUDIOS DOPPLER JULIO - AGOSTO 2025.xlsx"
  ],
  "count": 1
}
```

---

## 🔑 Authentication Examples

### Using curl

```bash
# Store token in variable
TOKEN="your-api-token-here"

# Make authenticated request
curl -X POST "http://localhost:8000/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "What was the most expensive study?"}'
```

### Using Python requests

```python
import requests

API_URL = "http://localhost:8000"
TOKEN = "your-api-token-here"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Make query
response = requests.post(
    f"{API_URL}/api/query",
    headers=headers,
    json={"question": "¿Cuántos estudios hay en total?"}
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Cost: ${result['estimated_cost']:.4f}")
```

### Using JavaScript (Node.js)

```javascript
const fetch = require('node-fetch');

const API_URL = 'http://localhost:8000';
const TOKEN = 'your-api-token-here';

async function queryAPI(question) {
  const response = await fetch(`${API_URL}/api/query`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question })
  });
  
  return await response.json();
}

// Usage
queryAPI('¿Cuántos estudios hay en total?')
  .then(result => {
    console.log('Answer:', result.answer);
    console.log('Cost:', result.estimated_cost);
  });
```

---

## 🚨 Error Responses

### 401 Unauthorized

Invalid or missing token:

```json
{
  "detail": "Invalid authentication token"
}
```

### 500 Internal Server Error

Server error during query processing:

```json
{
  "error": "Error processing query: ...",
  "status_code": 500
}
```

### 503 Service Unavailable

Service not initialized or AWS connection failed:

```json
{
  "detail": "Service initialization failed: ..."
}
```

---

## 📊 Example Queries

### Spanish Queries

```bash
# Count total studies
curl -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cuántos estudios hay en total?"}'

# Find most expensive study
curl -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cuál fue el estudio más caro y cuánto costó?"}'

# Find specific patient
curl -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Qué estudios tiene la paciente Maria Magnolia Cortes Aguirre?"}'
```

### English Queries

```bash
# Count studies
curl -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "How many studies are there in total?"}'

# Most expensive study
curl -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "What was the most expensive study and what patient did it?"}'

# Studies by date
curl -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "How many studies were done in July 2025?"}'
```

---

## 🌐 Deployment

### Local Development

```bash
python api.py
```

### Production with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:8000
```

### Docker Deployment

```bash
# Build image
docker build -t medical-data-api -f docker/Dockerfile .

# Run container
docker run -p 8000:8000 --env-file .env medical-data-api
```

### AWS EC2 / Cloud Deployment

1. Install dependencies
2. Set environment variables
3. Run with systemd service:

```ini
# /etc/systemd/system/medical-api.service
[Unit]
Description=Medical Data Analysis API
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/app
Environment="PATH=/home/ubuntu/app/venv/bin"
ExecStart=/home/ubuntu/app/venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Environment Variables for Production

```env
# Required
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=sa-east-1
S3_BUCKET_NAME=your_bucket
BEDROCK_REGION=us-east-1
BEDROCK_MODEL=cohere.command-r-plus-v1:0

# API Security
API_TOKEN=your-secure-random-token-here

# Optional
PORT=8000
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Use `.gitignore`
2. **Generate strong tokens** - Use `openssl rand -hex 32`
3. **Use HTTPS in production** - Never plain HTTP
4. **Rotate tokens regularly** - Update `API_TOKEN` periodically
5. **Limit CORS origins** - Change `allow_origins=["*"]` to specific domains
6. **Use environment secrets** - In AWS/Cloud, use AWS Secrets Manager
7. **Rate limiting** - Add rate limiting middleware for production
8. **Logging** - Monitor access logs and failed authentication attempts

---

## 📈 Cost Tracking

Each response includes:

- `tokens_used`: Total tokens consumed
- `estimated_cost`: Approximate cost in USD

Monitor your AWS Bedrock costs in the AWS Console under Bedrock → Usage.

---

## 🆘 Support

For issues:
1. Check logs: API outputs detailed logs
2. Verify `.env` configuration
3. Test with `/health` endpoint
4. Check AWS credentials and permissions
5. Verify S3 bucket access

---

## 📝 License

Private API - Internal use only.

