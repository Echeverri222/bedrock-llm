# AWS Bedrock Data Analysis Agent 🤖

An intelligent AI agent that reads medical data from AWS S3 buckets and answers questions using AWS Bedrock (Cohere Command R+) with function calling capabilities.

## 🌟 Features

- **Excel File Analysis**: Read and analyze Excel files from S3
- **AWS Bedrock Integration**: Uses Cohere Command R+ with function calling
- **AWS S3 Integration**: Automatically downloads and caches files
- **Interactive Chat**: Natural language interface for data analysis
- **Docker Ready**: Easy deployment with Docker
- **Token Tracking**: Monitor usage and costs in real-time
- **Medical Data Focus**: Specialized for Doppler ultrasound studies

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

### 1. Clone the Repository

```bash
git clone https://github.com/Echeverri222/bedrock-llm.git
cd bedrock-llm
```

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

```bash
python main.py
```

## 🐳 Docker Deployment

### Build and Run

```bash
docker compose up --build
```

### Interactive Mode

```bash
docker exec -it llm_data_agent python main.py
```

## 💬 Usage Examples

Once running, you can ask questions like:

```
You: ¿Cuántos estudios hay en total?
Agent: Según los datos del archivo Excel, hay 145 estudios Doppler en total...

You: Show me studies from July
Agent: Filtering the data for July... [results]

You: What are the most common findings?
Agent: Based on the analysis... [summary]
```

### Commands

- Type your question to interact with the data
- `reset` - Clear conversation history
- `quit` or `exit` - End the session

## 🛠️ Project Structure

```
bedrock-llm/
├── main.py                 # Main application entry point
├── bedrock_agent.py        # AWS Bedrock agent with function calling
├── llm_agent.py           # OpenAI agent (alternative)
├── s3_loader.py           # S3 data loader
├── file_tools.py          # Excel/JSON processing tools
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md          # This file
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
