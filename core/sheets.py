import os
import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def conectar_sheet():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds_json = os.getenv("GOOGLE_CREDS_JSON")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    return client.open(sheet_name)

def gravar_cliente(dados_df):
    # Limpeza defensiva
    dados_df = dados_df.fillna("")  # Substitui NaNs por strings vazias
    dados_df.columns = dados_df.columns.astype(str)  # Garante que os nomes são strings
    dados_df = dados_df.astype(str)  # Converte todos os valores para string

    sh = conectar_sheet()
    ws = sh.worksheet("Clientes")
    ws.clear()
    ws.update([dados_df.columns.tolist()] + dados_df.values.tolist())

def ler_clientes():
    sh = conectar_sheet()
    ws = sh.worksheet("Clientes")
    data = ws.get_all_records()
    return pd.DataFrame(data)

def gravar_empresa(dados_dict):
    sh = conectar_sheet()
    ws = sh.worksheet("Empresas")
    ws.append_row(list(dados_dict.values()))

def ler_empresas():
    sh = conectar_sheet()
    ws = sh.worksheet("Empresas")
    data = ws.get_all_records()
    return pd.DataFrame(data)

def gravar_stand(dados_dict):
    sh = conectar_sheet()
    ws = sh.worksheet("Stands")
    ws.append_row(list(dados_dict.values()))

def ler_stands():
    sh = conectar_sheet()
    ws = sh.worksheet("Stands")
    data = ws.get_all_records()
    return pd.DataFrame(data)

def gravar_bem(dados_dict):
    sh = conectar_sheet()
    ws = sh.worksheet("Bens")
    ws.append_row(list(dados_dict.values()))

def ler_bens():
    sh = conectar_sheet()
    ws = sh.worksheet("Bens")
    data = ws.get_all_records()
    return pd.DataFrame(data)

def gravar_lead(dados_dict):
    sh = conectar_sheet()
    ws = sh.worksheet("Leads")
    ws.append_row(list(dados_dict.values()))

def gravar_decisao(dados_dict):
    sh = conectar_sheet()
    ws = sh.worksheet("Decisoes")
    ws.append_row(list(dados_dict.values()))

def ler_decisoes():
    sh = conectar_sheet()
    ws = sh.worksheet("Decisoes")
    data = ws.get_all_records()
    return pd.DataFrame(data)

def ler_propostas():
    try:
        sh = conectar_sheet()
        ws = sh.worksheet("Propostas")
        data = ws.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()
