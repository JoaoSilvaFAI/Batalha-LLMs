#!/bin/bash

# Define OLLAMA_HOST para garantir que ele aceite conexões locais
export OLLAMA_HOST=0.0.0.0

# Inicia o Ollama em background
echo "Iniciando Ollama..."
ollama serve &

# Aguarda a API do Ollama estar pronta
echo "Aguardando Ollama iniciar..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 2
done

# Faz o pull do modelo configurado (se já existir, ele pula rápido)
echo "Baixando/Verificando modelo deepseek-r1:1.5b..."
ollama pull deepseek-r1:1.5b

# Inicia a aplicação Streamlit
echo "Iniciando Streamlit..."
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0