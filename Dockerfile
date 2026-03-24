# Use a imagem base oficial do Python (bookworm é a versão estável atual)
FROM python:3.11-slim-bookworm

# Define o diretório de trabalho no container
WORKDIR /app

# Não instalaremos dependências do sistema por enquanto para contornar erros no apt

# Copia o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o Streamlit usa por padrão
EXPOSE 8501

# Comando para rodar a aplicação
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Copia o script para dentro do container
COPY start.sh /start.sh

# Dá permissão de execução
RUN chmod +x /start.sh

# Define o script como o comando de inicialização
CMD ["/start.sh"]
