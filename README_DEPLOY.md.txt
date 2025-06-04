# 🚀 Lendismart – Cloud Ready App

Sistema de gestão de propostas, leads, empresas e viaturas com PDFs e integração Google.

## ✅ Funcionalidades
- Titulares e Empresas com checklist de documentos
- Propostas automáticas com dados de simulação
- Simulador com cálculo de financiamento
- Uploads para Google Drive
- Geração de PDFs com logotipo e branding
- Google Sheets como base de dados

---

## 🌍 Publicar na Streamlit Cloud

### 📦 Pré-requisitos
1. Repositório no GitHub com esta estrutura.
2. `logo.png` e `Arial.ttf` dentro da pasta `static/`.

### 🔐 Segredos (.streamlit/secrets.toml)
```toml
GOOGLE_SHEET_NAME="LendismartDB"
GOOGLE_CREDS_JSON='{
  "type": "service_account",
  ...
}'
