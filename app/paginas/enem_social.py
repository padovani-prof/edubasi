import streamlit as st
import pandas as pd
import funcao_social as fs
import edubasi


def pagina_enem_social():
    edubasi.iniciar_sessao()
    
    st.title("Perspectiva Social")

    qtd = 0
    aux = []
    for ano in edubasi.obter_anos_selecionados():
        st.write(ano)
        df = edubasi.obter_dados(ano = ano, id_municipio = edubasi.obter_municipio_selecionado())
        if True:
            df = df[df['CO_MUNICIPIO_ESC'] == edubasi.obter_municipio_selecionado()]
        aux.append(df)
        qtd += len(df)

    df = pd.concat(aux, ignore_index=True, sort=False)

    st.write("Município único selecionado:", edubasi.obter_municipio_selecionado())
    st.write("Municípios múltiplos selecionados:", edubasi.obter_municipios_selecionados())
    st.write("Quantidade de registros: " + str(qtd))


    Sexualidade = st.multiselect(
        "Selecione a sexualidade:",
        ['Masculino', "Feminino"],
        placeholder="Selecione uma sexualidade",
    )
    resultado = ", ".join(Sexualidade)
    st.write("Sexualidade:", resultado)
    df = fs.filtrar_por_sexo(df, resultado)

    idade = st.multiselect(
        "Selecione a idade:",
        ["Menor de 17 anos",
        "17 anos",
        "18 anos",
        "19 anos",
        "20 anos",
        "21 anos",
        "22 anos",
        "23 anos",
        "24 anos",
        "25 anos",
        "Entre 26 e 30 anos",
        "Entre 31 e 35 anos",
        "Entre 36 e 40 anos",
        "Entre 41 e 45 anos",
        "Entre 46 e 50 anos",
        "Entre 51 e 55 anos",
        "Entre 56 e 60 anos",
        "Entre 61 e 65 anos",
        "Entre 66 e 70 anos",
        "Maior de 70 anos"],
        placeholder="Selecione uma idade"
    )
    resultado1 = ", " .join(idade)
    st.write("Idades selecionadas:", resultado1)
    df = fs.filtrar_por_idade(df, idade)
    st.write(df)
    st.write(len(df))



#================== expander 1 ===================================================
#=================================================================================
    with st.expander("DADOS ESCOLARES"):
    #============ tipo de depedencia ===========================
        col1, col2 = st.columns(2)
        with col1:
            map={
                '1': "Federal",
                '2': "Estadual",
                '3': "Municipal",
                '4': "Privada"
            }
            pizza1 = fs.grafico_pizza(df,
                "TP_DEPENDENCIA_ADM_ESC",
                "Tipo de dependência",
                "Quantidade",
                'Tipo de dependência',
                map)
            pizza1.update_traces(textinfo='percent', textfont_size=14)
            st.plotly_chart(pizza1)
    # ============ Tipo de ensino ================================
        with col2:
            map = {
                '1': 'Urbana',
                '2': 'Rural'
            }
            pizza2 = fs.grafico_pizza(
                df,
                'TP_LOCALIZACAO_ESC',
                'tipo_de_zona',
                'quantidade',
                'Tipos de Zonas',
                map)
            st.plotly_chart(pizza2)
    # =========== zona territorial ==============================


        map = {
        '1': "Ensino Regular",
        '2': "Educação Especial - Modalidade Substitutiva",
        '3': "Educação de Jovens e Adultos"
        }
        barra1 = fs.grafico_barra(
            df,
            'TP_ENSINO',
            'tipo de ensino',
            'quantidade',
            'Tipo de ensino',
            'v',
            map)
        st.plotly_chart(barra1)
    # ================== expander 2 ===================================================
    # =================================================================================
    with st.expander("DADOS DA PROVA"):
    #=========== lingua estrangeira ============================
        map = {
            '0': "Inglês",
            '1': "Espanhol"
        }
        barra2 = fs.grafico_barra(
            df,
            'TP_LINGUA',
            'tipo_de_lingua',
            'quantidade',
            'Tipo de linguagem estrangeira escolhida',
            'v',
            map)
        st.plotly_chart(barra2)
    # =========== prova treino ou não =========================
        map = {
            '1':'Realizando prova para treino',
            '0':'Prova valendo pontuação'
    }
        pizza3 = fs.grafico_pizza(
            df,
            'IN_TREINEIRO',
            'qual_modalidade',
            'treino_ou_não',
            'Tipo de Modalidade de Prova',
            map)
        st.plotly_chart(pizza3)

