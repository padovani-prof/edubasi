
import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar dados
def carregar_dados():
    df_2019 = pd.read_csv("MD_ITA_2019.csv", sep=";", encoding="latin1")
    df_2023 = pd.read_csv("MD_ITA_2023.csv", sep=";", encoding="latin1")
    return df_2019, df_2023

df_2019, df_2023 = carregar_dados()

# Adiciona coluna de ano e combina os dados dos dois anos para análise
df_2019["ANO"] = 2019
df_2023["ANO"] = 2023
df_final = pd.concat([df_2019, df_2023], ignore_index=True)

# -=-=-=-=-=-=-=-=-=-
# Criação da Barra Lateral
# -=-=-=-=-=-=-=-=-=-
st.sidebar.header("Filtros")

#Seleção dos filtros dos anos de 2019 e 2023
anos = st.sidebar.multiselect(
    "Selecione o(s) ano(s):",
    options=[2019, 2023],
    default=[2019, 2023]
)

# Filtra os dados de acordo com os anos selecionados
df_filtrado = df_final[df_final["ANO"].isin(anos)]

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Checkbox para incluir alunos sem escola e treineiros
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=

incluir_sem_escola = st.sidebar.checkbox(
    "Incluir alunos sem escola",
    value=True,
    help="Se desmarcado, alunos sem informação de escola não serão considerados."
)
# Filtro de alunos sem escola
if not incluir_sem_escola and "CO_MUNICIPIO_ESC" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["CO_MUNICIPIO_ESC"].notna()]

incluir_treineiros = st.sidebar.checkbox(
    "Incluir treineiros",
    value=True,
    help="Se desmarcado, alunos que são treineiros não serão considerados."
)
# Filtro de treineiros
if not incluir_treineiros and "IN_TREINEIRO" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["IN_TREINEIRO"] != 1]

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Título e cabeçalho
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
st.title("EDUBASI")
st.header("Análise Social")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Criação das abas Dados Gerais,
# pessoais, escolares de renda,
# moradia, transporte e aparelhos e tecnologias em casa
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
tabs = st.tabs([
    "Dados Gerais",
    "Dados Escolares",
    "Bens e Moradia",
    "Desempenho Geral"
])

