#!/bin/bash

# Script to run the FastAPI Medical Data Analysis API
# Works on Mac/Linux

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   🔒 Medical Data Analysis API Startup Script         ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Copying config/env.example to .env..."
    cp config/env.example .env
    echo ""
    echo "🔧 Please edit .env file with your credentials:"
    echo "   - AWS_ACCESS_KEY_ID"
    echo "   - AWS_SECRET_ACCESS_KEY"
    echo "   - S3_BUCKET_NAME"
    echo "   - API_TOKEN (generate with: openssl rand -hex 32)"
    echo ""
    read -p "Press Enter after you've configured .env file..."
fi

# Install/update requirements
echo "📦 Installing/updating dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Get port from .env or use default
PORT=${PORT:-8000}

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║   ✅ Starting API Server                               ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Server: http://localhost:$PORT"
echo "📚 API Docs: http://localhost:$PORT/docs"
echo "🔐 Auth: Bearer token required (set in .env)"
echo ""
echo "📝 Example usage:"
echo "   curl -X POST \"http://localhost:$PORT/api/query\" \\"
echo "        -H \"Authorization: Bearer \$API_TOKEN\" \\"
echo "        -H \"Content-Type: application/json\" \\"
echo "        -d '{\"question\": \"¿Cuántos estudios hay?\"}'"
echo ""
echo "Press Ctrl+C to stop the server"
echo "════════════════════════════════════════════════════════"
echo ""

# Run the API
python api.py

