#!/bin/bash

# Inicia o servidor da API FastAPI em background
# O host 0.0.0.0 torna a API acessível de fora do contêiner.
echo "Iniciando API FastAPI em background..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Aguarda um pouco para garantir que a API tenha tempo de iniciar
sleep 5

# Inicia o dashboard Streamlit em foreground
# Este será o processo principal do contêiner.
echo "Iniciando Dashboard Streamlit..."
streamlit run app/dashboard.py --server.port 8501 --server.address 0.0.0.0
