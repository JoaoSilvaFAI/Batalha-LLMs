#!/bin/bash

# Inicia o Ollama em background
ollama serve &

# Aguarda alguns segundos para garantir que a API do Ollama esteja pronta
sleep 5

# Inicia a sua aplicação principal (substitua pelo comando real da sua stack, ex: npm start, python main.py, etc)
python -m streamlit run app.py