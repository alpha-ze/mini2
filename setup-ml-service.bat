@echo off
echo ========================================
echo Setting up ML Service for DDGRS
echo ========================================
echo.

cd ml-service

echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.9+ is installed
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please edit it with your API keys if needed.
) else (
    echo .env file already exists, skipping...
)

echo.
echo ========================================
echo ML Service setup complete!
echo ========================================
echo.
echo To start the ML service:
echo   1. cd ml-service
echo   2. venv\Scripts\activate
echo   3. python main.py
echo.
echo The service will run on http://localhost:8000
echo.
pause
