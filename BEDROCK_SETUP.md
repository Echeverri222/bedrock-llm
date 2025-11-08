# AWS Bedrock Setup Guide

## Why Bedrock?

- No OpenAI API Key needed - Uses your AWS credentials
- Code Interpreter built-in - Can write and execute Python code
- Better AWS integration - Native S3, DynamoDB, etc.
- Multiple models - Claude 3.5 Sonnet, Haiku, Opus
- Data privacy - Data stays in your AWS account

## Setup Steps

### 1. Enable Bedrock Model Access

1. Go to AWS Console -> Bedrock -> Model access
2. Click "Manage model access"
3. Enable: Anthropic - Claude 3.5 Sonnet v2
4. Click "Request model access"
5. Wait for approval (usually instant)

### 2. Update Your .env File

```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=sa-east-1
S3_BUCKET_NAME=your_bucket
BEDROCK_REGION=us-east-1
BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

Note: BEDROCK_REGION should be us-east-1 (Bedrock not available in all regions)

### 3. Run the Application

```bash
python main.py
```

## Available Models

- Claude 3.5 Sonnet v2: Best balance (recommended)
- Claude 3.5 Haiku: Fast and cheap
- Claude 3 Opus: Most capable

## Troubleshooting

### Error: Could not resolve the foundation model

Solution: Enable model access in Bedrock console

### Error: AccessDeniedException

Solution: Add Bedrock permissions to your IAM user

## Cost Comparison

Claude 3.5 Sonnet:
- Input: $3.00 per 1M tokens
- Output: $15.00 per 1M tokens
