import streamlit as st
from datetime import date
from fpdf import FPDF
import os
import pandas as pd
from core.sheets import gravar_cliente, ler_clientes

LOGO_PATH = "static/logo.png"
PDF_DIR = "generated_pdfs"
FONT_PATH = "static/fonts/Arial.ttf"
os.makedirs(PDF_DIR, exist_ok=True)

def formatar_nif(nif):
    nif = str(nif)
    if len(nif) == 9 and nif.isdigit():
        return f"{nif[:3]} {nif[3:6]} {nif[6:]}"
    return nif

def gerar_identificador(nif, nome):
    hoje = date.today().strftime("%d%m%Y")
    primeiro_nome = nome.split()[0] if nome else "Nome"
    return f"{nif}_{primeiro_nome}_{hoje}"

def gerar_pdf_documentos(nome, checklist):
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
    path = f"{PDF_DIR}/documentos_faltam_{nome.replace(' ', '_')}.pdf"
    pdf.output(path)
    return path

def carregar_cliente_existente(nif):
    df = ler_clientes()
    if not df.empty and str(nif) in df["NIF"].astype(str).values:
        cliente = df[df["NIF"].astype(str) == str(nif)].iloc[0].to_dict()
        return cliente
    return {}

def upsert_cliente(nif, cliente):
    df = ler_clientes()
    df["NIF"] = df["NIF"].astype(str)
    nif = str(nif)
    cliente_df = pd.DataFrame([cliente])
    if nif in df["NIF"].values:
        df = df[df["NIF"] != nif]
        df = pd.concat([df, cliente_df], ignore_index=True)
    else:
        df = pd.concat([df, cliente_df], ignore_index=True)
    gravar_cliente(df)
    return True

