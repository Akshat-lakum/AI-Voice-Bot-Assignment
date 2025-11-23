@echo off
echo ===================================================
echo 🚀 STARTING VOICE BOT ECOSYSTEM
echo ===================================================

:: 1. Start the Server in a new window
start "Voice Bot Server" cmd /k "python -m uvicorn app.main:app --reload"

:: 2. Start the Dashboard in a new window
start "Analytics Dashboard" cmd /k "streamlit run analytics/dashboard.py"

:: 3. Wait a few seconds for server to boot
timeout /t 5

:: 4. Start the Client in THIS window
echo.
echo 🎙️ MIC CLIENT IS READY.
echo Press ENTER in this window to start recording.
python client/mic_record.py

pause