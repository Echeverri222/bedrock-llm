@echo off
REM AWS Bedrock Data Analysis Agent Runner (Windows)
REM This script activates the virtual environment and runs the application

echo AWS Bedrock Data Analysis Agent
echo =================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo Warning: .env file not found!
    echo Please copy config\env.example to .env and configure it.
    echo.
    pause
)

REM Run the application
echo.
echo Starting application...
echo.

REM Set Python path to include src directory
set PYTHONPATH=%cd%\src;%PYTHONPATH%

REM Run main.py from src folder
cd src
python main.py

