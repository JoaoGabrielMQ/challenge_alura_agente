import streamlit as st
from agente import AgentePesquisa
import uuid

st.set_page_config(page_title="Chat Santo Pegasus", page_icon="🤖", layout="wide")
st.markdown("<style>.stAppDeployButton { display: none !important; }</style>", unsafe_allow_html=True)
st.title("🤖 -- Assistente Santo Pegasus --")

if "id_conversa" not in st.session_state:
    st.session_state.id_conversa = str(uuid.uuid4())

if "agente_instancia" not in st.session_state:
    st.session_state.agente_instancia = AgentePesquisa()

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{
            "role": "assistant",
            "content": "Olá! Eu sou o assistente de pesquisa da Santo Pegasus. Como posso te ajudar hoje?"
        }]

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if pergunta := st.chat_input("Digite sua dúvida aqui..."):
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = st.session_state.agente_instancia.funcao_agente(pergunta, st.session_state.id_conversa)
            st.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})

with st.sidebar:
    if st.button("Nova conversa", type="primary", use_container_width=True):
        st.session_state.mensagens = [{
                "role": "assistant",
                "content": "Olá! Eu sou o assistente de pesquisa da Santo Pegasus. Como posso te ajudar hoje?"
            }]
        st.session_state.id_conversa = str(uuid.uuid4())
        st.rerun()

