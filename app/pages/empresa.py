import streamlit as st
from fpdf import FPDF
from datetime import date
import os
from core.sheets import gravar_empresa, ler_empresas

LOGO_PATH = "static/logo.png"
PDF_DIR = "generated_pdfs"
FONT_PATH = "static/fonts/Arial.ttf"
os.makedirs(PDF_DIR, exist_ok=True)

def gerar_pdf_empresa(nome, checklist):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", FONT_PATH, uni=True)
    pdf.set_font("Arial", size=12)
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, 10, 8, 33)
    pdf.cell(200, 10, f"Documentos em falta - {nome}".encode("latin-1", "replace").decode("latin-1"), ln=True, align="C")
    pdf.ln(5)
    pdf.set_text_color(255, 0, 0)
    for doc in checklist:
        if doc["Estado"] == "FALTA":
            linha = f"{doc['Documento']}: FALTA - {doc['Observacoes']}"
            pdf.cell(200, 10, linha.encode("latin-1", "replace").decode("latin-1"), ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10,
        "Lendismart Unipessoal Lda\n"
        "N.º registo junto do Banco de Portugal: 0006212\n"
        "https://www.bportugal.pt/intermediariocreditofar/lendismart-unipessoal-lda"
    )
    path = f"{PDF_DIR}/documentos_empresa_{nome.replace(' ', '_')}.pdf"
    pdf.output(path)
    return path

def run():
    st.title("🏢 Cadastro de Empresa")

    nome = st.text_input("Nome da Empresa")
    nif = st.text_input("NIF", max_chars=9)
    telefone = st.text_input("Telefone", max_chars=9)
    email = st.text_input("E-mail")
    atividade = st.text_input("Atividade")
    morada = st.text_input("Morada")
    localidade = st.text_input("Localidade")
    cod_postal = st.text_input("Código Postal", placeholder="0000-000")

    st.subheader("Checklist de Documentos")
    docs = ["NIF", "Certidão Comercial", "Declaração Inicio Atividade", "IRS", "IBAN", "CC/BI"]
    checklist = []
    for doc in docs:
        col1, col2 = st.columns([1, 2])
        estado = col1.selectbox(f"{doc}", ["OK", "FALTA"], key=f"empresa_{doc}")
        obs = col2.text_input(f"Observações {doc}", key=f"empresa_{doc}_obs")
        checklist.append({"Documento": doc, "Estado": estado, "Observacoes": obs})

    st.markdown("---")
    col1, col2 = st.columns(2)

    if col1.button("💾 Gravar Empresa"):
        dados = {
            "Nome": nome,
            "NIF": nif,
            "Telefone": telefone,
            "Email": email,
            "Atividade": atividade,
            "Morada": morada,
            "Localidade": localidade,
            "Código Postal": cod_postal
        }
        gravar_empresa(dados)
        st.success("✔️ Empresa gravada com sucesso!")

    if col2.button("📄 Gerar PDF de Faltas"):
        pdf_path = gerar_pdf_empresa(nome, checklist)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Baixar PDF", data=f, file_name=os.path.basename(pdf_path), mime="application/pdf")
