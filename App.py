import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Cadastro de Produtos", page_icon="\ud83d\udce6", layout="wide")

# Carregar credenciais do Streamlit Secrets
try:
    creds_json = json.loads(st.secrets["gspread"]["service_account"])
    SHEET_ID = st.secrets["gspread"]["sheet_id"]
    CREDS = Credentials.from_service_account_info(creds_json)
except Exception as e:
    st.error(f"Erro ao carregar credenciais: {e}")
    st.stop()

# Conectar ao Google Sheets
@st.cache_resource
def conectar_google_sheets():
    try:
        client = gspread.authorize(CREDS)
        spreadsheet = client.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet("Lista de Produtos")

        # Verifica se há cabeçalho, se não, adiciona
        if not worksheet.get_all_values():
            worksheet.append_row(["Nome", "Descrição", "Categoria", "Preço", "Quantidade", "Data Cadastro"])

        return worksheet
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")
        st.stop()

worksheet = conectar_google_sheets()

# Estilos da interface
st.markdown(
    """
    <style>
        .stApp { background-color: #f5f7fa; }
        .titulo { font-size: 32px; font-weight: bold; color: #333; text-align: center; }
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin: 10px;
        }
        .btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        .btn:hover {
            background-color: #45a049;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título da aplicação
st.markdown('<div class="titulo">\ud83d\udce6 Cadastro de Produtos</div>', unsafe_allow_html=True)

# Formulário de cadastro
st.markdown('<div class="card">', unsafe_allow_html=True)
with st.form("cadastro_produto", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome do Produto*", placeholder="Digite o nome")
        descricao = st.text_area("Descrição", placeholder="Detalhes do produto")
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
                novo_produto = [
                    nome,
                    descricao,
                    categoria,
                    preco,
                    quantidade,
                    datetime.now().strftime("%d/%m/%Y %H:%M")
                ]

                worksheet.append_row(novo_produto)
                st.success("✅ Produto cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao cadastrar produto: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Exibir produtos cadastrados
st.markdown('<div class="titulo">\ud83d\udccb Produtos Cadastrados</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

try:
    dados = worksheet.get_all_values()

    if len(dados) > 1:
        df = pd.DataFrame(dados[1:], columns=dados[0])
        st.dataframe(df, height=400, use_container_width=True)
    else:
        st.info("🔍 Nenhum produto cadastrado ainda.")
except Exception as e:
    st.error(f"Erro ao carregar produtos cadastrados: {e}")

st.markdown('</div>', unsafe_allow_html=True)


