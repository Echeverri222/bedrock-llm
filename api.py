"""
FastAPI Application for Secure Medical Data Analysis
Requires Bearer token authentication for all API calls
"""

import os
import sys
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.bedrock_agent import BedrockAgent
from tools.s3_loader import S3DataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Medical Data Analysis API",
    description="Secure API for querying Doppler ultrasound study data with token authentication",
    version="1.0.0"
)

# CORS configuration (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# API Token from environment
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    logger.warning("⚠️  API_TOKEN not set! Using default token. Set API_TOKEN in .env for production!")
    API_TOKEN = "your-secret-token-here-change-this"

# Global variables for lazy initialization
s3_loader = None
agent = None
local_files = {}


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """
    Verify the Bearer token provided in the Authorization header
    """
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


def initialize_services():
    """
    Initialize S3 loader and Bedrock agent (lazy loading)
    """
    global s3_loader, agent, local_files
    
    if agent is not None:
        return  # Already initialized
    
    try:
        # Validate environment variables
        required_vars = [
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY', 
            'AWS_REGION',
            'S3_BUCKET_NAME',
            'BEDROCK_REGION',
            'BEDROCK_MODEL'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Initialize S3 loader
        s3_loader = S3DataLoader(
            bucket_name=os.getenv('S3_BUCKET_NAME'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        # Download files from S3
        logger.info("📥 Downloading files from S3 bucket...")
        files = s3_loader.list_files()
        
        if not files:
            logger.warning("⚠️  No files found in S3 bucket")
        else:
            for file_key in files:
                local_path = s3_loader.download_file(file_key)
                local_files[file_key] = local_path
                logger.info(f"✅ Downloaded: {file_key}")
        
        # Initialize Bedrock agent
        agent = BedrockAgent(
            aws_region=os.getenv('BEDROCK_REGION'),
            model_id=os.getenv('BEDROCK_MODEL')
        )
        
        # Set available files for the agent
        agent.set_available_files(list(local_files.values()))
        
        logger.info("✅ Services initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {str(e)}")
        raise


# Request/Response models
class QueryRequest(BaseModel):
    question: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "¿Cuántos estudios hay en total?"
            }
        }


class QueryResponse(BaseModel):
    answer: str
    tokens_used: Optional[int] = None
    estimated_cost: Optional[float] = None


class HealthResponse(BaseModel):
    status: str
    message: str
    files_loaded: int


# API Endpoints

@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": "Medical Data Analysis API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "authentication": "Bearer token required"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(authenticated: bool = Security(verify_token)):
    """
    Health check endpoint (requires authentication)
    Returns service status and files loaded
    """
    try:
        initialize_services()
        return {
            "status": "healthy",
            "message": "API is running and ready to accept queries",
            "files_loaded": len(local_files)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service initialization failed: {str(e)}"
        )


@app.post("/api/query", response_model=QueryResponse, tags=["Query"])
async def query_data(
    request: QueryRequest,
    authenticated: bool = Security(verify_token)
):
    """
    Query medical data endpoint (requires authentication)
    
    Send a natural language question about the Doppler ultrasound studies.
    The AI agent will analyze the data and provide an answer.
    
    **Authentication:** Requires Bearer token in Authorization header
    
    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/query" \\
         -H "Authorization: Bearer your-token-here" \\
         -H "Content-Type: application/json" \\
         -d '{"question": "¿Cuántos estudios hay en total?"}'
    ```
    """
    try:
        # Initialize services if not already done
        initialize_services()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Agent not initialized"
            )
        
        # Process the query
        logger.info(f"Processing query: {request.question}")
        answer = agent.chat(request.question)
        
        # Get token usage
        token_usage = agent.get_token_usage()
        
        return {
            "answer": answer,
            "tokens_used": token_usage.get('total_tokens', 0),
            "estimated_cost": token_usage.get('estimated_cost', 0.0)
        }
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/api/files", tags=["Files"])
async def list_files(authenticated: bool = Security(verify_token)):
    """
    List all files loaded from S3 (requires authentication)
    """
    try:
        initialize_services()
        return {
            "files": list(local_files.keys()),
            "count": len(local_files)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing files: {str(e)}"
        )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler
    """
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║   🔒 Medical Data Analysis API                        ║
    ║   Secure token-based authentication enabled           ║
    ╚═══════════════════════════════════════════════════════╝
    
    🚀 Starting server on http://0.0.0.0:{port}
    📚 API Documentation: http://localhost:{port}/docs
    🔐 API Token: Set in .env file (API_TOKEN)
    
    📝 Example usage:
    curl -X POST "http://localhost:{port}/api/query" \\
         -H "Authorization: Bearer {API_TOKEN}" \\
         -H "Content-Type: application/json" \\
         -d '{{"question": "¿Cuántos estudios hay en total?"}}'
    """)
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable auto-reload to prevent reload loops
        log_level="info"
    )

