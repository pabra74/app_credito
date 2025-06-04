import streamlit as st
from core.sheets import gravar_decisao, ler_decisoes
import pandas as pd
from datetime import date

def run():
    st.title("🧾 Decisão Financeira")

    nome = st.text_input("Nome do Cliente")
    nif = st.text_input("NIF", max_chars=9)
    decisao = st.radio("Decisão", ["Aprovado", "Reprovado", "Pendente"])
    justificativa = st.text_area("Justificação")
    data_decisao = st.date_input("Data da Decisão", value=date.today())

    if st.button("💾 Gravar Decisão"):
        dados = {
            "Nome": nome,
            "NIF": nif,
            "Decisão": decisao,
            "Justificação": justificativa,
            "Data": data_decisao.strftime("%Y-%m-%d")
        }
        gravar_decisao(dados)
        st.success("✔️ Decisão gravada com sucesso!")

    st.markdown("---")
    st.subheader("📋 Histórico de Decisões")

    df = ler_decisoes()
    if not df.empty:
        st.dataframe(df)
        st.download_button(
            "📥 Baixar decisões",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="decisoes_financeiras.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhuma decisão registrada ainda.")
