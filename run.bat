@echo off
cd /d %~dp0backend
if not exist venv (
  echo Creating virtual environment...
  python -m venv venv
)
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt -q
echo.
echo NightOwl starting on http://127.0.0.1:8000
echo API Docs - http://127.0.0.1:8000/api/docs
echo.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
