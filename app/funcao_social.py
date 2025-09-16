import streamlit as st
import plotly.express as px
import pandas as pd


# ========================filtro Sexualidade=============================================
def filtro_por_sexo(df, sexo):
    aux = []
    map_sexo = {
        "Masculino": 'M',
        "Feminino": 'F'
    }
    if len(sexo) > 0:
        for i in sexo:
            aux.append(map_sexo[i])
        df = df[df['TP_SEXO'].isin(aux)]
        return df
    else:
        return df

# ========================filtro idade===================================================
def filtro_por_idade(df, idade):
    aux = []
    map_idade = {
        "Menor de 17 anos": '1',
        "17 anos": '2',
        "18 anos": '3',
        "19 anos": '4',
        "20 anos": '5',
        "21 anos": '6',
        "22 anos": '7',
        "23 anos": '8',
        "24 anos": '9',
        "25 anos": '10',
        "Entre 26 e 30 anos": '11',
        "Entre 31 e 35 anos": '12',
        "Entre 36 e 40 anos": '13',
        "Entre 41 e 45 anos": '14',
        "Entre 46 e 50 anos": '15',
        "Entre 51 e 55 anos": '16',
        "Entre 56 e 60 anos": '17',
        "Entre 61 e 65 anos": '18',
        "Entre 66 e 70 anos": '19',
        "Maior de 70 anos": '20'
    }
    if len(idade) > 0:
        for i in idade:
            aux.append(map_idade[i])
        df = df[df['TP_FAIXA_ETARIA'].isin(aux)]
        return df
    else:
        return df
#=========================================================
def filtro_tipo_ensino(df, ensino):
    aux = []
    map_ensino = {
        'Ensino Regular':'1',
        'Educação Especial':'2',
        'Educação de Jovens e Adultos':'3'
    }
    if len(ensino) > 0:
        for i in ensino:
            aux.append(map_ensino[i])
        df = df[df['TP_ENSINO'].isin(aux)]
        return df
    else:
        return df
#=========================================================
def filtro_dependencia(df, dependencia):
    aux = []
    map_dependencia = {
    'Federal':'1',
    'Estadual':'2',
    'Municipal':'3',
    'Privada':'4'
    }
    if len(dependencia) > 0:
        for i in dependencia:
            aux.append(map_dependencia[i])
        df = df[df['TP_DEPENDENCIA_ADM_ESC'].isin(aux)]
        return df
    else:
        return df
#=========================================================
def filtro_zona(df,zona):
    aux = []
    map_zona = {
        'Urbana':'1',
        'Rural':'2'
        }
    if len(zona) > 0:
        for i in zona:
            aux.append(map_zona[i])
        df = df[df['TP_LOCALIZACAO_ESC'].isin(aux)]
        return df
    else:
        return df
#==========================================================================================================
def grafico_barra (df,coluna, col1, col2, tile, orientacao, map):
    if orientacao == 'h':
        info = df[coluna].map(map).value_counts().reset_index()
        info.columns = [col1 , col2]

        total = info[col2].sum()
        info["percentual"] = info[col2] / total * 100
        info["texto"] = info["percentual"].map("{:.2f}%".format)


        st.write(info)
        barra = px.bar(info,
                       x=col2,
                       y=col1,
                       title=tile,
                       color=None,
                       color_discrete_sequence=['Blue'],
                       orientation=orientacao,
                       text=info["texto"])
        barra.update_traces(textfont_size=15)
        barra.update_xaxes(title_text='')
        barra.update_yaxes(title_text='')
        barra.update_layout(autosize=True)
        return barra
    else:
        info = df[coluna].map(map).value_counts().reset_index()
        info.columns = [col1, col2]

        total = info[col2].sum()
        info["percentual"] = info[col2] / total * 100
        info["texto"] = info["percentual"].map("{:.2f}%".format)

        st.write(info)
        barra = px.bar(info,
                       x=col1,
                       y=col2,
                       color=None,
                       color_discrete_sequence=['Blue'],
                       title=tile,
                       orientation=orientacao,
                       text=info["texto"],
                       )

        barra.update_traces(textfont_size=15)
        barra.update_xaxes(title_text='')
        barra.update_yaxes(title_text='')
        barra.update_layout(autosize=True)
        return barra
#========================================================================================================
def grafico_pizza (df, coluna, col1, col2, tile, map):
    info = df[coluna].map(map).value_counts().reset_index()
    info.columns = [col1 , col2]
    cores_map = [
        '#FF6347',
        '#FFD700',
        '#90EE90'
    ]
    pizza = px.pie(info, names=col1, values=col2, color_discrete_sequence=cores_map, title=tile)

    return pizza