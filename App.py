import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Cadastro de Produtos", page_icon="📦", layout="wide")

# Autenticação no Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "C:\\Users\\Eriqu\\OneDrive\\Documentos\\Projeto-Cadastro\\delta-entity-451313-b4-3fd49c3a8c06.json"

try:
    CREDS = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
    CLIENT = gspread.authorize(CREDS)

    # ID da planilha do Google Sheets
    SHEET_ID = "1Nf-SB0j2lK_KrZRyyt2mrdemz3QHBCrReI2udmgzw4w"
    SHEET_NAME = "Lista de Produtos"  # Nome correto da aba

    # Abrir a planilha e a aba correta
    spreadsheet = CLIENT.open_by_key(SHEET_ID)
    worksheet = spreadsheet.worksheet(SHEET_NAME)
except Exception as e:
    st.error(f"Erro ao conectar com o Google Sheets: {e}")
    st.stop()

# Título da aplicação
st.title("📦 Sistema de Cadastro de Produtos")

# Formulário de cadastro
with st.form("cadastro_produto", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome do Produto*")
        descricao = st.text_area("Descrição")
        categoria = st.selectbox("Categoria*", ["Eletrônicos", "Vestuário", "Alimentos", "Livros", "Outros"])

    with col2:
        preco = st.number_input("Preço (R$)*", min_value=0.01, format="%.2f")
        quantidade = st.number_input("Quantidade em Estoque*", min_value=1, step=1)

    submitted = st.form_submit_button("Cadastrar Produto")

    if submitted:
        if not nome or not categoria:
            st.error("Preencha todos os campos obrigatórios (*)")
        else:
            try:
                # Criar nova linha de produto
                novo_produto = [
                    nome,
                    descricao,
                    categoria,
                    preco,
                    quantidade,
                    datetime.now().strftime("%d/%m/%Y %H:%M")
                ]

                # Adiciona no Google Sheets
                worksheet.append_row(novo_produto)

                st.success("Produto cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao cadastrar produto: {e}")

# Exibir produtos cadastrados
st.divider()
st.subheader("Produtos Cadastrados")

try:
    # Ler os dados do Google Sheets
    dados = worksheet.get_all_values()

    if len(dados) > 1:  # Se houver mais que o cabeçalho
        df = pd.DataFrame(dados[1:], columns=dados[0])  # Ignorar cabeçalhos
        st.dataframe(df)
    else:
        st.info("Nenhum produto cadastrado ainda.")
except Exception as e:
    st.error(f"Erro ao carregar produtos cadastrados: {e}")