# ================== expander 3 ===================================================
# =================================================================================
    with st.expander("DADOS SOBRE ELETRO-DOMESTICO"):
    # ======== maquina de lavar ================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra8 = fs.grafico_barra(
            df,
            'Q014',
            'possui quantas maquinas de lavar?',
            'Quantidade de respostas',
            'Possuem maquinas de lavar roupa',
            'h',
            map)
        st.plotly_chart(barra8)
    # ======== micro-ondas ======================================
        map = {
            "A": "Nenhum.",
            "B": "Um.",
            "C": "Dois.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        pizza5 = fs.grafico_pizza(
            df,
            "Q016",
            'Possui micro-ondas',
            'resposta',
            'Possuem Micro-ondas',
            map)
        st.plotly_chart(pizza5)
    # ========= televisão =======================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        pizza6 = fs.grafico_pizza(
            df,
            'Q019',
            'Possui televisão de cor',
            'resposta',
            'Possuem televisão de cor',
            map)
        st.plotly_chart(pizza6)

# ================== expander 4 ===================================================
# =================================================================================
    with st.expander('DADOS SOBRE VEICULOS'):
    # ======== automovel moto =================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra7 = fs.grafico_barra(
            df,
            'Q011',
            'possuem moto',
            'Quantas motos possuem',
            'Possuem Moto',
            'h',
            map)
        st.plotly_chart(barra7)

    # ========== automovel carro ==============================
        map = {
            "A": "Não.",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais."
        }
        barra6 = fs.grafico_barra(
            df,
            'Q010',
            'possuem carro',
            'Quantas carros possuem',
            'Possuem Carro',
            'h',
            map)
        st.plotly_chart(barra6)

    # ========= automoveis =====================================TESTE

        map = {

            "A": "Não.",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais."
        }

        automovel = df["Q010"].map(map).value_counts().reset_index()
        automovel.columns = ['possui_automovel', 'Resposta']
        #st.write(automovel)

# ================== expander 5 ===================================================
# =================================================================================
    with st.expander('DADOS SOBRE A MORADIA'):
    #=========== empregada domestica ===========================
        map = {
            "A": "Não.",
            "B": "Sim, um ou dois dias por semana.",
            "C": "Sim, três ou quatro dias por semana.",
            "D": "Sim, pelo menos cinco dias por semana."
        }
        barra3 = fs.grafico_barra(
            df,
            'Q007',
            'Possui empregada domestica',
            'quantidade',
            'Possue Empregada',
            'v',
            map)
        st.plotly_chart(barra3)
    #========== possui banheiro ===============================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra4 = fs.grafico_barra(
            df,
            'Q008',
            'possui_banheiro',
            'quantidade',
            'Possuem Banheiro',
            'h',
            map)
        st.plotly_chart(barra4)
    #========== quartos ======================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra5 = fs.grafico_barra(
            df,
            'Q009',
            'possui_quantos_quartos',
            'quantidade',
            'Possui quantos quartos na casa ',
            'h',
            map)
        st.plotly_chart(barra5)

# ================== expander 6 ===================================================
# =================================================================================
    with st.expander('DADOS APARELHOS DIGITAIS E INTERNET'):
    #============ internet ====================================
        map = {
            'A':'Não.',
            'B': 'Sim.'
    }
        pizza4 = fs.grafico_pizza(
            df,
            'Q025',
            'possuem internet',
            'Respostas',
            'Possuem Internet',
            map)
        st.plotly_chart(pizza4)
    #=========  celular ========================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra9 = fs.grafico_barra(
            df,
            'Q022',
            'Possui celular',
            'resposta',
            'Possuem Celular',
            'h',
            map)
        st.plotly_chart(barra9)
    #========= computador ======================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        pizza7 = fs.grafico_pizza(
            df,
            'Q024',
            'Possuem computador',
            'Quantos computadores possuem',
            'Possuem Computador',
            map)
        st.plotly_chart(pizza7)



