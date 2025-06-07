@echo off
REM Activate Python virtual environment and run app.py

REM Change directory to script location
cd /d "%~dp0"

REM Activate the virtual environment (update 'venv' if your env folder has a different name)
call .venv\Scripts\activate.bat

REM Run the Python script
python app.py

REM Optional: Pause to keep the window open
pause