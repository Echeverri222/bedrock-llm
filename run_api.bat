@echo off
REM Script to run the FastAPI Medical Data Analysis API
REM Works on Windows

echo ╔═══════════════════════════════════════════════════════╗
echo ║   🔒 Medical Data Analysis API Startup Script         ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Virtual environment not found. Creating one...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo 📋 Copying config\env.example to .env...
    copy config\env.example .env
    echo.
    echo 🔧 Please edit .env file with your credentials:
    echo    - AWS_ACCESS_KEY_ID
    echo    - AWS_SECRET_ACCESS_KEY
    echo    - S3_BUCKET_NAME
    echo    - API_TOKEN (generate with: python -c "import secrets; print(secrets.token_hex(32))")
    echo.
    pause
)

REM Install/update requirements
echo 📦 Installing/updating dependencies...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Get port from .env or use default
set PORT=8000

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   ✅ Starting API Server                               ║
echo ╚═══════════════════════════════════════════════════════╝
echo.
echo 🚀 Server: http://localhost:%PORT%
echo 📚 API Docs: http://localhost:%PORT%/docs
echo 🔐 Auth: Bearer token required (set in .env)
echo.
echo 📝 Example usage:
echo    curl -X POST "http://localhost:%PORT%/api/query" ^
echo         -H "Authorization: Bearer YOUR_TOKEN" ^
echo         -H "Content-Type: application/json" ^
echo         -d "{\"question\": \"¿Cuántos estudios hay?\"}"
echo.
echo Press Ctrl+C to stop the server
echo ════════════════════════════════════════════════════════
echo.

REM Run the API
python api.py

