#!/bin/bash

# Verifica se o Uvicorn está instalado
if ! command -v uvicorn &> /dev/null; then
    echo "⚠️ Uvicorn não está instalado. Instalando..."
    sudo apt update && sudo apt install -y uvicorn
else
    echo "✅ Uvicorn já está instalado."
fi

# Inicia o servidor FastAPI na porta 5050
echo "🚀 Iniciando servidor FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 5050
