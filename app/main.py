import streamlit as st
from dotenv import load_dotenv
import os

# Modules from pages
from pages.titular import proposta_titular
from app.pages.empresa import run as run_empresa
from app.pages.bem import run as run_bem
from app.pages.stand import run as run_stand
from app.pages.simulador import run as run_simulador
from app.pages.proposta import run as run_proposta
from app.pages.decisao_financeira import run as run_decisao_financeira
from app.pages.leads import run as run_leads
from app.pages.propostas_gravadas import run as run_propostas_gravadas

load_dotenv()

def main():
    st.set_page_config(page_title="Lendismart", layout="wide")

    st.sidebar.image("static/logo.png", width=220)
    st.sidebar.title("📊 Navegação")

    menu = st.sidebar.radio("Ir para:", [
        "Titular",
        "Empresa",
        "Bem",
        "Stand",
        "Simulador",
        "Proposta",
        "Decisões Financeiras",
        "Leads",
        "Propostas Gravadas"
    ])

    if menu == "Titular":
        proposta_titular("Titular Principal")
    elif menu == "Empresa":
        run_empresa()
    elif menu == "Bem":
        run_bem()
    elif menu == "Stand":
        run_stand()
    elif menu == "Simulador":
        run_simulador()
    elif menu == "Proposta":
        run_proposta()
    elif menu == "Decisões Financeiras":
        run_decisao_financeira()
    elif menu == "Leads":
        run_leads()
    elif menu == "Propostas Gravadas":
        run_propostas_gravadas()

if __name__ == "__main__":
    main()
