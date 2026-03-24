import streamlit as st
import requests
import time
import json
from openai import OpenAI

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="LLM Battle Arena",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Header */
.arena-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
    background: linear-gradient(135deg, #0a0a0f 0%, #12121f 100%);
    border-bottom: 1px solid #1e1e3a;
    margin-bottom: 2rem;
}
.arena-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #6c63ff, #ff6b9d, #ffd93d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}
.arena-subtitle {
    color: #666680;
    font-size: 0.95rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: -0.3rem;
}

/* Contestant cards */
.contestant-card {
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid;
}
.card-local {
    background: linear-gradient(135deg, #0f1a2e, #0a1628);
    border-color: #1e4080;
}
.card-api {
    background: linear-gradient(135deg, #1a0f2e, #120a28);
    border-color: #6c1e80;
}
.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.tag-local { color: #4da6ff; }
.tag-api   { color: #bf6cff; }
.card-model {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #888;
}

/* Response boxes */
.response-box {
    background: #11111c;
    border-radius: 12px;
    padding: 1.4rem;
    min-height: 220px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    line-height: 1.7;
    color: #d0d0e8;
    border: 1px solid #1e1e3a;
    white-space: pre-wrap;
    word-break: break-word;
}
.response-placeholder {
    color: #333355;
    font-style: italic;
}

/* Metric chips */
.metrics-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 0.8rem;
}
.metric-chip {
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.chip-latency  { background: #0d2a1a; color: #3dff8a; border: 1px solid #1a4d30; }
.chip-tokens   { background: #2a1a0d; color: #ffb23d; border: 1px solid #4d300d; }
.chip-conf     { background: #1a0d2a; color: #d97dff; border: 1px solid #3d1a4d; }

/* VS divider */
.vs-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding-top: 6rem;
}
.vs-badge {
    background: linear-gradient(135deg, #6c63ff, #ff6b9d);
    border-radius: 50%;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1rem;
    color: white;
    box-shadow: 0 0 30px rgba(108,99,255,0.5);
}

/* Input area */
.input-section {
    background: #11111c;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #1e1e3a;
    margin-bottom: 1.5rem;
}

/* Verdict banner */
.verdict-banner {
    border-radius: 16px;
    padding: 1.2rem 1.8rem;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 1.5rem;
    letter-spacing: 1px;
}
.verdict-local  { background: #0a1f2e; border: 1px solid #4da6ff; color: #4da6ff; }
.verdict-api    { background: #1a0a2e; border: 1px solid #bf6cff; color: #bf6cff; }
.verdict-tie    { background: #1a1a0a; border: 1px solid #ffd93d; color: #ffd93d; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0d18 !important;
    border-right: 1px solid #1e1e3a;
}
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stSelectbox select {
    background: #11111c !important;
    border-color: #2a2a4a !important;
    color: #e8e8f0 !important;
}

/* Scrollable history */
.history-item {
    background: #11111c;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    border-left: 3px solid #6c63ff;
    color: #aaa;
    cursor: pointer;
}

/* Streamlit overrides */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #9b59ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 1px !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(108,99,255,0.4) !important;
}
.stTextArea textarea {
    background: #11111c !important;
    border-color: #2a2a4a !important;
    color: #e8e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    border-radius: 10px !important;
}
.stTextArea textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
}
div[data-testid="stMarkdownContainer"] p { color: #c0c0d8; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "result_local" not in st.session_state:
    st.session_state.result_local = None
if "result_api" not in st.session_state:
    st.session_state.result_api = None

# ──────────────────────────────────────────────
# SIDEBAR — SETTINGS
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    st.markdown("---")

    st.markdown("**🟦 Modelo Local (Ollama)**")
    
    import os
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    st.caption(f"Endpoint: `{ollama_url}`")

    def get_ollama_models(base_url):
        try:
            resp = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            return [m["name"] for m in data.get("models", [])]
        except:
            return []

    available_models = get_ollama_models(ollama_url)
    
    if available_models:
        # Tenta selecionar olmo-3:7b por padrão se disponível, senão o primeiro da lista
        default_idx = 0
        if "olmo-3:7b" in available_models:
            default_idx = available_models.index("olmo-3:7b")
        
        ollama_model = st.selectbox("Modelo", options=available_models, index=default_idx, key="ollama_model")
    else:
        st.warning("⚠️ Não foi possível listar modelos do Ollama. Verifique o endpoint.")
        ollama_model = st.text_input("Modelo (Manual)", value="olmo-3:7b", key="ollama_model_manual")

    st.markdown("---")
    st.markdown("**🟣 OpenAI API**")
    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""), key="openai_key_input")
    openai_model = st.selectbox("Modelo GPT", ["gpt-5.2", "gpt-5.1", "gpt-4.1", "o3-mini", "o1", "o1-mini", "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"], key="openai_model")

    st.markdown("---")
    st.markdown("**🧮 Prompt de Sistema**")
    system_prompt = st.text_area(
        "System Prompt",
        value="Você é um especialista em lógica matemática. Sua resposta deve seguir RIGOROSAMENTE este formato:\n\n### 🧠 Raciocínio\n[Explicação passo a passo]\n\n### ✅ Resposta Final\n[Resultado da equação]\n\n### 🎯 Confiança\n[Indique seu nível de confiança de 0 a 100]%",
        height=180,
        key="system_prompt",
    )

    st.markdown("---")
    st.markdown("**📜 Histórico**")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-8:])):
            st.markdown(f'<div class="history-item">#{len(st.session_state.history)-i} {item["equation"][:45]}{"..." if len(item["equation"]) > 45 else ""}</div>', unsafe_allow_html=True)
    else:
        st.caption("Nenhuma consulta ainda.")

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def call_ollama(prompt: str, system: str, model: str, base_url: str) -> dict:
    """Call Ollama local API and return result dict."""
    url = f"{base_url.rstrip('/')}/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        "stream": False,
    }
    t0 = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data     = resp.json()
        elapsed  = time.time() - t0
        content  = data.get("message", {}).get("content", "")
        # token counts from Ollama response
        p_tokens = data.get("prompt_eval_count", 0)
        c_tokens = data.get("eval_count", 0)
        conf     = extract_confidence(content)
        return {
            "ok": True,
            "text": content,
            "latency": elapsed,
            "prompt_tokens": p_tokens,
            "completion_tokens": c_tokens,
            "total_tokens": p_tokens + c_tokens,
            "confidence": conf,
        }
    except Exception as e:
        return {"ok": False, "text": f"❌ Erro ao conectar ao Ollama:\n{e}", "latency": 0,
                "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "confidence": None}


def call_openai(prompt: str, system: str, model: str, api_key: str) -> dict:
    """Call OpenAI API and return result dict."""
    if not api_key:
        return {"ok": False, "text": "❌ Insira sua OpenAI API Key na barra lateral.", "latency": 0,
                "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "confidence": None}
    t0 = time.time()
    try:
        client = OpenAI(api_key=api_key)
        resp   = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.2,
        )
        elapsed = time.time() - t0
        content = resp.choices[0].message.content
        usage   = resp.usage
        conf    = extract_confidence(content)
        return {
            "ok": True,
            "text": content,
            "latency": elapsed,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "confidence": conf,
        }
    except Exception as e:
        return {"ok": False, "text": f"❌ Erro na API OpenAI:\n{e}", "latency": 0,
                "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "confidence": None}


def extract_confidence(text: str) -> float | None:
    """Try to extract a confidence percentage from the model's response."""
    import re
    patterns = [
        r'confiança[:\s]*(\d{1,3})\s*%',
        r'confidence[:\s]*(\d{1,3})\s*%',
        r'(\d{1,3})\s*%\s*de confiança',
        r'(\d{1,3})%',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = int(m.group(1))
            if 0 <= val <= 100:
                return val
    return None


def confidence_color(val):
    if val is None:
        return "#555"
    if val >= 80:
        return "#3dff8a"
    if val >= 50:
        return "#ffd93d"
    return "#ff6b6b"


def verdict(r_local, r_api):
    """Return a verdict banner HTML based on results."""
    if not r_local or not r_api:
        return ""
    if not r_local["ok"] and not r_api["ok"]:
        return ""

    score_local = score_api = 0

    # Latency: lower is better
    if r_local["ok"] and r_api["ok"]:
        if r_local["latency"] < r_api["latency"]:
            score_local += 1
        else:
            score_api += 1

    # Confidence: higher is better
    cl = r_local.get("confidence") or 0
    ca = r_api.get("confidence") or 0
    if cl > ca:
        score_local += 1
    elif ca > cl:
        score_api += 1

    if score_local > score_api:
        return '<div class="verdict-banner verdict-local">🏆 VENCEDOR: OLMO-3 LOCAL — Melhor latência / confiança</div>'
    elif score_api > score_local:
        return f'<div class="verdict-banner verdict-api">🏆 VENCEDOR: {st.session_state.openai_model.upper()} API — Melhor latência / confiança</div>'
    else:
        return '<div class="verdict-banner verdict-tie">🤝 EMPATE — Desempenho equivalente</div>'


def render_metrics(r: dict, side: str):
    lat_html   = f'<span class="metric-chip chip-latency">⚡ {r["latency"]:.2f}s</span>'
    tok_html   = f'<span class="metric-chip chip-tokens">🪙 {r["total_tokens"]} tokens</span>'
    conf_val   = r.get("confidence")
    conf_label = f'{conf_val}%' if conf_val is not None else 'N/A'
    conf_html  = f'<span class="metric-chip chip-conf">🎯 {conf_label}</span>'
    return f'<div class="metrics-row">{lat_html}{tok_html}{conf_html}</div>'

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown("""
<div class="arena-header">
    <div class="arena-title">⚔️ LLM Battle Arena</div>
    <div class="arena-subtitle">Local Intelligence vs Cloud Power · Lógica Matemática</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# INPUT SECTION
# ──────────────────────────────────────────────
st.markdown('<div class="input-section">', unsafe_allow_html=True)
equation = st.text_area(
    "🧮 Digite sua equação ou problema matemático",
    placeholder="Ex: Resolva: 2x² + 5x - 3 = 0\nEx: Prove que √2 é irracional\nEx: Calcule a integral de x·sin(x)dx",
    height=90,
    key="equation_input",
)

col_btn1, col_btn2 = st.columns([3, 1])
with col_btn1:
    run_btn = st.button("⚔️  BATALHAR", use_container_width=True)
with col_btn2:
    clear_btn = st.button("🗑️  Limpar", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if clear_btn:
    st.session_state.result_local = None
    st.session_state.result_api   = None
    st.rerun()

# ──────────────────────────────────────────────
# RUN COMPARISON
# ──────────────────────────────────────────────
if run_btn and equation.strip():
    with st.spinner("⚔️ Batalha em andamento..."):
        col_prog1, col_prog2 = st.columns(2)
        with col_prog1:
            st.info(f"🟦 Consultando **{ollama_model}** local...")
        with col_prog2:
            st.info(f"🟣 Consultando **{openai_model}** via API...")

        # Run both concurrently using threads
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            fut_local = executor.submit(call_ollama, equation, system_prompt, ollama_model, ollama_url)
            fut_api   = executor.submit(call_openai, equation, system_prompt, openai_model, openai_key)
            r_local = fut_local.result()
            r_api   = fut_api.result()

    st.session_state.result_local = r_local
    st.session_state.result_api   = r_api

    # Save to history
    st.session_state.history.append({
        "equation": equation,
        "local": r_local,
        "api": r_api,
    })
    st.rerun()

elif run_btn:
    st.warning("⚠️ Digite uma equação antes de batalhar!")

# ──────────────────────────────────────────────
# RESULTS PANEL
# ──────────────────────────────────────────────
r_local = st.session_state.result_local
r_api   = st.session_state.result_api

col_left, col_mid, col_right = st.columns([10, 1, 10])

with col_left:
    st.markdown(f"""
    <div class="contestant-card card-local">
        <div class="card-title tag-local">🟦 {ollama_model.split(':')[0].upper()} — Local</div>
        <div class="card-model">ollama · {ollama_model} · localhost</div>
    </div>
    """, unsafe_allow_html=True)

    if r_local:
        content = r_local["text"] if r_local["ok"] else r_local["text"]
        st.markdown(f'<div class="response-box">{content}</div>', unsafe_allow_html=True)
        if r_local["ok"]:
            st.markdown(render_metrics(r_local, "local"), unsafe_allow_html=True)
    else:
        st.markdown('<div class="response-box"><span class="response-placeholder">A resposta do modelo local aparecerá aqui...</span></div>', unsafe_allow_html=True)

with col_mid:
    st.markdown('<div class="vs-divider"><div class="vs-badge">VS</div></div>', unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
    <div class="contestant-card card-api">
        <div class="card-title tag-api">🟣 {openai_model.split(':')[0].upper()} — API</div>
        <div class="card-model">openai · {openai_model} · cloud</div>
    </div>
    """, unsafe_allow_html=True)

    if r_api:
        content = r_api["text"] if r_api["ok"] else r_api["text"]
        st.markdown(f'<div class="response-box">{content}</div>', unsafe_allow_html=True)
        if r_api["ok"]:
            st.markdown(render_metrics(r_api, "api"), unsafe_allow_html=True)
    else:
        st.markdown('<div class="response-box"><span class="response-placeholder">A resposta da API aparecerá aqui...</span></div>', unsafe_allow_html=True)

# Verdict
if r_local and r_api:
    st.markdown(verdict(r_local, r_api), unsafe_allow_html=True)
