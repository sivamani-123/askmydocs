@echo off
REM One-time setup for Windows. Requires Python 3.10-3.12 and Node.js 18+ on PATH.
cd backend
python -m venv .venv || goto :err
call .venv\Scripts\activate
pip install -r requirements.txt || goto :err
if not exist .env copy .env.example .env
python ml\train_classifier.py
cd ..\frontend
call npm install || goto :err
echo.
echo Setup complete. Edit backend\.env (MySQL password, JWT secret), then open this folder in VS Code and press F5.
goto :eof
:err
echo Setup failed - read the error above.
exit /b 1
