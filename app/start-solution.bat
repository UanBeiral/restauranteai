@echo off

REM Ativa o ambiente virtual do backend (ajuste o caminho se necessário)
cd bread-meat-delivery-backend
call venv\Scripts\activate

REM Sobe o backend em uma nova janela
start "Backend" cmd /k "uvicorn app.main:app --reload"

REM Volta para a pasta do projeto pai
cd ..

REM Sobe o frontend em uma nova janela
cd bread-meat-delivery-frontend
start "Frontend" cmd /k "npm run dev"

REM Volta para a raiz
cd ..
