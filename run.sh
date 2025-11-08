#!/bin/bash

# AWS Bedrock Data Analysis Agent Runner
# This script activates the virtual environment and runs the application

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}AWS Bedrock Data Analysis Agent${NC}"
echo "================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Warning: .env file not found!"
    echo "   Please copy config/env.example to .env and configure it."
    echo ""
    read -p "Press enter to continue anyway..."
fi

# Run the application
echo ""
echo -e "${GREEN}Starting application...${NC}"
echo ""

# Set Python path to include src directory
export PYTHONPATH="$(pwd)/src:${PYTHONPATH}"

# Run main.py from src folder
cd src && python3 main.py

