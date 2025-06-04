import streamlit as st
from fpdf import FPDF
import os

LOGO_PATH = "static/logo.png"
PDF_DIR = "generated_pdfs"
FONT_PATH = "static/fonts/Arial.ttf"
os.makedirs(PDF_DIR, exist_ok=True)

def gerar_pdf_proposta(proposta):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", FONT_PATH, uni=True)
    pdf.set_font("Arial", size=12)

    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, 10, 8, 33)
    pdf.cell(200, 10, "Proposta Financeira", ln=True, align="C")
    pdf.ln(10)

    for secao, conteudo in proposta.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, secao, ln=True)
        pdf.set_font("Arial", "", 12)
        for k, v in conteudo.items():
            pdf.cell(200, 10, f"{k}: {v}", ln=True)
        pdf.ln(5)

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10,
        "Lendismart Unipessoal Lda\n"
        "N.º registo junto do Banco de Portugal: 0006212\n"
        "https://www.bportugal.pt/intermediariocreditofar/lendismart-unipessoal-lda"
    )

    path = f"{PDF_DIR}/proposta_{conteudo.get('Nome', 'sem_nome')}.pdf"
    pdf.output(path)
    return path

def run():
    st.title("📑 Geração de Proposta")

    cliente = st.text_input("Nome do Cliente")
    contacto = st.text_input("Contacto")
    email = st.text_input("E-mail")
    modelo = st.text_input("Modelo do Bem")
    pvp = st.number_input("Preço de Venda (EUR)", min_value=0.0, step=100.0)

    st.markdown("---")
    simulacao = st.session_state.get("simulacao", {})

    if simulacao:
        st.subheader("🧮 Simulação Aplicada")
        st.json(simulacao)
    else:
        st.warning("⚠️ Nenhuma simulação carregada.")

    st.markdown("---")
    if st.button("📄 Gerar Proposta PDF"):
        proposta = {
            "Cliente": {
                "Nome": cliente,
                "Contacto": contacto,
                "Email": email
            },
            "Bem": {
                "Modelo": modelo,
                "PVP": f"{pvp:.2f} €"
            },
            "Simulação": {
                k: f"{v:.2f} €" if isinstance(v, float) else v
                for k, v in simulacao.items()
            }
        }
        pdf_path = gerar_pdf_proposta(proposta)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Baixar Proposta", data=f, file_name=os.path.basename(pdf_path), mime="application/pdf")
