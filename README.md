# AWS Bedrock Data Analysis Agent 🤖

An intelligent AI agent that reads medical data from AWS S3 buckets and answers questions using AWS Bedrock (Cohere Command R+) with function calling capabilities.

## 🎯 Two Deployment Options

1. **🔒 Secure REST API** (Recommended for production) - Token-based authentication, perfect for integrations
2. **🌐 Web App** - Beautiful Streamlit UI with chat interface

## 🌟 Features

### Core Features
- 📊 **Excel File Analysis**: Read and analyze Excel files from S3
- 🤖 **AWS Bedrock Integration**: Uses Cohere Command R+ with function calling
- ☁️ **AWS S3 Integration**: Automatically downloads and caches files
- 💬 **Natural Language Interface**: Ask questions in English or Spanish
- 💰 **Token Tracking**: Monitor usage and costs in real-time
- 🏥 **Medical Data Focus**: Specialized for Doppler ultrasound studies

### API Mode (Secure)
- 🔐 **Token Authentication**: Bearer token security (like DevRev API)
- 📡 **REST API**: Easy integration with any application
- 📚 **Auto Documentation**: Interactive Swagger/OpenAPI docs
- 🚀 **Production Ready**: FastAPI with uvicorn

### Web App Mode
- 🌐 **Browser Interface**: Beautiful Streamlit UI
- 💬 **Chat Interface**: Conversational data analysis
- 🎨 **Custom Theme**: Professional design
- ☁️ **Cloud Deploy**: Easy deployment to Streamlit Cloud

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   AWS S3    │─────▶│   Python     │─────▶│  AWS Bedrock│
│   Bucket    │      │  Application │      │  (Cohere)   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Excel Files │
                     │  JSON Files  │
                     └──────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- AWS Account with:
  - S3 bucket access
  - Bedrock model access (Cohere Command R+)
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### Option A: Secure REST API (Recommended) 🔒

**Best for:** Production use, integrations, keeping data private

```bash
# 1. Clone the repository
git clone https://github.com/Echeverri222/bedrock-llm.git
cd bedrock-llm

# 2. Generate API token
openssl rand -hex 32

# 3. Configure .env (add your token)
cp config/env.example .env
# Edit .env with your AWS credentials and API_TOKEN

# 4. Run the API
./run_api.sh  # Mac/Linux
# or
run_api.bat  # Windows
```

**Access:**
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

**Quick test:**
```bash
curl -X POST "http://localhost:8000/api/query" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cuántos estudios hay?"}'
```

📖 **Full API Documentation:** See [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md)

---

### Option B: Web App Interface 🌐

**Best for:** Quick analysis, visual interface, demos

```bash
# 1. Clone the repository
git clone https://github.com/Echeverri222/bedrock-llm.git
cd bedrock-llm

### 2. Set Up Environment

Create a `.env` file:

```bash
cp env.example .env
```

Edit `.env` with your AWS credentials:

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=sa-east-1
S3_BUCKET_NAME=your_bucket_name_here
BEDROCK_REGION=us-east-1
BEDROCK_MODEL=cohere.command-r-plus-v1:0
```

### 3. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Application

#### **🌐 Web Interface (Recommended!)**

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501` 

**Features:**
- ✨ Beautiful chat interface
- 📊 Real-time token usage
- 📁 View S3 files
- 💬 Conversation history
- 🔄 Easy reset

---

#### **💻 CLI Interface (Classic)**

**Easy way:**
```bash
./run.sh              # Mac/Linux
run.bat               # Windows
```

**Manual way:**
```bash
source venv/bin/activate
cd src && python main.py
```

## 🐳 Docker Deployment

### Streamlit Web App

```bash
docker run -it -p 8501:8501 --env-file .env bedrock-llm streamlit run streamlit_app.py
```

Access at `http://localhost:8501`

---

### CLI Version

```bash
cd docker
docker compose up --build
docker exec -it llm_data_agent python src/main.py
```

### Or build from root:

```bash
docker build -f docker/Dockerfile -t bedrock-llm .
docker run -it --env-file .env bedrock-llm
```

---

## 🚀 Deploy to Cloud

### Deploy to Streamlit Cloud (FREE!)

1. **Push to GitHub** (already done ✅)

