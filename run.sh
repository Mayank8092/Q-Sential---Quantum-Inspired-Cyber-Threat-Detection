#!/bin/bash
# Quick start script for NightOwl

cd "$(dirname "$0")/backend"

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies (first time may take a minute)..."
pip install -r requirements.txt --quiet

echo ""
echo "🦉 Starting NightOwl on http://127.0.0.1:8000"
echo "   API Docs → http://127.0.0.1:8000/api/docs"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
