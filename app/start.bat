@echo off

REM === Backend ===
cd bread-meat-delivery-backend

REM Garante venv com o Python 3.13 detectado pelo py
if not exist venv (
  py -3.13 -m venv venv
)

call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

start "Backend" cmd /k "uvicorn app.main:app --reload"

REM === Frontend ===
cd ..
cd bread-meat-delivery-frontend
npm install
start "Frontend" cmd /k "npm run dev"

cd ..
