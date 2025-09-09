import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly.graph_objs import Figure

import edubasi
import plotly.express as px

def pagina_enem_social():
    edubasi.iniciar_sessao()
    
    st.title("Perspectiva Social")

    estado_civil = st.sidebar.multiselect(
        "Selecione estado civil:",
        ["Solteiro", "Casado", "Divorciado", "Viúvo"],
        placeholder="Selecione um município"
    )
    qtd = 0
    aux = []
    for ano in edubasi.obter_anos_selecionados():
        st.write(ano)
        df = edubasi.obter_dados(ano = ano, id_municipio = edubasi.obter_municipio_selecionado())
        aux.append(df)
        qtd += len(df)

    df = pd.concat(aux, ignore_index=True, sort=False)
    
    st.write("Município único selecionado:", edubasi.obter_municipio_selecionado())
    st.write("Municípios múltiplos selecionados:", edubasi.obter_municipios_selecionados())
    st.write("Quantidade de registros: " + str(qtd))
    st.write(df)

    def grafico_barra (coluna, col1, col2, tile, orientacao):
        if orientacao == 'h':
            info = df[coluna].value_counts().reset_index()
            info.columns = [col1 , col2]
            barra = px.bar(info, x=col2, y=col1, color=col2, title=tile, orientation=orientacao)
            return barra
        else:
            info = df[coluna].value_counts().reset_index()
            info.columns = [col1, col2]
            #st.write(info)
            barra = px.bar(info, x=col1, y=col2, color=col2, title=tile, orientation=orientacao)
            return barra
    def grafico_pizza (coluna, col1, col2, tile):
        info = df[coluna].value_counts().reset_index()
        info.columns = [col1 , col2]
        pizza = px.pie(info, names=col1, values=col2, color=col2, title=tile )
        return pizza

#============ tipo de depedencia ===========================
    pizza1 = grafico_pizza("TP_DEPENDENCIA_ADM_ESC",
                          "tipo_dependencia",
                          "quantidade",
                          'Tipos de Dependencias')
    st.plotly_chart(pizza1)

#============ Tipo de ensino ================================
    barra1 = grafico_barra('TP_ENSINO',
                             'tipo_de_ensino',
                             'quantidade',
                             'Tipo de ensino',
                             'v')
    st.plotly_chart(barra1)

#=========== zona territorial ==============================
    pizza2 = grafico_pizza('TP_LOCALIZACAO_ESC','tipo_de_zona', 'quantidade', 'Tipos de Zonas')
    st.plotly_chart(pizza2)

#=========== lingua estrangeira ============================
    barra2 = grafico_barra('TP_LINGUA',
                             'tipo_de_lingua',
                             'quantidade',
                             'Tipo de linguagem estrangeira escolhida',
                             'v')
    st.plotly_chart(barra2)

#=========== empregada domestica ===========================
    barra3 = grafico_barra('Q007',
                             'Possui_empregada',
                             'quantidade',
                             'Possue Empregada',
                             'v')
    st.plotly_chart(barra3)

#========== possui banheiro ===============================
    barra4 = grafico_barra('Q008',
                            'possui_banheiro',
                            'quantidade',
                            'Possuem Banheiro',
                            'h')
    st.plotly_chart(barra4)

#========== quartos ======================================

    barra5 = grafico_barra('Q009',
                            'possui_quantos_quartos',
                            'quantidade',
                            'Possui quantos quartos na casa ',
                            'h')
    st.plotly_chart(barra5)

#=========== prova treino ou não =========================
    pizza3 = grafico_pizza('IN_TREINEIRO',
                          'qual_modalidade',
                          'treino_ou_não',
                          'Tipo de Modalidade de Prova')
    st.plotly_chart(pizza3)

#========== automovel carro ==============================
    map = {

        "A": "Não.",
        "B": "Sim, um.",
        "C": "Sim, dois.",
        "D": "Sim, três.",
        "E": "Sim, quatro ou mais."
    }

    barra6 = grafico_barra('Q010',
                            'possui_carro',
                            'Resposta',
                            'Possuem Carro',
                            'h')
    st.plotly_chart(barra6)

#======== automovel moto =================================
    barra7 = grafico_barra('Q011',
                            'possui_moto',
                            'Resposta',
                            'Possuem Moto',
                            'h')
    st.plotly_chart(barra7)

#======== maquina de lavar ================================
    barra8 = grafico_barra('Q014',
                            'possui_lavar',
                            'Resposta',
                            'Possuem maquinas de lavar roupa',
                            'h')
    st.plotly_chart(barra8)

#============ internet ====================================
    pizza4 = grafico_pizza('Q025', 'possui_internet', 'Resposta', 'Possuem Internet')
    st.plotly_chart(pizza4)

#========= automoveis =====================================

    map = {

        "A": "Não.",
        "B": "Sim, um.",
        "C": "Sim, dois.",
        "D": "Sim, três.",
        "E": "Sim, quatro ou mais."
    }

    automovel = df["Q010"].map(map).value_counts().reset_index()
    automovel.columns = ['possui_automovel', 'Resposta']
    st.write(automovel)

#======== micro-ondas ======================================
    pizza5 = grafico_pizza("Q016", 'Possui micro-ondas', 'resposta', 'Possuem Micro-ondas')
    st.plotly_chart(pizza5)
#========= televisão =======================================
    pizza6 = grafico_pizza('Q019', 'Possui televisão de cor', 'resposta', 'Possuem televisão de cor')
    st.plotly_chart(pizza6)
#=========  celular ========================================
    barra9 = grafico_barra('Q022', 'Possui celular', 'resposta', 'Possuem Celular', 'h')
    st.plotly_chart(barra9)
#========= computador ======================================
    pizza7 = grafico_pizza('Q024', 'Possui computador', 'resposta', 'Possuem Computador')
    st.plotly_chart(pizza7)