# -=-=-=-=-=-=-=-=-=-=
# Dados gerais
# -=-=-=-=-=-=-=-=-=-=
with tabs[0]:
    # Alunos regulares
    df_regulares = df_filtrado[(df_filtrado["TP_ST_CONCLUSAO"] == 2) & (df_filtrado["ANO"].isin([2019, 2023]))]
    total_regulares = len(df_regulares)
    total_geral = len(df_filtrado[df_filtrado["ANO"].isin([2019, 2023])])

    col1, col2 = st.columns(2)
    col1.metric("Inscritos Gerais", f"{total_geral:,}".replace(",", "."))
    col2.metric("Regulares do Ensino Médio", f"{total_regulares:,}".replace(",", "."))

    # Gráfico
    df_inscritos = df_filtrado[df_filtrado["ANO"].isin([2019, 2023])]
    if not df_inscritos.empty:
        contagem = df_inscritos.groupby("ANO").size().reset_index(name="Quantidade")
        total = contagem["Quantidade"].sum()
        contagem["Percentual"] = (contagem["Quantidade"] / total * 100).round(2)

        # Texto com quantidade e percentual
        contagem["Texto"] = contagem.apply(lambda x: f"{x['Quantidade']} ({x['Percentual']}%)", axis=1)

        grafico = px.bar(
            contagem,
            x="ANO",
            y="Quantidade",
            text="Texto",
            title="Quantidade de inscritos no ENEM por ano",
            color="ANO"
        )

        grafico.update_traces(textposition="outside", width=0.4)
        grafico.update_xaxes(type="category")
        grafico.update_layout(coloraxis_showscale=False)

        st.plotly_chart(grafico)


        #-=-=-=-=-=-=-=-=-=-=-
        #Presentes por prova
        #-=-=-=-=-=-=-=-=-=-=-
        with st.expander("Presença dos alunos por prova"):
            st.subheader("Presença dos alunos por prova")

            # Calcula presença por ano
            provas = ["Natureza", "Humanas", "Linguagens", "Matemática", "Redação"]

            # Separa por ano dentro do df_filtrado
            df_2019 = df_filtrado[df_filtrado["ANO"] == 2019]
            df_2023 = df_filtrado[df_filtrado["ANO"] == 2023]

            pres_2019 = [
                (df_2019["TP_PRESENCA_CN"] == 1).sum(),
                (df_2019["TP_PRESENCA_CH"] == 1).sum(),
                (df_2019["TP_PRESENCA_LC"] == 1).sum(),
                (df_2019["TP_PRESENCA_MT"] == 1).sum(),
                (df_2019["TP_STATUS_REDACAO"].notna()).sum()
            ]

            pres_2023 = [
                (df_2023["TP_PRESENCA_CN"] == 1).sum(),
                (df_2023["TP_PRESENCA_CH"] == 1).sum(),
                (df_2023["TP_PRESENCA_LC"] == 1).sum(),
                (df_2023["TP_PRESENCA_MT"] == 1).sum(),
                (df_2023["TP_STATUS_REDACAO"].notna()).sum()
            ]

            # Cria dataframe simples
            df_plot = pd.DataFrame({
                "Prova": provas * 2,
                "Presentes": pres_2019 + pres_2023,
                "Ano": ["2019"] * 5 + ["2023"] * 5
            })

            # Percentual dentro do ano
            total_2019 = sum(pres_2019)
            total_2023 = sum(pres_2023)

            df_plot["Percentual"] = df_plot.apply(
                lambda row: round((row["Presentes"] / (total_2019 if row["Ano"] == "2019" else total_2023)) * 100, 1),
                axis=1
            )

            # Texto nas barras
            df_plot["Texto"] = df_plot["Presentes"].astype(str) + " (" + df_plot["Percentual"].astype(str) + "%)"

            # Gráfico simples
            grafico_prova_presentes = px.bar(
                df_plot,
                x="Prova",
                y="Presentes",
                color="Ano",
                barmode="group",
                text="Texto"
            )

            grafico_prova_presentes.update_traces(textposition="outside")
            st.plotly_chart(grafico_prova_presentes, use_container_width=True)

    # -=-=-=-=-=-=-=-=-=-=
    # Sexo dos Participantes
    # -=-=-=-=-=-=-=-=-=-=
    with st.expander("Sexo dos participantes"):
        st.subheader("Participantes por Sexo")

        # Mapa para os códigos de sexo
        mapa_sexo = {
            "M": "Masculino",
            "F": "Feminino"
        }

        # Contagem dos dados de 2019
        sexo_2019 = df_2019["TP_SEXO"].map(mapa_sexo).value_counts().reset_index()
        sexo_2019.columns = ["Sexo", "Quantidade"]
        sexo_2019["Ano"] = "2019"

        # Contagem dos dados de 2023
        sexo_2023 = df_2023["TP_SEXO"].map(mapa_sexo).value_counts().reset_index()
        sexo_2023.columns = ["Sexo", "Quantidade"]
        sexo_2023["Ano"] = "2023"

        # Junta os dois dataframes
        contagem_sexo = pd.concat([sexo_2019, sexo_2023])

        # Ordena (garantindo Masculino antes de Feminino, se quiser)
        ordem = ["Masculino", "Feminino"]
        contagem_sexo["Sexo"] = pd.Categorical(contagem_sexo["Sexo"], categories=ordem, ordered=True)
        contagem_sexo = contagem_sexo.sort_values("Sexo")

        # Cria duas colunas
        col1, col2 = st.columns(2)

        # Primeiro gráfico
        try:
            dados_ano1 = df_filtrado[df_filtrado["ANO"] == anos[0]].copy()
            dados_ano1["Sexo"] = dados_ano1["TP_SEXO"].map(mapa_sexo)

            graf1 = px.pie(
                dados_ano1,
                names="Sexo",
                hole=0.3,
                title=str(anos[0])
            )
            graf1.update_traces(textinfo='percent+label', hovertemplate='%{label}: %{percent}')
            col1.plotly_chart(graf1)

        except:
            col1.info("Sem dados para o primeiro ano")

        # Segundo gráfico
        try:
            dados_ano2 = df_filtrado[df_filtrado["ANO"] == anos[1]].copy()
            dados_ano2["Sexo"] = dados_ano2["TP_SEXO"].map(mapa_sexo)

            graf2 = px.pie(
                dados_ano2,
                names="Sexo",
                hole=0.3,
                title=str(anos[1])
            )
            graf2.update_traces(textinfo='percent+label', hovertemplate='%{label}: %{percent}')
            col2.plotly_chart(graf2)

        except:
            col2.info("Sem dados para o segundo ano")

        # -=-=-=-=-=-=-=-=-=-=
        # Gráfico de barras Sexo dos Participantes
        # -=-=-=-=-=-=-=-=-=-=
        st.subheader("Participantes por Sexo")
        mapa_sexo = {
            "M": "Masculino",
            "F": "Feminino"
        }

        # Contagem dos dados de 2019
        sexo_2019 = df_2019["TP_SEXO"].map(mapa_sexo).value_counts().reset_index()
        sexo_2019.columns = ["Sexo", "Quantidade"]
        sexo_2019["Ano"] = "2019"

        # Percentual 2019
        total_sexo_2019 = sexo_2019["Quantidade"].sum()
        sexo_2019["Percentual"] = (sexo_2019["Quantidade"] / total_sexo_2019 * 100).round(1)

        # Contagem dos dados de 2023
        sexo_2023 = df_2023["TP_SEXO"].map(mapa_sexo).value_counts().reset_index()
        sexo_2023.columns = ["Sexo", "Quantidade"]
        sexo_2023["Ano"] = "2023"

        # Percentual 2023
        total_sexo_2023 = sexo_2023["Quantidade"].sum()
        sexo_2023["Percentual"] = (sexo_2023["Quantidade"] / total_sexo_2023 * 100).round(1)

        # Junta os dois dataframes
        contagem_sexo = pd.concat([sexo_2019, sexo_2023])

        # Texto com quantidade e percentual
        contagem_sexo["Texto"] = contagem_sexo["Quantidade"].astype(str) + " (" + contagem_sexo["Percentual"].astype(
            str) + "%)"

        # gráfico de barras
        grafico_sexo = px.bar(
            contagem_sexo,
            x="Sexo",
            y="Quantidade",
            color="Ano",
            barmode="group",
            text="Texto"
        )

        grafico_sexo.update_traces(textposition="outside")
        grafico_sexo.update_layout(yaxis_title="Quantidade", xaxis_title="Sexo")

        st.plotly_chart(grafico_sexo)

    with st.expander("Faixa Etária"):
        st.subheader("Faixa Etária dos participantes")

        # Mapeamento OFICIAL do ENEM
        mapa_faixa_etaria = {
            1: "Menor de 17 anos",
            2: "17 anos",
            3: "18 anos",
            4: "19 anos",
            5: "20 anos",
            6: "21 anos",
            7: "22 anos",
            8: "23 anos",
            9: "24 anos",
            10: "25 anos",
            11: "Entre 26 e 30 anos",
            12: "Entre 31 e 35 anos",
            13: "Entre 36 e 40 anos",
            14: "Entre 41 e 45 anos",
            15: "Entre 46 e 50 anos",
            16: "Entre 51 e 55 anos",
            17: "Entre 56 e 60 anos",
            18: "Entre 61 e 65 anos",
            19: "Entre 66 e 70 anos",
            20: "Maior de 70 anos"
        }

        # Ordem correta das idades
        ordem_faixas = [mapa_faixa_etaria[i] for i in range(1, 20)]

        #Função para evitar a repetição de código desnecessário.
        def preparar(df, ano):
            tabela = df["TP_FAIXA_ETARIA"].value_counts().reset_index()
            tabela.columns = ["Faixa Etária", "Quantidade"]
            tabela["Faixa Etária"] = tabela["Faixa Etária"].map(mapa_faixa_etaria)
            tabela["Ano"] = ano
            total = tabela["Quantidade"].sum()
            tabela["Percentual"] = (tabela["Quantidade"] / total * 100).round(1)
            return tabela


        df19 = preparar(df_2019, "2019")
        df23 = preparar(df_2023, "2023")

        combinado = pd.concat([df19, df23])

        combinado["Faixa Etária"] = pd.Categorical(
            combinado["Faixa Etária"],
            categories=ordem_faixas,
            ordered=True
        )

        combinado = combinado.sort_values("Faixa Etária")

        # Texto
        combinado["Texto"] = combinado.apply(
            lambda x: f"{x['Quantidade']} ({x['Percentual']}%)",
            axis=1
        )

        grafico_fx_etaria = px.bar(
            combinado,
            x="Faixa Etária",
            y="Quantidade",
            color="Ano",
            barmode="group",
            text="Texto"
        )

        grafico_fx_etaria.update_traces(textposition="outside")

        st.plotly_chart(grafico_fx_etaria)

    # -=-=-=-=-=-=-=-=-=-=-=-
    # Gráfico Estado civil
    # -=-=-=-=-=-=-=-=-=-=-=-
    with st.expander("Estado Civil"):
        st.subheader("Estado Civil")
        dados_estado_civil = df_filtrado["TP_ESTADO_CIVIL"].dropna().unique()

        mapa_estado_civil = {
            0: "Não informado",
            1: "Solteiro(a)",
            2: "Casado(a)",
            3: "Divorciado(a)",
            4: "Viúvo(a)"
        }

        # Contagem dos dados de 2019
        estado_civil_2019 = df_2019["TP_ESTADO_CIVIL"].value_counts().reset_index()
        estado_civil_2019.columns = ["Estado Civil", "Quantidade"]
        estado_civil_2019["Estado Civil"] = estado_civil_2019["Estado Civil"].astype(int).map(mapa_estado_civil)
        estado_civil_2019["Ano"] = "2019"

        # Percentual 2019
        total_2019 = estado_civil_2019["Quantidade"].sum()
        estado_civil_2019["Percentual"] = (estado_civil_2019["Quantidade"] / total_2019 * 100).round(1)

        # Contagem dos dados de 2023
        estado_civil_2023 = df_2023["TP_ESTADO_CIVIL"].value_counts().reset_index()
        estado_civil_2023.columns = ["Estado Civil", "Quantidade"]
        estado_civil_2023["Estado Civil"] = estado_civil_2023["Estado Civil"].astype(int).map(mapa_estado_civil)
        estado_civil_2023["Ano"] = "2023"

        #Percentual 2023
        total_2023 = estado_civil_2023["Quantidade"].sum()
        estado_civil_2023["Percentual"] = (estado_civil_2023["Quantidade"] / total_2023 * 100).round(1)

        # Juntar os dois anos
        contagem_estado_civil = pd.concat([estado_civil_2019, estado_civil_2023])

        # Criar coluna de texto (Quantidade + Percentual)
        contagem_estado_civil["Texto"] = contagem_estado_civil.apply(
            lambda x: f"{x['Quantidade']} ({x['Percentual']}%)", axis=1
        )

        # gráfico de barras
        grafico_estado_civil = px.bar(
            contagem_estado_civil,
            x="Estado Civil",
            y="Quantidade",
            color="Ano",
            barmode="group",  # barras lado a lado
            text="Texto"
        )

        grafico_estado_civil.update_traces(textposition="outside")

        st.plotly_chart(grafico_estado_civil)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=
    # Cor/ Raça dos estudantes
    # -=-=-=-=-=-=-=-=-=-=-=-=-=
    with st.expander("Cor/Raça"):
        st.subheader("Distribuição por Cor/Raça")

        # Mapeamento numérico para nomes
        mapa_cor_raca = {
            0: "Não informado",
            1: "Branco(a)",
            2: "Preto(a)",
            3: "Pardo(a)",
            4: "Amarelo(a)",
            5: "Indígena",
            6: "Não dispõe da informação"
        }

        # Contagem dos dados de 2019
        cor_raca_2019 = df_2019["TP_COR_RACA"].value_counts().reset_index()
        cor_raca_2019.columns = ["Cor Raça", "Quantidade"]
        cor_raca_2019["Cor Raça"] = cor_raca_2019["Cor Raça"].astype(int).map(mapa_cor_raca)
        cor_raca_2019["Ano"] = "2019"

        # Percentual 2019
        total_2019 = cor_raca_2019["Quantidade"].sum()
        cor_raca_2019["Percentual"] = (cor_raca_2019["Quantidade"] / total_2019 * 100).round(1)

        # Contagem dos dados de 2023
        cor_raca_2023 = df_2023["TP_COR_RACA"].value_counts().reset_index()
        cor_raca_2023.columns = ["Cor Raça", "Quantidade"]
        cor_raca_2023["Cor Raça"] = cor_raca_2023["Cor Raça"].astype(int).map(mapa_cor_raca)
        cor_raca_2023["Ano"] = "2023"

        # Percentual 2023
        total_2023 = cor_raca_2023["Quantidade"].sum()
        cor_raca_2023["Percentual"] = (cor_raca_2023["Quantidade"] / total_2023 * 100).round(1)

        # Juntar os dois anos
        contagem_cor_raca = pd.concat([cor_raca_2019, cor_raca_2023])

        # Texto com quantidade e percentual
        contagem_cor_raca["Texto"] = contagem_cor_raca["Quantidade"].astype(str) + " (" + contagem_cor_raca[
            "Percentual"].astype(str) + "%)"

        # Gráfico de barras com texto
        grafico_cor_raca = px.bar(
            contagem_cor_raca,
            x="Cor Raça",
            y="Quantidade",
            color="Ano",
            barmode="group",
            text="Texto"
        )

        grafico_cor_raca.update_traces(textposition="outside")
        grafico_cor_raca.update_layout(yaxis_title="Quantidade de Estudantes", xaxis_title="Cor/Raça")

        st.plotly_chart(grafico_cor_raca)

    #=-=-=-=-=-=-=-=-=-=-=-=-=
    # Aba com os dados de Renda
    #=-=-=-=-=-=-=-=-=-=-=-=-=
    with st.expander("Renda dos Incritos"):
        st.subheader("Renda dos Incritos")

        mapa_renda = {
            "A": "Nenhuma renda",
            "B": "Até R$ 1.320,00",
            "C": "De R$ 1.320,01 até R$ 1.980,00",
            "D": "De R$ 1.980,01 até R$ 2.640,00",
            "E": "De R$ 2.640,01 até R$ 3.300,00",
            "F": "De R$ 3.300,01 até R$ 3.960,00",
            "G": "De R$ 3.960,01 até R$ 5.280,00.",
            "H": "De R$ 5.280,01 até R$ 6.600,00.",
            "I": "De R$ 6.600,01 até R$ 7.920,00",
            "J": "De R$ 7.920,01 até R$ 9.240,00",
            "K": "De R$ 9.240,01 até R$ 10.560,00",
            "L": "De R$ 10.560,01 até R$ 11.880,00",
            "M": "De R$ 11.880,01 até R$ 13.200,00",
            "N": "De R$ 13.200,01 até R$ 15.840,00",
            "O": "De R$ 15.840,01 até R$ 19.800,00",
            "P": "De R$ 19.800,01 até R$ 26.400,00",
            "Q": "Acima de R$ 26.400,00"
        }

        #-=-=-=-=- renda 2019
        renda_2019 = df_2019["Q006"].value_counts().reset_index()
        renda_2019.columns = ["Faixa", "Quantidade"]
        renda_2019["Renda"] = renda_2019["Faixa"].astype(str).map(mapa_renda)
        renda_2019["Ano"] = "2019"

        total_renda_2019 = renda_2019["Quantidade"].sum()
        renda_2019["Percentual"] = (renda_2019["Quantidade"] / total_renda_2019 * 100).round(1)

        #-=-=-=-=- renda 2023
        renda_2023 = df_2023["Q006"].value_counts().reset_index()
        renda_2023.columns = ["Faixa", "Quantidade"]
        renda_2023["Renda"] = renda_2023["Faixa"].astype(str).map(mapa_renda)
        renda_2023["Ano"] = "2023"

        total_renda_2023 = renda_2023["Quantidade"].sum()
        renda_2023["Percentual"] = (renda_2023["Quantidade"] / total_renda_2023 * 100).round(1)

        contagem_renda = pd.concat([renda_2019, renda_2023])

        # Criar label para exibição
        contagem_renda["Label"] = (
                contagem_renda["Quantidade"].astype(str)
                + " (" + contagem_renda["Percentual"].astype(str) + "%)"
        )

        # Ordenação correta
        ordem = list(mapa_renda.values())
        contagem_renda["Renda"] = pd.Categorical(
            contagem_renda["Renda"], categories=ordem, ordered=True
        )


        grafico_renda = px.bar(
            contagem_renda.sort_values("Renda"),
            x="Renda",
            y="Quantidade",
            color="Ano",
            barmode="group",
            text="Label"
        )

        grafico_renda.update_traces(textposition="outside")
        grafico_renda.update_layout(
            yaxis_title="Quantidade de Estudantes",
            xaxis_title="Renda",
            xaxis_tickangle=-45
        )

        st.plotly_chart(grafico_renda)

