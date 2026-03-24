# Use a imagem base oficial do Python (bookworm é a versão estável atual)
FROM python:3.11-slim-bookworm

# Define o diretório de trabalho no container
WORKDIR /app

# Instala o curl e zstd para baixar e extrair o Ollama
RUN apt-get update && apt-get install -y curl zstd && rm -rf /var/lib/apt/lists/*

# Instala o Ollama no container
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copia o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o Streamlit usa por padrão e a do Ollama
EXPOSE 8501
EXPOSE 11434

# Copia o script para dentro do container e dá permissão de execução
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Remove o ENTRYPOINT anterior para permitir que o CMD (start.sh) controle tudo
ENTRYPOINT []

# Define o script como o comando de inicialização
CMD ["/bin/bash", "/start.sh"]
