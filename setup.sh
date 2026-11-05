#!/usr/bin/env bash
# One-time setup for macOS/Linux. Requires Python 3.10-3.12 and Node.js 18+.
set -e
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
python ml/train_classifier.py
cd ../frontend && npm install
echo "Setup complete. Edit backend/.env, then open the folder in VS Code and press F5."
