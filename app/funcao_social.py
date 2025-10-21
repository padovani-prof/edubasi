import streamlit as st
import plotly.express as px
import pandas as pd

def filtro_prova_treino(df, resp):
    if resp == True:
        return df
    elif resp == '1':
        df = df[df['IN_TREINEIRO'] == '1']
        return df
    else:
        df = df[df['IN_TREINEIRO'] == '0']
        return df
#=======================================================================================
def filtro_alunos_sem_escola(df, resp):
    if resp == True:
        return df
    else:
        vet = ['1', '2', '3']
        df = df[df['TP_ENSINO'].isin(vet)]
        return df

# ========================filtro Sexualidade=============================================
def filtro_multiselect(df, sexo, map, coluna):
    aux = []
    if len(sexo) > 0:
        for i in sexo:
            aux.append(map[i])
        df = df[df[coluna].isin(aux)]
        return df
    else:
        return df

def multicolunas(df, resp):
    if resp == 'Possui Nenhum':
        vet = [['A'], ['A']]
    elif resp == 'Possui Carro':
        vet = [['B','C','D','E'], ['A']]
    elif resp == 'Possui Moto':
        vet = [['A'], ['B','C','D','E']]
    elif resp == 'Possui Ambos':
        vet = [['B','C','D','E'], ['B','C','D','E']]
    else:
        return df
    df_filtrado = df[(df['Q010'].isin(vet[0])) & (df['Q011'].isin(vet[1]))]
    return df_filtrado



#-======================================graficos===========================================================
#==========================================================================================================
def grafico_barra(df, coluna, col1, col2, tile, orientacao, map=False):
    if map == True:
        info = df[coluna].map(map).value_counts().reset_index()
        info.columns = [col1, col2]
    else:
        info = df[coluna].value_counts().reset_index()
        info.columns = [col1, col2]

    #porcentagem
    total = info[col2].sum()
    info["percentual"] = info[col2] / total * 100
    info["Porcentagem"] = info["percentual"].map("{:.2f}%".format)

    #cores
    paleta = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    # Mapeia cores para cada categoria
    cores = {cat: paleta[i % len(paleta)] for i, cat in enumerate(info[col1].unique())}
    info["cor"] = info[col1].map(cores)

    #st.write(info)

    if orientacao == 'h':
        info=info.sort_values(by=col2, ascending=True, inplace=False).reset_index(drop=True)
        barra = px.bar(
            info,
            x=col2,
            y=col1,
            title=tile,
            orientation=orientacao,
            text=info["Porcentagem"]
        )
    else:
        barra = px.bar(
            info,
            x=col1,
            y=col2,
            title=tile,
            orientation=orientacao,
            text=info["Porcentagem"],
            height=600
        )

    # Aplica as cores manualmente (todas no mesmo trace)
    barra.update_traces(marker_color=info["cor"], width=0.7, textfont_size=18, hoverinfo='x')

    # Remove títulos de eixo
    barra.update_xaxes(title_text='')
    barra.update_yaxes(title_text='')

    # Ajusta layout para ocupar melhor o espaço
    barra.update_layout(
        autosize=True,
        bargap=0.05,
        bargroupgap=0.0,
        showlegend=False ,
        width=150,

    )

    return st.plotly_chart(barra, theme=None, use_container_width=True)
#========================================================================================================
def grafico_pizza (df, coluna, col1, col2, tile, map):
    info = df[coluna].map(map).value_counts().reset_index()
    info.columns = [col1 , col2]
    #st.write(info)
    cores_map = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    pizza = px.pie(info, names=col1, values=col2, color_discrete_sequence=cores_map, title=tile)
    pizza.update_traces(textfont_size=18)

    return st.plotly_chart(pizza, use_container_width=True)

def anos ():
    pass