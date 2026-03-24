# ⚔️ LLM Battle Arena — Documentação Completa

Comparador visual entre **Deepseek-r1:1.5b local (Ollama)** e **GPT via OpenAI API**, focado em lógica matemática.

---

## 📁 Estrutura

```
llm_comparator/
├── app.py              # Aplicação principal Streamlit
├── requirements.txt    # Dependências Python
└── README.md           # Esta documentação
```

---

## 🚀 Instalação e Execução

### 1. Pré-requisitos

- Python 3.10+
- [Ollama](https://ollama.com) instalado e rodando
- Modelo `deepseek-r1:1.5b` baixado no Ollama
- API Key da OpenAI

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Garantir que o Ollama está rodando

```bash
# Iniciar o servidor Ollama (se não estiver rodando)
ollama serve

# Em outro terminal, verificar se o modelo está disponível
ollama list

# Se não tiver o modelo, baixar:
ollama pull deepseek-r1:1.5b
```

### 4. Rodar o app

```bash
python -m streamlit run app.py
```

O app abrirá automaticamente em: **http://localhost:8501**

---

## 🖥️ Como usar

1. **Sidebar (barra lateral esquerda)**
   - Confirme o modelo Ollama (`deepseek-r1:1.5b`)
   - Confirme o endpoint (`http://localhost:11434`)
   - Insira sua **OpenAI API Key** (campo senha)
   - Escolha o modelo GPT desejado
   - Personalize o system prompt se quiser

2. **Campo de equação**
   - Digite qualquer equação ou problema matemático
   - Use o botão **📋 Exemplos** para carregar um exemplo

3. **Botão ⚔️ BATALHAR**
   - Envia a equação para **ambos os modelos simultaneamente** (threads paralelas)
   - Exibe as respostas lado a lado com métricas

4. **Métricas exibidas por modelo**
   - ⚡ **Latência** — tempo total de resposta em segundos
   - 🪙 **Tokens** — total de tokens consumidos (prompt + resposta)
   - 🎯 **Confiança** — percentual extraído automaticamente da resposta do modelo

5. **Banner de veredicto**
   - Declara o vencedor com base em latência e confiança combinadas

---

## ⚙️ Configurações avançadas

### Trocar modelo Ollama
Na sidebar, altere o campo **Modelo** para qualquer modelo que você tenha baixado:
```
llama3, mistral, deepseek-r1, phi3, gemma2, etc.
```

### Trocar modelo OpenAI
Selecione no dropdown da sidebar:
- `gpt-4o` — mais capaz, mais lento
- `gpt-4o-mini` — equilibrado (recomendado)
- `gpt-4-turbo` — alternativa poderosa
- `gpt-3.5-turbo` — mais rápido e barato

### Personalizar system prompt
Edite o campo **System Prompt** na sidebar para adaptar o comportamento dos modelos.

---

## 🔌 Endpoints utilizados

| Serviço | Endpoint | Documentação |
|---------|----------|--------------|
| Ollama  | `POST http://localhost:11434/api/chat` | https://github.com/ollama/ollama/blob/main/docs/api.md |
| OpenAI  | `POST https://api.openai.com/v1/chat/completions` | https://platform.openai.com/docs/api-reference/chat |

### Payload Ollama (`/api/chat`)
```json
{
  "model": "deepseek-r1:1.5b",
  "messages": [
    { "role": "system", "content": "..." },
    { "role": "user",   "content": "2x + 3 = 7" }
  ],
  "stream": false
}
```

## 🚀 Como Executar

Você pode rodar esta aplicação de duas formas:

### Opção A: Execução via Docker (Recomendado)

Esta opção é 100% independente do seu Windows, pois roda tanto a aplicação quanto o servidor Ollama dentro do container.

1. **Pré-requisitos**: Docker e Docker Compose instalados.
2. **Comando**:
   ```bash
   docker-compose up --build
   ```
3. **O que acontece automaticamente**:
   - O Docker instala o servidor Ollama internamente.
   - O script de inicialização baixa automaticamente o modelo `deepseek-r1:1.5b`.
   - O Streamlit sobe na porta `8501`.
4. **Acesso**: Abra **[http://localhost:8501](http://localhost:8501)**

---

### 📥 Baixando novas LLMs no Docker

Se você quiser usar outros modelos além do padrão, você deve baixá-los dentro do container em execução:

```bash
# 1. Verifique o nome do seu container (ex: batalha-llms-app-1)
docker ps

# 2. Execute o comando de pull dentro do container
docker exec -it batalha-llms-app-1 ollama pull llama3.2
```

Os modelos baixados serão persistidos no volume `ollama_data` configurado no `docker-compose.yml`.

---

### Opção B: Execução Local (Python)

1. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Rodar o App**:
   ```bash
  python -m streamlit run app.py
   ```

---

## 🖥️ Funcionalidades e Modelos

### 🟦 Modelos Locais (Ollama)
O app detecta automaticamente os modelos instalados no seu computador.
- **Modelos testados**: `olmo-3:7b`, `deepseek-r1:1.5b`, `llama3.2`.
- **Endpoint**: Fixo em `http://localhost:11434` (ou configurado via env no Docker).

### 🟣 Modelos de Nuvem (OpenAI)
O app já vem com uma **API Key configurada** internamente.
- **Modelos Disponíveis**:
    - `o3-mini`, `o1`, `o1-mini` (Mais atuais)
    - `gpt-4o`, `gpt-4o-mini`
    - `gpt-5.2`, `gpt-5.1` (Hypothetical/Layout test)

---

## 🧮 Formato de Saída Padronizado

Ambos os modelos são instruídos a responder seguindo rigorosamente esta estrutura:
1. **🧠 Raciocínio**: Explicação passo a passo.
2. **✅ Resposta Final**: O resultado direto.
3. **🎯 Confiança**: Nível de certeza de 0 a 100%.

---

## 🔌 Endpoints de Integração

| Serviço | Endpoint | Base |
|---------|----------|------|
| **Ollama** | `/api/chat` | `http://localhost:11434` |
| **OpenAI** | `/v1/chat/completions` | `https://api.openai.com` |

---

## 🐛 Solução de Problemas

- **Conexão Recusada (Local Python)**: Se estiver rodando LOCAL (Opção B), verifique se o Ollama no Windows está permitindo conexões externas (variável `OLLAMA_HOST=0.0.0.0`) e se o Firewall permite a porta 11434.
- **Erro de Rede no Docker Build**: Se o `apt-get` falhar durante o build, o download do Ollama pode ser interrompido; tente rodar o build novamente.
- **Erro 500 ao carregar modelo**: Geralmente indica falta de RAM para rodar o modelo local selecionado. Tente um modelo menor como `deepseek-r1:1.5b`.
