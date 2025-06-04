import streamlit as st
from core.sheets import gravar_lead

def run():
    st.title("📋 Cadastro de Lead")

    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone", max_chars=9)
    email = st.text_input("E-mail")
    origem = st.selectbox("Origem da Lead", ["Online", "Telefone", "Loja", "Indicação", "Outro"])
    interesse = st.text_area("Interesse / Notas")

    if st.button("💾 Gravar Lead"):
        lead = {
            "Nome": nome,
            "Telefone": telefone,
            "Email": email,
            "Origem": origem,
            "Interesse": interesse
        }
        gravar_lead(lead)
        st.success("✔️ Lead gravada com sucesso!")
