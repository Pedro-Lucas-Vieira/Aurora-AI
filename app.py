# ============================================================
# AURORA AI
# Interface desenvolvida com Streamlit
# ============================================================

# Biblioteca do Streamlit
import streamlit as st

# Importa a função que conversa com a IA
from chatbot import responder


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="AURORA AI",
    page_icon="🤖",  # Substituído favicon por emoji
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS DA APLICAÇÃO
# ============================================================

st.markdown("""
<style>
.block-container{
    max-width:1100px;
    padding-top:2rem;
}

[data-testid="stHeader"]{
    background:transparent;
}

section[data-testid="stSidebar"]{
    background:#0F1B3D;
}

.sidebar-title{
    font-size:1.6rem;
    font-weight:bold;
    color:white;
}

.small{
    color:#B9B5C8;
}

.stButton>button{
    width:100%;
    border:none;
    border-radius:12px;
    background:#2563EB;
    color:white;
    font-weight:bold;
}

.stButton>button:hover{
    background:#3B82F6;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    # Substituída a imagem por um cabeçalho estilizado com emoji
    st.markdown(
        '<div class="sidebar-title">🤖 AURORA AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="small">Assistente Corporativo</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Áreas disponíveis")

    st.markdown("""
👥 Recursos Humanos

💰 Financeiro

🛡️ Compliance

💻 Tecnologia

📈 Comercial

📣 Comunicação

""")

    st.divider()

    st.subheader("Tecnologias")

    st.markdown("""
- Gemini 2.0 Flash
- Google Embeddings
- FAISS
- LangChain
- Streamlit
""")

    st.divider()

    # Botão para limpar o histórico
    if st.button("Limpar conversa"):
        st.session_state.mensagens = [
            {
                "role": "assistant",
                "content": """Olá!

Sou o **AURORA AI**.

Posso responder dúvidas sobre documentos internos da empresa.

Como posso ajudar?"""
            }
        ]
        st.rerun()


# ============================================================
# HISTÓRICO
# ============================================================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": """Olá!

Sou o **AURORA AI**.

Posso responder perguntas sobre:

- Recursos Humanos
- Financeiro
- Tecnologia
- Compliance
- Comercial
- Comunicação

Como posso ajudar?"""
        }
    ]


# ============================================================
# EXIBE AS MENSAGENS
# ============================================================

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])


# ============================================================
# RECEBE A PERGUNTA
# ============================================================

pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:
    # Salva pergunta
    st.session_state.mensagens.append(
        {
            "role": "user",
            "content": pergunta
        }
    )

    with st.chat_message("user"):
        st.markdown(pergunta)

    # Resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos..."):
            try:
                resposta = responder(pergunta)
            except Exception as erro:
                resposta = f"""
Ocorreu um erro.

Detalhes:
{erro}
"""
            st.markdown(resposta)

    st.session_state.mensagens.append(
        {
            "role": "assistant",
            "content": resposta
        }
    )