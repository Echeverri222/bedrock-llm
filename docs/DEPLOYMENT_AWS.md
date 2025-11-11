# ☁️ Deploy to AWS

Deploy your Medical Data Analysis API to AWS for production use.

## Option 1: AWS App Runner (Easiest)

### Prerequisites
- AWS Account
- Docker installed locally (optional)

### Steps

1. **Create Dockerfile for production** (already exists in `docker/Dockerfile`)

2. **Push to Amazon ECR (Elastic Container Registry)**

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name medical-api --region us-east-1

# Build and tag
docker build -t medical-api -f docker/Dockerfile .
docker tag medical-api:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/medical-api:latest

# Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/medical-api:latest
```

3. **Create App Runner Service**

Go to AWS Console → App Runner → Create service:
- Source: Container registry → ECR
- Image: Select your pushed image
- Port: 8000
- Environment variables: Add all from `.env`
- Click "Create & Deploy"

**Cost:** ~$15-30/month (pay for what you use)

---

## Option 2: AWS EC2 (Full Control)

### Launch EC2 Instance

1. **Create EC2 instance:**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.micro (free tier) or t3.small
   - Security Group: Allow port 8000 (or 80/443)
   - Key pair: Create or use existing

2. **Connect to instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install dependencies:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip git

# Clone your repo
git clone https://github.com/Echeverri222/bedrock-llm.git
cd bedrock-llm

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

4. **Create `.env` file:**
```bash
nano .env
# Paste your environment variables
```

5. **Run with systemd (auto-start on boot):**

Create service file:
```bash
sudo nano /etc/systemd/system/medical-api.service
```

Paste:
```ini
[Unit]
Description=Medical Data Analysis API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/bedrock-llm
Environment="PATH=/home/ubuntu/bedrock-llm/venv/bin"
ExecStart=/home/ubuntu/bedrock-llm/venv/bin/python api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable medical-api
sudo systemctl start medical-api
sudo systemctl status medical-api
```

6. **Set up nginx as reverse proxy (optional):**

```bash
sudo apt install -y nginx

sudo nano /etc/nginx/sites-available/medical-api
```

Paste:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or EC2 public IP

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/medical-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Get your API URL:**
- **With nginx:** `http://your-ec2-ip/`
- **Direct:** `http://your-ec2-ip:8000/`

**Cost:** 
- t3.micro: Free tier (first 12 months) or ~$7/month
- t3.small: ~$15/month

---

## Option 3: AWS ECS Fargate (Recommended for Scale)

### Prerequisites
- Docker installed locally
- AWS CLI configured

### Steps

1. **Create ECS Cluster:**
```bash
aws ecs create-cluster --cluster-name medical-api-cluster --region us-east-1
```

2. **Create Task Definition:**

Create `task-definition.json`:
```json
{
  "family": "medical-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "medical-api",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/medical-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "AWS_ACCESS_KEY_ID", "value": "your_value"},
        {"name": "AWS_SECRET_ACCESS_KEY", "value": "your_value"},
        {"name": "AWS_REGION", "value": "sa-east-1"},
        {"name": "S3_BUCKET_NAME", "value": "your_bucket"},
        {"name": "BEDROCK_REGION", "value": "us-east-1"},
        {"name": "BEDROCK_MODEL", "value": "cohere.command-r-plus-v1:0"},
        {"name": "API_TOKEN", "value": "your_token"}
      ]
    }
  ]
}
```

Register:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

3. **Create Service:**
```bash
aws ecs create-service \
  --cluster medical-api-cluster \
  --service-name medical-api-service \
  --task-definition medical-api \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

4. **Set up Application Load Balancer** (for HTTPS and domain):
   - Create ALB in AWS Console
   - Create target group (port 8000)
   - Add ECS service to target group
   - Configure Route53 for custom domain

**Cost:** 
- Fargate: ~$10-20/month (256 CPU, 512 MB RAM)
- ALB: ~$16/month + data transfer

---

## Comparison

| Feature | Railway | EC2 | ECS Fargate | App Runner |
|---------|---------|-----|-------------|------------|
| **Setup Time** | 5 min | 30 min | 20 min | 15 min |
| **Cost** | $5-20/mo | $7-15/mo | $10-20/mo | $15-30/mo |
| **Scalability** | Auto | Manual | Auto | Auto |
| **Maintenance** | None | High | Low | None |
| **Free Tier** | $5 credit | 12 months | No | No |

## Recommendation

**For quick production:** Use **Railway** (easiest, fastest)

**For AWS ecosystem:** Use **App Runner** (simple, AWS-native)

**For full control:** Use **EC2** (cheapest, most flexible)

**For enterprise scale:** Use **ECS Fargate** (auto-scaling, production-grade)

