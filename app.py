import streamlit as st

st.set_page_config(page_title="Chat Santo Pegasus", page_icon="🤖", layout="wide")
st.title("🤖 -- Assistente Santo Pegasus --")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant",
         "content": "Olá! Sou o assistente virtual da Santo Pegasus. Como posso te ajudar?"}
    ]

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if pergunta := st.chat_input("Digite sua dúvida aqui..."):
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = f"Recebi sua mensagem: '{pergunta}'. A interface visual está funcionando 100%!"
            st.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})

with st.sidebar:
    if st.button("Nova conversa", type="primary", use_container_width=True):
        st.session_state.mensagens = []
        st.rerun()


