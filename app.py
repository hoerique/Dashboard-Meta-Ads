import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Sales Management Dashboard", layout="wide")

# Dados de exemplo
data = {
    "Product": ["Black Backpack", "Dano Backpack", "New Backpack", "Clutch Backpack"],
    "Category": ["Backpack", "Backpack", "Backpack", "Backpack"],
    "Price": [101, 144, 121, 300],
    "Status": ["Paid", "Unpaid", "Overdue", "Paid"],
    "Date": ["2022-07-02", "2022-07-03", "2022-07-04", "2022-07-05"]
}
df = pd.DataFrame(data)

# Sidebar para filtros
with st.sidebar:
    st.header("Filtros de Produtos")
    
    # Filtro por produto
    product_filter = st.multiselect(
        "Selecione os Produtos",
        options=df["Product"].unique(),  # Lista de produtos únicos
        default=df["Product"].unique()   # Mostrar todos os produtos por padrão
    )

# Aplicar filtro de produtos aos dados
filtered_df = df[df["Product"].isin(product_filter)]

# Título do Dashboard
st.title("Deshboard De Trafego Pago")
st.subheader("Sales Management Databases")

# Seção de boas-vindas e métricas
st.header("Welcome Back, Erique")
col1, col2, col3, col4 = st.columns(4)
col1.metric("impressões", "1,456", "+6.9% since last week")
col2.metric("investimento (R$)", "$3,345", "0.0% since last week")
col3.metric("Profit", "60%", "+0.2% since last week")
col4.metric("Invoices", "1,135", "+11.5% since last week")


# Seção de Record Invoices com dados filtrados
st.header("Record Invoices")
st.table(filtered_df)


# Título do gráfico
st.header("Gráfico de Linha - Vendas ao Longo do Tempo")

# Dados fictícios para o gráfico de linha
data = {
    "Date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
    "Sales": [200, 300, 150, 400, 350]  # Valores de vendas fictícios
}

# Criar um DataFrame com os dados
df = pd.DataFrame(data)

# Criar o gráfico de linha com Plotly
fig = px.line(
    df,  # DataFrame com os dados
    x="Date",  # Eixo X: datas
    y="Sales",  # Eixo Y: vendas
    title="Vendas ao Longo do Tempo",  # Título do gráfico
    labels={"Date": "Data", "Sales": "Vendas"},  # Rótulos dos eixos
    markers=True  # Adicionar marcadores aos pontos
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)





# Rodapé
st.write("Free")