def proposta_titular(tipo_titular):
    st.title(f"{tipo_titular} – Dados")

    df_clientes = ler_clientes()
    modo = st.radio("Modo", ["Novo Cliente", "Editar Cliente"])
    cliente_data = {}

    if modo == "Editar Cliente" and not df_clientes.empty:
        df_clientes["label"] = df_clientes["Nome"] + " - " + df_clientes["NIF"].astype(str)
        escolha = st.selectbox("Selecionar Cliente", df_clientes["label"])
        cliente_data = df_clientes[df_clientes["label"] == escolha].iloc[0].to_dict()
        input_nome = cliente_data.get("Nome", "")
        input_nif = str(cliente_data.get("NIF", ""))
    else:
        input_nome = st.text_input("Nome Completo")
        input_nif = st.text_input("NIF").replace(" ", "")

    st.caption(f"NIF formatado: {formatar_nif(input_nif)}")

    tipo_rel = st.selectbox("Tipo", ["1º Titular", "2º Titular", "Avalista"])
    relacao_tit = st.text_input("Relação com o 1º Titular")

    col7, col8, col9 = st.columns(3)
    genero = col7.selectbox("Género", ["Masculino", "Feminino"])
    nascimento = col8.date_input("Data de Nascimento", min_value=date(1940, 1, 1))
    nacionalidade = col9.text_input("Nacionalidade")

    col10, col11, col12 = st.columns(3)
    estado_civil = col10.selectbox("Estado Civil", ["Casado", "Solteiro", "Divorciado", "Viúvo", "Separado"])
    dependentes = col11.number_input("Nº de Dependentes", min_value=0)
    habilitacoes = col12.selectbox("Habilitações", ["Primária", "Secundária", "Universitária"])

    st.subheader("Documento de Identificação")
    col1, col2, col3 = st.columns(3)
    tipo_doc = col1.selectbox("Tipo de Identificação", ["Cartão Cidadão", "Título residência", "Autorização residência"])
    num_ident = col2.text_input("Nº Identificação", max_chars=13)
    validade = col3.date_input("Data de Validade", min_value=date(2022, 1, 1))

    col4, col5, col6 = st.columns(3)
    entidade = col4.text_input("Entidade Emitente")
    pais_emissao = col5.text_input("País de Emissão")
    input_niss = col6.text_input("Nº Segurança Social", max_chars=11)

    st.subheader("Contactos")
    col13, col14, col15 = st.columns(3)
    cp = col13.text_input("Código Postal", placeholder="0000-000")
    morada = col14.text_input("Morada")
    porta = col15.text_input("Porta")
    col16, col17, col18 = st.columns(3)
    andar = col16.text_input("Andar")
    localidade = col17.text_input("Localidade")
    tipo_hab = col18.selectbox("Tipo Habitação", [
        "Arrendada", "Própria com hipoteca", "Própria sem hipoteca", "Familiares", "Sem domicilio"
    ])
    valor_mensal_hab = st.number_input("Valor Mensal Habitação (EUR)", min_value=0.0)

    col19, col20 = st.columns(2)
    telefone_fixo = col19.text_input("Telefone Fixo", max_chars=9)
    telemovel = col20.text_input("Telemóvel", max_chars=9)
    email = st.text_input("E-Mail")

    if input_nif and input_nome:
        identificador = gerar_identificador(input_nif, input_nome)
        st.text_input("Identificador da Proposta", value=identificador, disabled=True)

    st.subheader("Profissão")
    col21, col22 = st.columns(2)
    profissao = col21.text_input("Profissão")
    antiguidade = col22.date_input("Antiguidade", min_value=date(1940, 1, 1))

    col23, col24 = st.columns(2)
    contrato = col23.selectbox("Tipo de Contrato", ["Efetivo", "A prazo", "ENI", "Temporário", "Função pública"])
    empresa = col24.text_input("Nome da Empresa")

    col25, col26 = st.columns(2)
    telefone_emp = col25.text_input("Telefone da Empresa", max_chars=9)
    nipc = col26.text_input("NIPC", max_chars=9)

    col27, col28 = st.columns(2)
    cae = col27.text_input("CAE do Empregador", max_chars=5)
    atividade = col28.text_input("Atividade do Empregador")

    st.subheader("Rendimentos")
    duodecimos = st.selectbox("Duodécimos?", ["Sim", "Não"])
    colr1, colr2, colr3 = st.columns(3)
    rv1 = colr1.number_input("Recibo Mês -1", step=1.0)
    sa1 = colr1.number_input("Subsidio Mês -1", step=1.0)
    rv2 = colr2.number_input("Recibo Mês -2", step=1.0)
    sa2 = colr2.number_input("Subsidio Mês -2", step=1.0)
    rv3 = colr3.number_input("Recibo Mês -3", step=1.0)
    sa3 = colr3.number_input("Subsidio Mês -3", step=1.0)
    media_r = (rv1 + rv2 + rv3) / 3
    media_s = (sa1 + sa2 + sa3) / 3
    venc_a = media_r if duodecimos == "Sim" else (media_r * 14 / 12) + (media_s * 11 / 12)
    venc_b = (rv1 + sa1 + rv2 + sa2 + rv3 + sa3) / 3
    col_va, col_vb = st.columns(2)
    col_va.metric("Vencimento Líquido A (EUR)", f"{venc_a:.2f}")
    col_vb.metric("Vencimento Líquido B (EUR)", f"{venc_b:.2f}")

    st.subheader("🧾 IRS")
    ano_irs = st.selectbox("Último IRS", [str(ano) for ano in range(2022, date.today().year + 1)][::-1])
    cod_valid = st.text_input("Código Validação", max_chars=12)
    rend_irs = st.number_input("Valor rendimentos IRS (€)", min_value=0.0)

    st.subheader("Checklist de Documentos")
    docs = [
        "Identificação", "Comprovativo Morada", "Comprovativo IBAN", "3 Recibos",
        "3 Extratos Bancários", "Contrato Trabalho", "Declaração Início Atividade",
        "IRS", "Passaporte"
    ]
    checklist = []
    for doc in docs:
        col1, col2 = st.columns([1, 2])
        estado = col1.selectbox(f"{doc}", ["OK", "FALTA"], key=f"{tipo_titular}_{doc}")
        obs = col2.text_input(f"Observações {doc}", key=f"{tipo_titular}_{doc}_obs")
        checklist.append({"Documento": doc, "Estado": estado, "Observacoes": obs})

    st.markdown("---")
    col_b1, col_b2 = st.columns(2)
    if col_b1.button("💾 Gravar Cliente"):
        cliente = {
            "Nome": input_nome,
            "NIF": input_nif,
            "Tipo": tipo_rel,
            "Relacao": relacao_tit,
            "Nascimento": nascimento,
            "Género": genero,
            "Nacionalidade": nacionalidade,
            "Estado Civil": estado_civil,
            "Dependentes": dependentes,
            "Habilitações": habilitacoes,
            "Tipo Doc": tipo_doc,
            "Número Doc": num_ident,
            "Validade": validade,
            "Entidade": entidade,
            "País Emissão": pais_emissao,
            "NISS": input_niss,
            "Morada": morada,
            "Porta": porta,
            "Andar": andar,
            "Localidade": localidade,
            "Tipo Habitação": tipo_hab,
            "Valor Habitação": valor_mensal_hab,
            "Telefone": telefone_fixo,
            "Telemóvel": telemovel,
            "Email": email,
            "Profissão": profissao,
            "Antiguidade": antiguidade,
            "Contrato": contrato,
            "Empresa": empresa,
            "Telefone Empresa": telefone_emp,
            "NIPC": nipc,
            "CAE": cae,
            "Atividade": atividade,
            "Duodécimos": duodecimos,
            "IRS Ano": ano_irs,
            "Código IRS": cod_valid,
            "Rendimentos IRS": rend_irs
        }
        upsert_cliente(input_nif, cliente)
        st.success("✔️ Cliente gravado com sucesso!")

    if col_b2.button("📄 Gerar PDF de Faltas"):
        pdf_path = gerar_pdf_documentos(input_nome, checklist)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Baixar PDF", data=f, file_name=os.path.basename(pdf_path), mime="application/pdf")