#-=-=-=-=-=-=-=-=-=-=-=-==-=-
# ABA DADOS ESCOLARES
#-=-=-=-=-=-=-=-=-=-=-=-=-=-
with tabs[1]:
    # =-=-=-=-=-=-=-=-=-=
    # ESCOLA
    # =-=-=-=-=-=-=-=-=-=
    with st.expander("Tipo de Escola"):
        st.subheader("Quantidade de inscritos por Tipo de Escola")

        mapa_escola = {
            1: "Federal",
            2: "Estadual",
            3: "Municipal",
            4: "Privada"
        }

        # Contagem dos dados de 2019
        escola_2019 = df_2019["TP_DEPENDENCIA_ADM_ESC"].value_counts().reset_index()
        escola_2019.columns = ["Escola", "Quantidade"]
        escola_2019["Escola"] = escola_2019["Escola"].astype(int).map(mapa_escola)
        escola_2019["Ano"] = "2019"

        #Percentual 2019
        total_escola_2019 = escola_2019["Quantidade"].sum()
        escola_2019["Percentual"] = (escola_2019["Quantidade"] / total_escola_2019 * 100).round(1)

        # Contagem dos dados de 2023
        escola_2023 = df_2023["TP_DEPENDENCIA_ADM_ESC"].value_counts().reset_index()
        escola_2023.columns = ["Escola", "Quantidade"]
        escola_2023["Escola"] = escola_2023["Escola"].astype(int).map(mapa_escola)
        escola_2023["Ano"] = "2023"

        #Percentual 2023
        total_escola_2023 = escola_2023["Quantidade"].sum()
        escola_2023["Percentual"] = (escola_2023["Quantidade"] / total_escola_2023 * 100).round(1)

        # Juntar os dois anos
        contagem_escola = pd.concat([escola_2019, escola_2023])

        # Criar texto com quantidade e percentual
        contagem_escola["Texto"] = contagem_escola["Quantidade"].astype(str) + " (" + contagem_escola[
            "Percentual"].astype(str) + "%)"

        # Gráfico de barras
        grafico_escola = px.bar(
            contagem_escola,
            x="Escola",
            y="Quantidade",
            color="Ano",
            text="Texto",
            barmode="group"
        )
        grafico_escola.update_traces(textposition="outside")
        grafico_escola.update_layout(yaxis_title="Quantidade", xaxis_title="Tipo de Escola")

        st.plotly_chart(grafico_escola)

    # =-=-=-=-=-=-=-=-=-=-=-=-=
    # Gráfico com o Tipo de Ensino
    # =-=-=-=-=-=-=-=-=-=-=-=-=
    with st.expander("Ensino"):
        st.subheader("Tipo de Ensino")

        mapa_ensino = {
            1: "Ensino Regular",
            2: "Educação Especial - Modalidade Substitutiva",
            3: "Educação de Jovens e Adultos (EJA)"
        }

        # Contagem dos dados de 2019
        ensino_2019 = df_2019["TP_ENSINO"].value_counts().reset_index()
        ensino_2019.columns = ["Tipo de Ensino", "Quantidade"]
        ensino_2019["Tipo de Ensino"] = ensino_2019["Tipo de Ensino"].astype(int).map(mapa_ensino)
        ensino_2019["Ano"] = "2019"

        total_ensino_2019 = ensino_2019["Quantidade"].sum()
        ensino_2019["Percentual"] = (ensino_2019["Quantidade"] / total_ensino_2019 * 100).round(1)

        # Contagem dos dados de 2023
        ensino_2023 = df_2023["TP_ENSINO"].value_counts().reset_index()
        ensino_2023.columns = ["Tipo de Ensino", "Quantidade"]
        ensino_2023["Tipo de Ensino"] = ensino_2023["Tipo de Ensino"].astype(int).map(mapa_ensino)
        ensino_2023["Ano"] = "2023"

        total_ensino_2023 = ensino_2023["Quantidade"].sum()
        ensino_2023["Percentual"] = (ensino_2023["Quantidade"] / total_ensino_2023 * 100).round(1)

        # Juntar os dois anos
        contagem_ensino = pd.concat([ensino_2019, ensino_2023])

        # Criar texto com quantidade e percentual
        contagem_ensino["Texto"] = contagem_ensino["Quantidade"].astype(str) + " (" + contagem_ensino[
            "Percentual"].astype(str) + "%)"

        # Gráfico
        grafico_ensino = px.bar(
            contagem_ensino,
            x="Tipo de Ensino",
            y="Quantidade",
            color="Ano",
            text="Texto",
            barmode="group"
        )

        grafico_ensino.update_traces(textposition="outside")
        grafico_ensino.update_layout(yaxis_title="Quantidade", xaxis_title="Tipo de Ensino")
        st.plotly_chart(grafico_ensino)

    # =-=-=-=-=-=-=-=-=-=-=-=-=
    # Gráfico com a Localização da Escola
    # =-=-=-=-=-=-=-=-=-=-=-=-=
    with st.expander("Localização da Escola"):
        st.subheader("Localização da Escola")

        # 1 = Urbana, 2 = Rural
        mapa_localizacao = {
            1: "Urbana",
            2: "Rural"
        }

        # Contagem dos dados de 2019
        localizacao_2019 = df_2019["TP_LOCALIZACAO_ESC"].value_counts().reset_index()
        localizacao_2019.columns = ["Localizacao Escola", "Quantidade"]
        localizacao_2019["Localizacao Escola"] = localizacao_2019["Localizacao Escola"].astype(int).map(
            mapa_localizacao)
        localizacao_2019["Ano"] = "2019"

        # Calcular percentual (em relação ao total de 2019)
        total_2019 = localizacao_2019["Quantidade"].sum()
        localizacao_2019["Percentual"] = (localizacao_2019["Quantidade"] / total_2019 * 100).round(1)

        # Contagem dos dados de 2023
        localizacao_2023 = df_2023["TP_LOCALIZACAO_ESC"].value_counts().reset_index()
        localizacao_2023.columns = ["Localizacao Escola", "Quantidade"]
        localizacao_2023["Localizacao Escola"] = localizacao_2023["Localizacao Escola"].astype(int).map(
            mapa_localizacao)
        localizacao_2023["Ano"] = "2023"

        # Calcular percentual (em relação ao total de 2023)
        total_2023 = localizacao_2023["Quantidade"].sum()
        localizacao_2023["Percentual"] = (localizacao_2023["Quantidade"] / total_2023 * 100).round(1)

        # Juntar os dois anos
        contagem_localizacao = pd.concat([localizacao_2019, localizacao_2023]).reset_index(drop=True)

        # Criar coluna com texto formatado (quantidade + percentual)
        contagem_localizacao["Texto"] = (contagem_localizacao["Quantidade"].astype(str) + " (" + contagem_localizacao["Percentual"].astype(str) + "%)")

        # Gráfico de barras
        grafico_localizacao = px.bar(
            contagem_localizacao,
            x="Localizacao Escola",
            y="Quantidade",
            color="Ano",
            text="Texto",
            barmode="group"  # barras lado a lado
        )

        grafico_localizacao.update_traces(textposition="outside")
        grafico_localizacao.update_layout(yaxis_title="Quantidade de Escolas")

        st.plotly_chart(grafico_localizacao)

