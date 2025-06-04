import streamlit as st
from fpdf import FPDF
import os
from core.sheets import gravar_bem, ler_bens, ler_stands

LOGO_PATH = "static/logo.png"
PDF_DIR = "generated_pdfs"
FONT_PATH = "static/fonts/Arial.ttf"
os.makedirs(PDF_DIR, exist_ok=True)

def gerar_pdf_bem(bem):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", FONT_PATH, uni=True)
    pdf.set_font("Arial", size=12)
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, 10, 8, 33)
    pdf.cell(200, 10, "Ficha Técnica do Bem", ln=True, align="C")
    pdf.ln(10)
    for k, v in bem.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10,
        "Lendismart Unipessoal Lda\n"
        "N.º registo junto do Banco de Portugal: 0006212\n"
        "https://www.bportugal.pt/intermediariocreditofar/lendismart-unipessoal-lda"
    )
    path = f"{PDF_DIR}/ficha_bem_{bem.get('Matrícula', 'sem_matricula')}.pdf"
    pdf.output(path)
    return path

def run():
    st.title("🚗 Cadastro de Bem")

    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    matricula = st.text_input("Matrícula")
    chassis = st.text_input("Nº Chassis")

    df_stands = ler_stands()
    nome_stand = None
    if not df_stands.empty:
        nome_stand = st.selectbox("Stand Associado", df_stands["Nome"].unique())

    dados_bem = {
        "Marca": marca,
        "Modelo": modelo,
        "Matrícula": matricula,
        "Chassis": chassis,
        "Stand": nome_stand
    }

    st.markdown("---")
    col1, col2 = st.columns(2)

    if col1.button("💾 Gravar Bem"):
        gravar_bem(dados_bem)
        st.success("✔️ Bem gravado com sucesso!")

    if col2.button("📄 Gerar Ficha PDF"):
        pdf_path = gerar_pdf_bem(dados_bem)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Baixar PDF", data=f, file_name=os.path.basename(pdf_path), mime="application/pdf")
