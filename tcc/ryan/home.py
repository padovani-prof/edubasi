import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(page_title="Dashboard | Microdados", layout="wide")
st.title("Dashboard | Microdados")

# =-=-=-=-=-= Sidebar =-=-=-=-=-=
st.sidebar.subheader('Procure os dados filtrados:')

def parametros_sidebar():
    ano = st.sidebar.selectbox("Selecione o ano:", ["2019", "2023", "Comparar"])
    return ano

# Carregando os dados filtrados
@st.cache_data
def carregar_dados():
    df2019 = pd.read_csv("MICRODADOS_ITA_2019_FILTRADO.csv")
    df2023 = pd.read_csv("MICRODADOS_ITA_2023_FILTRADO.csv")
    return df2019, df2023

df2019, df2023 = carregar_dados()

# Função para adicionar números sobre barras
def adicionar_valores(ax):
    for bar in ax.patches:
        ax.text(
            bar.get_x() + bar.get_width()/2,           # centraliza horizontalmente
            bar.get_height() + bar.get_height()*0.01,  # 1% acima da barra
            int(bar.get_height()),                      # valor inteiro
            ha='center', va='bottom'
        )

# =-=-=-=-=-= Corpo =-=-=-=-=-=
ano_escolhido = parametros_sidebar()
if ano_escolhido == "2019":
    st.header('Visualização dos Microdados de 2019')
    df = df2019

    # Gráfico de inscritos 2019
    st.subheader("Total de Inscritos (2019)")
    inscritos_2019 = len(df)
    fig, ax = plt.subplots(figsize=(5,5))
    ax.bar(["2019"], [inscritos_2019])
    adicionar_valores(ax)
    ax.set_ylabel("Quantidade de inscritos")
    st.pyplot(fig)

    # Gráficos distribuição por sexo e idade
    col1, col2 = st.columns(2)

    with col1:
        # Distribuição por Sexo (2019) em formato de pizza
        st.subheader("Distribuição por Sexo (2019)")
        # Contagem de cada sexo
        counts = df['TP_SEXO'].value_counts()
        # Criar gráfico de pizza
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
        ax.set_title('2019')
        # Exibir gráfico
        st.pyplot(fig)

    with col2:
        st.subheader("Distribuição por Idade (2019)")
        fig, ax = plt.subplots(figsize=(6,5))
        counts = df['TP_FAIXA_ETARIA'].value_counts()
        counts.plot(kind='bar', ax=ax)
        adicionar_valores(ax)
        st.pyplot(fig)

    # Dados filtrados
    st.header("Dados filtrados de 2019")
    st.dataframe(df2019.sample(20))

elif ano_escolhido == "2023":
    st.header('Visualização dos Microdados de 2023')
    df = df2023

    # Gráfico de inscritos 2023
    st.subheader("Total de Inscritos (2023)")
    inscritos_2023 = len(df)
    fig, ax = plt.subplots(figsize=(5,5))
    ax.bar(["2023"], [inscritos_2023])
    adicionar_valores(ax)
    ax.set_ylabel("Quantidade de inscritos")
    st.pyplot(fig)

    # Gráficos distribuição por sexo e idade
    col1, col2 = st.columns(2)

    with col1:
        # Distribuição por Sexo (2023) em formato de pizza
        st.subheader("Distribuição por Sexo (2023)")
        # Contagem de cada sexo
        counts = df['TP_SEXO'].value_counts()
        # Criar gráfico de pizza
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
        ax.set_title('2023')
        # Exibir gráfico
        st.pyplot(fig)

    with col2:
        st.subheader("Distribuição por Idade (2023)")
        fig, ax = plt.subplots(figsize=(6,5))
        counts = df['TP_FAIXA_ETARIA'].value_counts()
        counts.plot(kind='bar', ax=ax)
        adicionar_valores(ax)
        st.pyplot(fig)

    # Dados filtrados
    st.header("Dados filtrados de 2023")
    st.dataframe(df2023.sample(20))

else:  # Comparar
    st.header("Comparação dos Microdados de 2019 e 2023")

    # Comparação de inscritos
    st.subheader("Total de Inscritos")
    inscritos = pd.DataFrame({
        "Ano": ["2019", "2023"],
        "Inscritos": [len(df2019), len(df2023)]
    })
    fig, ax = plt.subplots(figsize=(7,5))
    inscritos.plot(kind='bar', x='Ano', y='Inscritos', ax=ax, legend=False)
    adicionar_valores(ax)
    ax.set_ylabel("Quantidade de inscritos")
    st.pyplot(fig)

    # Comparação por sexo em formato de pizza
    st.subheader("Distribuição por Sexo")
    # Contagem de cada sexo
    sexo2019 = df2019['TP_SEXO'].value_counts()
    sexo2023 = df2023['TP_SEXO'].value_counts()
    # Criar duas pizzas, uma para cada ano
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    # Pizza 2019
    axs[0].pie(sexo2019, labels=sexo2019.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
    axs[0].set_title('2019')
    # Pizza 2023
    axs[1].pie(sexo2023, labels=sexo2023.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
    axs[1].set_title('2023')
    # Exibir gráfico
    st.pyplot(fig)

    # Comparação por idade
    st.subheader("Distribuição por Idade")
    idade2019 = df2019['TP_FAIXA_ETARIA'].value_counts()
    idade2023 = df2023['TP_FAIXA_ETARIA'].value_counts()
    idade_comparacao = pd.DataFrame({'2019': idade2019, '2023': idade2023}).fillna(0)
    fig, ax = plt.subplots(figsize=(6,5))
    idade_comparacao.plot(kind='bar', ax=ax)
    adicionar_valores(ax)
    st.pyplot(fig)

    st.subheader("Dados filtrados de ambos os anos")
    st.dataframe(df2019.sample(20))
    st.dataframe(df2023.sample(20))