2. **Go to** [share.streamlit.io](https://share.streamlit.io)

3. **Click "New app"**

4. **Select your repo**: `Echeverri222/bedrock-llm`

5. **Set main file**: `streamlit_app.py`

6. **Add secrets** (click Advanced settings → Secrets):
   ```toml
   AWS_ACCESS_KEY_ID = "your_key"
   AWS_SECRET_ACCESS_KEY = "your_secret"
   AWS_REGION = "sa-east-1"
   S3_BUCKET_NAME = "your_bucket"
   BEDROCK_REGION = "us-east-1"
   BEDROCK_MODEL = "cohere.command-r-plus-v1:0"
   ```

7. **Click Deploy!** 🚀

Your app will be live at `https://yourusername-bedrock-llm.streamlit.app`

---

### Deploy to Railway (Alternative)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Add environment variables in Railway dashboard.

## 💬 Usage Examples

### Web Interface

Simply type your questions in the chat box:

```
¿Cuántos estudios hay en total?
Show me studies from July
What are the most common findings?
```

The assistant will automatically use the right tools to answer!

---

### CLI Interface

```
You: ¿Cuántos estudios hay en total?
Agent: Según los datos del archivo Excel, hay 145 estudios Doppler en total...

You: Show me studies from July
Agent: Filtering the data for July... [results]

You: What are the most common findings?
Agent: Based on the analysis... [summary]
```

**Commands:**
- Type your question to interact with the data
- `reset` - Clear conversation history (CLI only)
- `quit` or `exit` - End the session (CLI only)

## 🛠️ Project Structure

```
bedrock-llm/
├── streamlit_app.py          # 🌐 Web interface (START HERE!)
├── src/                      # Source code
│   ├── main.py              # CLI application entry point
│   ├── agents/              # AI agents
│   │   ├── bedrock_agent.py # AWS Bedrock agent
│   │   └── llm_agent.py     # OpenAI agent
│   └── tools/               # Utility tools
│       ├── s3_loader.py     # S3 data loader
│       └── file_tools.py    # File processing
├── .streamlit/               # Streamlit configuration
│   └── config.toml          # Theme and settings
├── docker/                   # Docker files
│   ├── Dockerfile           # Docker configuration
│   └── docker-compose.yml   # Docker Compose
├── docs/                     # Documentation
│   └── BEDROCK_SETUP.md     # Bedrock setup guide
├── config/                   # Configuration files
│   └── env.example          # Environment template
├── data/                     # Data cache (auto-created)
├── run.sh                    # Run script (Mac/Linux)
├── run.bat                   # Run script (Windows)
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔧 Available Tools

The agent has access to:

1. **read_excel**: Read Excel file structure and sample data
2. **query_excel**: Filter data using pandas query syntax
3. **get_excel_column_values**: Extract values from specific columns
4. **list_available_files**: Show all files from S3

## 💰 Cost Information

### Cohere Command R+ Pricing
- **Input**: $3.00 per 1M tokens
- **Output**: $15.00 per 1M tokens
- **Typical question**: ~$0.007 (0.7 cents)

### Example Usage Costs
- 100 questions/day = $0.70/day
- 1,000 questions/month = $7.00/month

**Note**: Costs appear on your AWS bill under "Amazon Bedrock"

## 🔐 AWS Setup

### 1. Enable Bedrock Model Access

1. Go to AWS Console → Bedrock → Model access
2. Ensure **Cohere Command R+** is enabled
3. Models are automatically available (no use case form needed)

### 2. IAM Permissions

Your IAM user needs these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:*::foundation-model/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name/*",
                "arn:aws:s3:::your-bucket-name"
            ]
        }
    ]
}
```

Or use managed policies:
- `AmazonBedrockFullAccess`
- `AmazonS3ReadOnlyAccess`

## 🎯 Use Case: Medical Data Analysis

This project is specialized for analyzing Doppler ultrasound studies:

- **Data Type**: Medical diagnostic records
- **Format**: Excel files with patient information, dates, findings
- **Period**: July-August 2025 studies
- **Privacy**: All data stays in AWS, HIPAA-compatible infrastructure

## 🔄 Alternative Models

If you want to use different models, update `.env`:

### Claude 3.5 Sonnet (after use case approval)
```env
BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20240620-v1:0
```

### Mistral Large
```env
BEDROCK_MODEL=mistral.mistral-large-2407-v1:0
```

### OpenAI (switch back)
Remove Bedrock config and add:
```env
OPENAI_API_KEY=your_openai_key
```

## 🐛 Troubleshooting

### Error: AccessDeniedException
**Solution**: Add Bedrock permissions to your IAM user (see AWS Setup)

### Error: ValidationException - model doesn't support tool use
**Solution**: Ensure you're using `cohere.command-r-plus-v1:0` or another tool-compatible model

### Error: ResourceNotFoundException - use case form
**Solution**: Switch to Cohere (no form needed) or fill out Anthropic use case form

### SSL Certificate Errors
**Solution**: Run certificate installer (macOS):
```bash
/Applications/Python*/Install\ Certificates.command
```

## 📊 Monitoring Costs

View your Bedrock usage:

1. **AWS Cost Explorer**: 
   - Console → Cost Management → Cost Explorer
   - Filter by service: "Bedrock"

2. **Bedrock Dashboard**:
   - Console → Bedrock → Usage/Metrics

3. **Set Budget Alerts**:
   - Console → Billing → Budgets
   - Create alert for $10/month threshold

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License

## 👤 Author

**Simon Echeverri**

- GitHub: [@Echeverri222](https://github.com/Echeverri222)

## 🙏 Acknowledgments

- AWS Bedrock for providing the AI infrastructure
- Cohere for the Command R+ model
- OpenAI for the alternative implementation

---

**⭐ Star this repo if you find it helpful!**