#-=-=-=-=-=-=--=-=-=-=-=
# Dados de Moradia
#-=-=-=-=-=-=--=-=-=-=-=
with tabs[2]:
    #-=-=-=-=-=-=
    #Gráfico celular em casa
    #=-=-=-=-=-=-
    with st.expander("Celular"):
        st.subheader("Celulares em casa")
        mapa_celulares = {
            "A": "Nenhum",
            "B": "Um",
            "C": "Dois",
            "D": "Três",
            "E": "Quatro ou mais"
        }

        # Contagem dos dados dos filtros de 2019
        celulares_2019 = df_2019["Q011"].value_counts().reset_index()
        celulares_2019.columns = ["Celulares", "Quantidade"]
        celulares_2019["Celulares"] = celulares_2019["Celulares"].astype(str).map(mapa_celulares)
        celulares_2019["Ano"] = "2019"
        # Percentual 2023
        total_celulares_2019 = celulares_2019["Quantidade"].sum()
        celulares_2019["Percentual"] = (celulares_2019["Quantidade"] / total_celulares_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        celulares_2023 = df_2023["Q011"].value_counts().reset_index()
        celulares_2023.columns = ["Celulares", "Quantidade"]
        celulares_2023["Celulares"] = celulares_2023["Celulares"].astype(str).map(mapa_celulares)
        celulares_2023["Ano"] = "2023"
        # Percentual 2023
        total_celulares_2023 = celulares_2023["Quantidade"].sum()
        celulares_2023["Percentual"] = (celulares_2023["Quantidade"] / total_celulares_2023 * 100).round(1)

        # Juntar os dois
        contagem_celulares = pd.concat([celulares_2019, celulares_2023])

        # Texto com quantidade e percentual
        contagem_celulares["Texto"] = contagem_celulares["Quantidade"].astype(str) + " (" + contagem_celulares["Percentual"].astype(
            str) + "%)"

        grafico_celulares = px.bar(
            contagem_celulares,
            x="Celulares",
            y="Quantidade",
            color="Ano",
            text="Texto",
            barmode="group"  # barras lado a lado
        )
        grafico_celulares.update_traces(textposition="outside")
        grafico_celulares.update_layout(yaxis_title="Quantidade", xaxis_title="Celulares")

        st.plotly_chart(grafico_celulares)

    #-=-=-=-=-=-=
    # Computador em casa
    #=-=-=-=-=-=-
    with st.expander("Computadores"):
        st.subheader("Computadores em casa")
        mapa_computadores = {
            "A": "Nenhum",
            "B": "Um",
            "C": "Dois",
            "D": "Três",
            "E": "Quatro ou mais"
        }

        # Contagem dos dados dos filtros de 2019
        computadores_2019 = df_2019["Q024"].value_counts().reset_index()
        computadores_2019.columns = ["Computadores", "Quantidade"]
        computadores_2019["Computadores"] = computadores_2019["Computadores"].astype(str).map(mapa_computadores)
        computadores_2019["Ano"] = "2019"
        # Percentual 2019
        total_computadores_2019 = computadores_2019["Quantidade"].sum()
        computadores_2019["Percentual"] = (computadores_2019["Quantidade"] / total_computadores_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        computadores_2023 = df_2023["Q024"].value_counts().reset_index()
        computadores_2023.columns = ["Computadores", "Quantidade"]
        computadores_2023["Computadores"] = computadores_2023["Computadores"].astype(str).map(mapa_computadores)
        computadores_2023["Ano"] = "2023"
        # Percentual 2023
        total_computadores_2023 = computadores_2023["Quantidade"].sum()
        computadores_2023["Percentual"] = (computadores_2023["Quantidade"] / total_computadores_2023 * 100).round(1)

        # Juntar os dois
        contagem_computadores = pd.concat([computadores_2019, computadores_2023])

        # Texto com quantidade e percentual
        contagem_computadores["Texto"] = contagem_computadores["Quantidade"].astype(str) + " (" + contagem_computadores["Percentual"].astype(
            str) + "%)"

        grafico_computadores = px.bar(
            contagem_computadores,
            x="Computadores",
            y="Quantidade",
            color="Ano",
            text="Texto",
            barmode="group"  # barras lado a lado
        )

        grafico_computadores.update_traces(textposition="outside")
        grafico_computadores.update_layout(yaxis_title="Quantidade", xaxis_title="Computadores")
        st.plotly_chart(grafico_computadores)

    #-=-=-=-=-=-=-=-=
    # Internet em casa
    #-=-==-=-=-=-=-=
    with st.expander("Internet"):
        st.subheader("Internet em casa")
        mapa_internet = {
            "A": "Não",
            "B": "Sim"
        }

        # Contagem dos dados dos filtros de 2019
        internet_2019 = df_2019["Q025"].value_counts().reset_index()
        internet_2019.columns = ["Internet", "Quantidade"]
        internet_2019["Internet"] = internet_2019["Internet"].astype(str).map(mapa_internet)
        internet_2019["Ano"] = "2019"

        # Percentual 2023
        total_internet_2019 = internet_2019["Quantidade"].sum()
        internet_2019["Percentual"] = (internet_2019["Quantidade"] / total_internet_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        internet_2023 = df_2023["Q025"].value_counts().reset_index()
        internet_2023.columns = ["Internet", "Quantidade"]
        internet_2023["Internet"] = internet_2023["Internet"].astype(str).map(mapa_internet)
        internet_2023["Ano"] = "2023"

        # Percentual 2023
        total_internet_2023 = internet_2023["Quantidade"].sum()
        internet_2023["Percentual"] = (internet_2023["Quantidade"] / total_internet_2023 * 100).round(1)

        # Juntar os dois
        contagem_internet = pd.concat([internet_2019, internet_2023])

        # Texto com quantidade e percentual
        contagem_internet["Total"] = contagem_internet["Quantidade"].astype(str) + "(" + contagem_internet[
            "Percentual"].astype(
            str) + "%)"

        grafico_internet = px.bar(
            contagem_internet,
            x="Internet",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"  # barras lado a lado
        )

        grafico_internet.update_traces(textposition="outside")
        grafico_internet.update_layout(yaxis_title="Quantidade", xaxis_title="Computadores")
        st.plotly_chart(grafico_internet)

    #-=-=-=-=-=-=-=-=-=-=-=-=-=
    #Televisão em Casa
    #-=-=-=-=-=-=-=-=-=-=-=-=-=
    with st.expander("Televisão"):
        st.subheader("Televisão em Casa")
        mapa_tv = {
            "A":"Não",
            "B":"Sim, uma",
            "C":"Sim, duas",
            "D":"Sim, quatro ou mais"
        }

        # Contagem dos dados dos filtros de 2019
        tv_2019 = df_2019["Q019"].value_counts().reset_index()
        tv_2019.columns = ["Televisão em casa", "Quantidade"]
        tv_2019["Televisão em casa"] = tv_2019["Televisão em casa"].astype(str).map(mapa_tv)
        tv_2019["Ano"] = "2019"
        # Percentual 2019
        total_tv_2019 = tv_2019["Quantidade"].sum()
        tv_2019["Percentual"] = (tv_2019["Quantidade"] / total_tv_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        tv_2023 = df_2023["Q019"].value_counts().reset_index()
        tv_2023.columns = ["Televisão em casa", "Quantidade"]
        tv_2023["Televisão em casa"] = tv_2023["Televisão em casa"].astype(str).map(mapa_tv)
        tv_2023["Ano"] = "2023"
        # Percentual 2023
        total_tv_2023 = tv_2023["Quantidade"].sum()
        tv_2023["Percentual"] = (tv_2023["Quantidade"] / total_tv_2023 * 100).round(1)

        # Juntar os dois
        contagem_tv = pd.concat([tv_2019, tv_2023])

        # Texto com quantidade e percentual
        contagem_tv["Total"] = contagem_tv["Quantidade"].astype(str) + "(" + contagem_tv[
            "Percentual"].astype(
            str) + "%)"

        grafico_tv = px.bar(
            contagem_tv,
            x="Televisão em casa",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"  # barras lado a lado
        )

        grafico_tv.update_traces(textposition="outside")
        grafico_tv.update_layout(yaxis_title="Quantidade", xaxis_title="Televisão em casa")
        st.plotly_chart(grafico_tv)

    # -=-=-=-=-=-=-=-=-=-=-=-
    # Empregado(a)
    # -=-=-=-=-=-=-=-=-=-=-=-
    with st.expander("Empregado(a) Doméstico(a)"):
        st.subheader("Empregado(a) Doméstico(a)")
        mapa_empregado = {
            "A": "Não",
            "B": "Sim, um ou dois dias por semana",
            "C": "Sim, três ou quatro dias por semana",
            "D": "Sim, pelo menos cinco dias por semana"
        }

        # Contagem dos dados dos filtros de 2019
        empregado_2019 = df_2019["Q007"].value_counts().reset_index()
        empregado_2019.columns = ["Empregado", "Quantidade"]
        empregado_2019["Empregado"] = empregado_2019["Empregado"].astype(str).map(mapa_empregado)
        empregado_2019["Ano"] = "2019"
        # Percentual 2019
        total_empregado_2019 = empregado_2019["Quantidade"].sum()
        empregado_2019["Percentual"] = (empregado_2019["Quantidade"] / total_empregado_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        empregado_2023 = df_2023["Q007"].value_counts().reset_index()
        empregado_2023.columns = ["Empregado", "Quantidade"]
        empregado_2023["Empregado"] = empregado_2023["Empregado"].astype(str).map(mapa_empregado)
        empregado_2023["Ano"] = "2023"
        # Percentual 2023
        total_empregado_2023 = empregado_2023["Quantidade"].sum()
        empregado_2023["Percentual"] = (empregado_2023["Quantidade"] / total_empregado_2023 * 100).round(1)

        # Juntar os dois
        contagem_empregado = pd.concat([empregado_2019, empregado_2023])

        # Texto com quantidade e percentual
        contagem_empregado["Total"] = contagem_empregado["Quantidade"].astype(str) + "(" + contagem_empregado[
            "Percentual"].astype(
            str) + "%)"

        grafico_empregado = px.bar(
            contagem_empregado,
            x="Empregado",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"  # barras lado a lado
        )

        grafico_empregado.update_traces(textposition="outside")
        grafico_empregado.update_layout(yaxis_title="Quantidade", xaxis_title="Empregado")
        st.plotly_chart(grafico_empregado)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=
    # Dados de moradia
    # -=-=-=-=-=-=-=-=-=-=-=-=-=
    with st.expander("Dados de Moradia"):
        st.subheader("Dados de Moradia")
        # Mapeamento de pessoas que moram na mesma casa
        mapa_moradia = {
            1: "1 pessoa",
            2: "2 pessoas",
            3: "3 pessoas",
            4: "4 pessoas",
            5: "5 pessoas",
            6: "6 pessoas",
            7: "7 pessoas",
            8: "8 pessoas",
            9: "9 pessoas",
            10: "10 pessoas",
            11: "11 pessoas",
            12: "12 pessoas",
            13: "13 pessoas",
            14: "14 pessoas",
            15: "15 pessoas",
            16: "16 pessoas",
            17: "17 pessoas",
            18: "18 pessoas ou mais"
        }

        # Contagem dos dados dos filtros de 2019
        moradia_2019 = df_2019["Q005"].value_counts().reset_index()
        moradia_2019.columns = ["Moradores", "Quantidade"]
        moradia_2019["Moradores"] = moradia_2019["Moradores"].astype(int).map(mapa_moradia)
        moradia_2019["Ano"] = "2019"
        # Percentual 2019
        total_moradia_2019 = moradia_2019["Quantidade"].sum()
        moradia_2019["Percentual"] = (moradia_2019["Quantidade"] / total_moradia_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        moradia_2023 = df_2023["Q005"].value_counts().reset_index()
        moradia_2023.columns = ["Moradores", "Quantidade"]
        moradia_2023["Moradores"] = moradia_2023["Moradores"].astype(int).map(mapa_moradia)
        moradia_2023["Ano"] = "2023"
        # Percentual 2023
        total_moradia_2023 = moradia_2023["Quantidade"].sum()
        moradia_2023["Percentual"] = (moradia_2023["Quantidade"] / total_moradia_2023 * 100).round(1)

        # Juntar os dois
        contagem_moradia = pd.concat([moradia_2019, moradia_2023])

        # Texto com quantidade e percentual
        contagem_moradia["Total"] = contagem_moradia["Quantidade"].astype(str) + "(" + contagem_moradia[
            "Percentual"].astype(
            str) + "%)"

        grafico_moradia = px.bar(
            contagem_moradia,
            x="Moradores",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"  # barras lado a lado
        )

        grafico_moradia.update_traces(textposition="outside")
        grafico_moradia.update_layout(yaxis_title="Quantidade", xaxis_title="Moradores")
        st.plotly_chart(grafico_moradia)

    # -==-=-==-=-=-=-=-=-=-=
    # Quartos em casa
    # -==-=-==-=-=-=-=-=-=-=
    with st.expander("Quartos em casa"):
        st.subheader("Quartos em casa")
        mapa_quartos = {
            "A": "Não",
            "B": "Um",
            "C": "Dois",
            "D": "Três",
            "E": "Quatro ou mais"
        }

        # Contagem dos dados dos filtros de 2019
        quarto_2019 = df_2019["Q009"].value_counts().reset_index()
        quarto_2019.columns = ["Quartos", "Quantidade"]
        quarto_2019["Quartos"] = quarto_2019["Quartos"].astype(str).map(mapa_quartos)
        quarto_2019["Ano"] = "2019"
        # Percentual 2023
        total_quarto_2019 = quarto_2019["Quantidade"].sum()
        quarto_2019["Percentual"] = (quarto_2019["Quantidade"] / total_quarto_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        quarto_2023 = df_2023["Q009"].value_counts().reset_index()
        quarto_2023.columns = ["Quartos", "Quantidade"]
        quarto_2023["Quartos"] = quarto_2023["Quartos"].astype(str).map(mapa_quartos)
        quarto_2023["Ano"] = "2023"
        # Percentual 2023
        total_quarto_2023 = quarto_2023["Quantidade"].sum()
        quarto_2023["Percentual"] = (quarto_2023["Quantidade"] / total_moradia_2023 * 100).round(1)

        # Juntar os dois
        contagem_quarto = pd.concat([quarto_2019, quarto_2023])

        # Texto com quantidade e percentual
        contagem_quarto["Total"] = contagem_quarto["Quantidade"].astype(str) + "(" + contagem_quarto[
            "Percentual"].astype(
            str) + "%)"

        grafico_quarto = px.bar(
            contagem_quarto,
            x="Quartos",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"  # barras lado a lado
        )

        grafico_quarto.update_traces(textposition="outside")
        grafico_quarto.update_layout(yaxis_title="Quantidade", xaxis_title="Quartos")
        st.plotly_chart(grafico_quarto)

    # -=-=-=-=-=-=-=-=
    # Banheiros em casa
    # -==-=-=-=-=-=-=-
    with st.expander("Banheiros em casa"):
        st.subheader("Banheiros em casa")
        mapa_banheiros = {
            "A": "Nenhum",
            "B": "Um",
            "C": "Dois",
            "D": "Três",
            "E": "Quatro ou mais"
        }

        # Contagem dos dados dos filtros de 2019
        banheiros_2019 = df_2019["Q010"].value_counts().reset_index()
        banheiros_2019.columns = ["Banheiros", "Quantidade"]
        banheiros_2019["Banheiros"] = banheiros_2019["Banheiros"].astype(str).map(mapa_banheiros)
        banheiros_2019["Ano"] = "2019"
        # Percentual 2019
        total_banheiros_2019 = banheiros_2019["Quantidade"].sum()
        banheiros_2019["Percentual"] = (banheiros_2019["Quantidade"] / total_banheiros_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        banheiros_2023 = df_2023["Q010"].value_counts().reset_index()
        banheiros_2023.columns = ["Banheiros", "Quantidade"]
        banheiros_2023["Banheiros"] = banheiros_2023["Banheiros"].astype(str).map(mapa_banheiros)
        banheiros_2023["Ano"] = "2023"
        # Percentual 2023
        total_banheiros_2023 = banheiros_2023["Quantidade"].sum()
        banheiros_2023["Percentual"] = (banheiros_2023["Quantidade"] / total_banheiros_2023 * 100).round(1)

        # Juntar os dois
        contagem_banheiros = pd.concat([banheiros_2019, banheiros_2023])

        # Texto com quantidade e percentual
        contagem_banheiros["Total"] = contagem_banheiros["Quantidade"].astype(str) + "(" + contagem_banheiros[
            "Percentual"].astype(
            str) + "%)"

        grafico_banheiros = px.bar(
            contagem_banheiros,
            x="Banheiros",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"  # barras lado a lado
        )

        grafico_banheiros.update_traces(textposition="outside")
        grafico_banheiros.update_layout(yaxis_title="Quantidade", xaxis_title="Banheiros")
        st.plotly_chart(grafico_banheiros)

    # -=-=-=-=-=-=-=-=-=-=-=-
    # Máquina de Lavar
    # -=-=-=-=-=-=-=-=-=-=-=-
    with st.expander("Máquina de Lavar"):
        st.subheader("Máquina de Lavar")
        mapa_maquina = {
            "A": "Não",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais"
        }
        # Contagem dos dados dos filtros de 2019
        maquina_2019 = df_2019["Q014"].value_counts().reset_index()
        maquina_2019.columns = ["Maquina de lavar", "Quantidade"]
        maquina_2019["Maquina de lavar"] = maquina_2019["Maquina de lavar"].astype(str).map(mapa_maquina)
        maquina_2019["Ano"] = "2019"
        # Percentual 2019
        total_maquina_2019 = maquina_2019["Quantidade"].sum()
        maquina_2019["Percentual"] = (maquina_2019["Quantidade"] / total_maquina_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        maquina_2023 = df_2023["Q010"].value_counts().reset_index()
        maquina_2023.columns = ["Maquina de lavar", "Quantidade"]
        maquina_2023["Maquina de lavar"] = maquina_2023["Maquina de lavar"].astype(str).map(mapa_maquina)
        maquina_2023["Ano"] = "2023"
        # Percentual 2023
        total_maquina_2023 = maquina_2023["Quantidade"].sum()
        maquina_2023["Percentual"] = (maquina_2023["Quantidade"] / total_maquina_2023 * 100).round(1)

        # Juntar os dois
        contagem_maquina = pd.concat([maquina_2019, maquina_2023])

        # Texto com quantidade e percentual
        contagem_maquina["Total"] = contagem_maquina["Quantidade"].astype(str) + "(" + contagem_maquina[
            "Percentual"].astype(
            str) + "%)"

        grafico_maquina = px.bar(
            contagem_maquina,
            x="Maquina de lavar",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"  # barras lado a lado
        )

        grafico_maquina.update_traces(textposition="outside")
        grafico_maquina.update_layout(yaxis_title="Quantidade", xaxis_title="Maquina de lavar")
        st.plotly_chart(grafico_maquina)

    # -=-=-=-=-=-=-=-=-=-=-=-
    # Microondas
    # -=-=-=-=-=-=-=-=-=-=-=-
    with st.expander("Microondas"):
        st.subheader("Microondas")
        mapa_microondas = {
            "A": "Não",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais"
        }
        # Contagem dos dados dos filtros de 2019
        microondas_2019 = df_2019["Q016"].value_counts().reset_index()
        microondas_2019.columns = ["Microondas", "Quantidade"]
        microondas_2019["Microondas"] = microondas_2019["Microondas"].astype(str).map(mapa_microondas)
        microondas_2019["Ano"] = "2019"
        # Percentual 2019
        total_microondas_2019 = microondas_2019["Quantidade"].sum()
        microondas_2019["Percentual"] = (microondas_2019["Quantidade"] / total_microondas_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        microondas_2023 = df_2023["Q016"].value_counts().reset_index()
        microondas_2023.columns = ["Microondas", "Quantidade"]
        microondas_2023["Microondas"] = microondas_2023["Microondas"].astype(str).map(mapa_microondas)
        microondas_2023["Ano"] = "2023"
        # Percentual 2023
        total_microondas_2023 = microondas_2023["Quantidade"].sum()
        microondas_2023["Percentual"] = (microondas_2023["Quantidade"] / total_microondas_2023 * 100).round(1)

        # Juntar os dois
        contagem_microondas = pd.concat([microondas_2019, microondas_2023])

        # Texto com quantidade e percentual
        contagem_microondas["Total"] = contagem_microondas["Quantidade"].astype(str) + "(" + contagem_microondas[
            "Percentual"].astype(
            str) + "%)"

        grafico_microondas = px.bar(
            contagem_microondas,
            x="Microondas",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"  # barras lado a lado
        )

        grafico_microondas.update_traces(textposition="outside")
        grafico_microondas.update_layout(yaxis_title="Quantidade", xaxis_title="Microondas")
        st.plotly_chart(grafico_microondas)

    # -=-=-=-=-=-=-=-=-=-=-=-=-
    # Automóveis e Motos
    # -=-=-=-=-=-=-=-=-=-=-=-=-
    with st.expander("Automóveis e Motos"):
        st.subheader("Posse de Automóveis e Motos")

        # Mapeamento de respostas
        mapa_veiculos = {
            "A": "Não",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais"
        }

        # -=-=-=-=-=-=-=-=-=-=-=
        # Carros
        # -=-=-=-=-=-=-=-=-=-=-=
        carro_2019 = df_2019["Q010"].value_counts().reset_index()
        carro_2019.columns = ["Resposta", "Quantidade"]
        carro_2019["Resposta"] = carro_2019["Resposta"].astype(str).map(mapa_veiculos)
        carro_2019["Ano"] = "2019"
        carro_2019["Tipo"] = "Carro"

        carro_2023 = df_2023["Q010"].value_counts().reset_index()
        carro_2023.columns = ["Resposta", "Quantidade"]
        carro_2023["Resposta"] = carro_2023["Resposta"].astype(str).map(mapa_veiculos)
        carro_2023["Ano"] = "2023"
        carro_2023["Tipo"] = "Carro"

        # -=-=-=-=-=-=-=-=-=-=-=
        # Motos
        # -=-=-=-=-=-=-=-=-=-=-=
        moto_2019 = df_2019["Q012"].value_counts().reset_index()
        moto_2019.columns = ["Resposta", "Quantidade"]
        moto_2019["Resposta"] = moto_2019["Resposta"].astype(str).map(mapa_veiculos)
        moto_2019["Ano"] = "2019"
        moto_2019["Tipo"] = "Moto"

        moto_2023 = df_2023["Q012"].value_counts().reset_index()
        moto_2023.columns = ["Resposta", "Quantidade"]
        moto_2023["Resposta"] = moto_2023["Resposta"].astype(str).map(mapa_veiculos)
        moto_2023["Ano"] = "2023"
        moto_2023["Tipo"] = "Moto"

        contagem_veiculos = pd.concat([carro_2019, carro_2023, moto_2019, moto_2023])

        grafico_veiculos = px.bar(
            contagem_veiculos,
            x="Resposta",
            y="Quantidade",
            color="Ano",
            facet_col="Tipo",  # separa em dois painéis: Carro e Moto
            barmode="group",
            text="Quantidade"
        )

        grafico_veiculos.update_traces(textposition="outside")
        grafico_veiculos.update_layout(
            yaxis_title="Quantidade",
            xaxis_title="Respostas",
            showlegend=True
        )

        st.plotly_chart(grafico_veiculos)

with tabs[3]:
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Desempenho Geral
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    with st.expander("Desempenho Geral"):
        st.subheader("Desempenho Geral")

        # Cálculo das médias por área
        medias = {
            "Ciências da Natureza": df_filtrado["NU_NOTA_CN"].mean(),
            "Ciências Humanas": df_filtrado["NU_NOTA_CH"].mean(),
            "Linguagens e Códigos": df_filtrado["NU_NOTA_LC"].mean(),
            "Matemática": df_filtrado["NU_NOTA_MT"].mean(),
            "Redação": df_filtrado["NU_NOTA_REDACAO"].mean()
        }

        # --- Gráfico de barras das médias ---
        grafico_medias = px.bar(
            x=list(medias.keys()),
            y=list(medias.values()),
            title="Média das Notas por Área",
            labels={"x": "Área", "y": "Nota Média"},
            text=[f"{v:.1f}" for v in medias.values()]
        )
        grafico_medias.update_traces(textposition='outside')
        st.plotly_chart(grafico_medias, use_container_width=True)

        # --- Boxplot das notas ---
        gráfico_notas = df_filtrado[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "TP_STATUS_REDACAO"]].rename(columns={
            "NU_NOTA_CN": "Ciências da Natureza",
            "NU_NOTA_CH": "Ciências Humanas",
            "NU_NOTA_LC": "Linguagens e Códigos",
            "NU_NOTA_MT": "Matemática",
            "TP_STATUS_REDACAO": "Redação"
        })

        gráfico_notas = px.box(
            gráfico_notas,
            points="outliers",
            title="Distribuição das Notas por Área (Boxplot)",
            labels={"value": "Nota", "variable": "Área"}
        )
        st.plotly_chart(gráfico_notas, use_container_width=True)


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Língua Estrangeira
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    with st.expander("Língua Estrangeira"):
        st.subheader("Língua Estrangeira")
        mapa_lingua = {
            0: "Inglês",
            1: "Espanhol"
        }

        # Contagem dos dados dos filtros de 2019
        lingua_2019 = df_2019["TP_LINGUA"].value_counts().reset_index()
        lingua_2019.columns = ["Lingua", "Quantidade"]
        lingua_2019["Lingua"] = lingua_2019["Lingua"].astype(int).map(mapa_lingua)
        lingua_2019["Ano"] = "2019"
        # Percentual 2019
        total_lingua_2019 = lingua_2019["Quantidade"].sum()
        lingua_2019["Percentual"] = (lingua_2019["Quantidade"] / total_lingua_2019 * 100).round(1)

        # Contagem dos dados dos filtros de 2023
        lingua_2023 = df_2023["TP_LINGUA"].value_counts().reset_index()
        lingua_2023.columns = ["Lingua", "Quantidade"]
        lingua_2023["Lingua"] = lingua_2023["Lingua"].astype(int).map(mapa_lingua)
        lingua_2023["Ano"] = "2023"
        # Percentual 2023
        total_lingua_2023 = lingua_2023["Quantidade"].sum()
        lingua_2023["Percentual"] = (lingua_2023["Quantidade"] / total_lingua_2023 * 100).round(1)

        # Juntar os dois anos
        contagem_lingua = pd.concat([lingua_2019, lingua_2023])

        # Criar texto com quantidade e percentual
        contagem_lingua["Total"] = contagem_lingua["Quantidade"].astype(str) + " (" + contagem_lingua["Percentual"].astype(str) + "%)"

        # Gráfico comparativo
        grafico_lingua = px.bar(
            contagem_lingua,
            x="Lingua",
            y="Quantidade",
            color="Ano",
            text="Total",
            barmode="group"
        )

        grafico_lingua.update_traces(textposition="outside")
        grafico_lingua.update_layout(yaxis_title="Quantidade",xaxis_title="Língua Estrangeira")
        st.plotly_chart(grafico_lingua)

    with st.expander("Desempenho por aspectos pessoais"):
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Mapas
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        mapa_areas = {
            "NU_NOTA_MT": "Matemática",
            "NU_NOTA_CN": "Ciências da Natureza",
            "NU_NOTA_CH": "Ciências Humanas",
            "NU_NOTA_LC": "Linguagens e Códigos",
            "NU_NOTA_REDACAO": "Redação"
        }
        notas = list(mapa_areas.keys())

        mapa_sexo = {
            "M": "Masculino",
            "F": "Feminino"
        }

        mapa_estado_civil = {
            1: "Solteiro(a)",
            2: "Casado(a)",
            3: "Divorciado(a)",
            4: "Viúvo(a)",
            5: "Outros"
        }

        mapa_faixa_etaria = {
            1: "Menor de 17 anos",
            2: "17 anos",
            3: "18 anos",
            4: "19 anos",
            5: "20 anos",
            6: "21 anos",
            7: "22 anos",
            8: "23 anos",
            9: "24 anos",
            10: "25 anos",
            11: "Entre 26 e 30 anos",
            12: "Entre 31 e 35 anos",
            13: "Entre 36 e 40 anos",
            14: "Entre 41 e 45 anos",
            15: "Entre 46 e 50 anos",
            16: "Entre 51 e 55 anos",
            17: "Entre 56 e 60 anos",
            18: "Entre 61 e 65 anos",
            19: "Entre 66 e 70 anos",
            20: "Maior de 70 anos"
        }

        mapa_renda = {
            "A": "Classe E (até 2 Salários Minímos)",
            "B": "Classe E (até 2 Salários Minímos)",
            "C": "Classe D (2 a 4 Salários Minímos)",
            "D": "Classe D (2 a 4 Salários Minímos)",
            "E": "Classe C (4 a 10 Salários Minímos)",
            "F": "Classe C (4 a 10 Salários Minímos)",
            "G": "Classe B (10 a 20 Salários Minímos)",
            "H": "Classe B (10 a 20 Salários Minímos)",
            "I": "Classe A (+ de 20 Salários Minímos)",
            "J": "Classe A (+ de 20 Salários Minímos)",
        }

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Seleção de Ano
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        st.title("Desempenho por aspectos sociais")
        ano = st.selectbox("Selecione o ano:", ["2019", "2023"])
        df = df_2019 if ano == "2019" else df_2023

        abas = st.tabs(["Por Sexo", "Por Estado Civil", "Por Idade", "Por Renda"])

        # --=-=-=-=-=-=-=-=-=-=
        # Por SEXO
        # --=-=-=-=-=-=-=-=-=-=
        with abas[0]:
            st.subheader("Por Sexo")
            df["Sexo"] = df["TP_SEXO"].map(mapa_sexo)

            medias = df.groupby("Sexo")[notas].mean().reset_index()
            dados_sexo = medias.melt(id_vars="Sexo", var_name="Área", value_name="Média")
            dados_sexo["Área"] = dados_sexo["Área"].map(mapa_areas)

            grafico_sexo = px.bar(
                dados_sexo,
                x="Área",
                y="Média",
                color="Sexo",
                barmode="group",
                text_auto=".1f"
            )
            st.plotly_chart(grafico_sexo, use_container_width=True)

            dados_sexo_box = df.melt(id_vars="Sexo", value_vars=notas, var_name="Área", value_name="Nota")
            dados_sexo_box["Área"] = dados_sexo_box["Área"].map(mapa_areas)
            sexo_box = px.box(
                dados_sexo_box,
                x="Área",
                y="Nota",
                color="Sexo"
            )
            st.plotly_chart(sexo_box, use_container_width=True)

        # -=-=-=-=-=-=-=-=-
        # Por ESTADO CIVIL
        # -=-=-=-=-=-=-=-=-
        with abas[1]:
                st.subheader("Por Estado Civil")
                df["Estado Civil"] = df["TP_ESTADO_CIVIL"].map(mapa_estado_civil)

                medias = df.groupby("Estado Civil")[notas].mean().reset_index()
                dados = medias.melt(id_vars="Estado Civil", var_name="Área", value_name="Média")
                dados["Área"] = dados["Área"].map(mapa_areas)

                estado_civil_grafico = px.bar(
                    dados,
                    x="Área",
                    y="Média",
                    color="Estado Civil",
                    barmode="group",
                    text_auto=".1f"
                )
                st.plotly_chart(estado_civil_grafico, use_container_width=True)

                dados_estado_civil_box = df.melt(id_vars="Estado Civil", value_vars=notas, var_name="Área",
                                                 value_name="Nota")
                dados_estado_civil_box["Área"] = dados_estado_civil_box["Área"].map(mapa_areas)
                estado_civil_box = px.box(
                    dados_estado_civil_box,
                    x="Área",
                    y="Nota",
                    color="Estado Civil"
                )
                st.plotly_chart(estado_civil_box, use_container_width=True)

        # -=-=-=-=-=-=-=-=-
        # Por IDADE
        # -=-=-=-=-=-=-=-=-
        with abas[2]:
            st.subheader("Por Idade")
            df["Faixa Etária"] = df["TP_FAIXA_ETARIA"].map(mapa_faixa_etaria)

            medias = df.groupby("Faixa Etária")[notas].mean().reset_index()
            dados = medias.melt(id_vars="Faixa Etária", var_name="Área", value_name="Média")
            dados["Área"] = dados["Área"].map(mapa_areas)

            grafico_idade = px.bar(
                dados,
                x="Área",
                y="Média",
                color="Faixa Etária",
                barmode="group",
                text_auto=".1f"
            )
            st.plotly_chart(grafico_idade, use_container_width=True)

            dados_idade_box = df.melt(id_vars="Faixa Etária", value_vars=notas, var_name="Área", value_name="Nota")
            dados_idade_box["Área"] = dados_idade_box["Área"].map(mapa_areas)
            idade_box = px.box(
                dados_idade_box,
                x="Área",
                y="Nota",
                color="Faixa Etária"
            )
            st.plotly_chart(idade_box, use_container_width=True)

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Desempenho por RENDA
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        with abas[3]:
            st.subheader("Por Renda")
            df["Renda"] = df["Q006"].map(mapa_renda)
            df = df.dropna(subset=["Renda"])

            medias = df.groupby("Renda")[notas].mean().reset_index()
            medias[notas] = (medias[notas] / 10).round(1)

            dados = medias.melt(id_vars="Renda", var_name="Área", value_name="Média (%)")
            dados["Área"] = dados["Área"].map(mapa_areas)

            fig_bar = px.bar(dados, x="Área", y="Média (%)", color="Renda", barmode="group", text_auto=".1f")
            st.plotly_chart(fig_bar, use_container_width=True)

            dados_box = df.melt(id_vars="Renda", value_vars=notas, var_name="Área", value_name="Nota")
            dados_box["Área"] = dados_box["Área"].map(mapa_areas)
            fig_box = px.box(
                dados_box,
                x="Área",
                y="Nota",
                color="Renda"
            )
            st.plotly_chart(fig_box, use_container_width=True)

    with st.expander("Desempenho por escola"):
        st.subheader("Distribuição e desempenho por tipo de escola")

        # Mapeamento dos tipos de administração
        mapa_adm = {
            1: "Federal",
            2: "Estadual",
            3: "Municipal",
            4: "Privada",
            5: "Sem informação"
        }

        # Adiciona as colunas mapeadas
        df["Classe Social"] = df["Q006"].map(mapa_renda)
        df["Tipo de Escola"] = df["TP_ESCOLA"].map(mapa_adm)

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Gráficos de Pizza por Classe Social
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        for classe in df["Classe Social"].unique():
            dados_classe = df[df["Classe Social"] == classe]
            contagem = dados_classe["Tipo de Escola"].value_counts(normalize=True) * 100
            dados_pizza = contagem.reset_index()
            dados_pizza.columns = ["Tipo de Escola", "Percentual"]

            grafico_pizza = px.pie(
                dados_pizza,
                names="Tipo de Escola",
                values="Percentual",
                title=f"{classe}",
                hole=0.3
            )
            st.plotly_chart(grafico_pizza, use_container_width=True)

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Gráfico de Média das Notas
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-
        st.write("Média das notas por classe social e tipo de escola")

        medias = df.groupby(["Classe Social", "Tipo de Escola"])[notas].mean().reset_index()
        medias[notas] = (medias[notas] / 10).round(1)

        dados_barra = medias.melt(id_vars=["Classe Social", "Tipo de Escola"], var_name="Área",
                                  value_name="Média (%)")
        dados_barra["Área"] = dados_barra["Área"].map(mapa_areas)

        grafico_barras = px.bar(
            dados_barra,
            x="Classe Social",
            y="Média (%)",
            color="Tipo de Escola",
            barmode="group",
            facet_col="Área"
        )

        # Remove o prefixo "Área=" dos títulos das facetas
        grafico_barras.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        st.plotly_chart(grafico_barras, use_container_width=True)
