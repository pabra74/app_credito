import streamlit as st
import pandas as pd
from core.sheets import ler_propostas

def run():
    st.title("📁 Propostas Gravadas")

    df = ler_propostas()

    if df.empty:
        st.info("Nenhuma proposta foi encontrada.")
        return

    st.dataframe(df)

    filtro_nome = st.text_input("🔍 Filtrar por nome do cliente")
    if filtro_nome:
        df_filtrado = df[df["Nome"].str.contains(filtro_nome, case=False, na=False)]
        st.dataframe(df_filtrado)

    st.download_button(
        "📥 Baixar todas em Excel",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="propostas_lendismart.csv",
        mime="text/csv"
    )
