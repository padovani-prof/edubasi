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
# Checkbox na barra lateral
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
incluir_sem_escola = st.sidebar.checkbox(
    "Incluir alunos sem escola",
    value=True,
    help="Se desmarcado, alunos sem informação de escola não serão considerados."
)

if not incluir_sem_escola and "CO_MUNICIPIO_ESC" in df_filtrado.columns:
    # Remove os alunos sem escola
    df_filtrado = df_filtrado[df_filtrado["CO_MUNICIPIO_ESC"].notna()]

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Título e cabeçalho
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
st.title("Análise Social")
st.header("Microdados do Exame Nacional do Ensino Médio")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Criação das abas Dados Gerais,
# pessoais, escolares de renda,
# moradia, transporte e aparelhos e tecnologias em casa
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
tabs = st.tabs([
    "Dados Gerais",
    "Dados Pessoais",
    "Depêndencia Administrativa",
    "Dados de Renda",
    "Dados de Moradia",
    "Aparelhos e Tecnologias Digitais",
    "Dados de Transporte",
])

#-=-=-=-=-=-=-=-=-=-=
# Dados gerais
# --=-=-=-=-=-=-=-=-=
with tabs[0]:
    df_inscritos = df_filtrado[df_filtrado["ANO"].isin([2019, 2023])] # todos os inscritos, sem filtro
    if not df_inscritos.empty:
        contagem = (
            # AGRUPA DADOS PELAS COLUNAS / Conta o número de linhas em cada grupo / Transforma o resultado em um novo DF com duas colunas de ano e quantidade
            df_inscritos.groupby("ANO").size().reset_index(name="Quantidade")
        )
        grafico_dados_gerais = px.bar(
            contagem,
            x="ANO",
            y="Quantidade",
            text="Quantidade",
            title="Quantidade de inscritos no ENEM por ano",
            color="ANO", # para que cada cor vá para uma faixa de renda diferente
        )
        # Remove a barra de cores da lateral que mostra anos que não estamos utilizando
        grafico_dados_gerais.update_layout(coloraxis_showscale=False)
        # força eixo X a ser categórico mostra apenas os valores que tem (2019 e 2023), sem intervalos no meio.
        grafico_dados_gerais.update_xaxes(type="category")
        # deixa as barras mais finas
        grafico_dados_gerais.update_traces(width=0.4)  # padrão é 0.8

        st.plotly_chart(grafico_dados_gerais)
    else:
        st.warning("Não há dados para os anos selecionados.")

#-=-=-=-=-=-=-=-=-=
# Dados pessoais
# -=-=-=-=-=-=-=-=
with tabs[1]:
    st.subheader("Participantes por Sexo")

    # Pegando os anos únicos e os dois primeiros
    anos = df_filtrado["ANO"].dropna().unique()[:2]

    # Substituindo M e F por Masculino e Feminino
    df_filtrado["TP_SEXO"] = df_filtrado["TP_SEXO"].replace({"M": "Masculino", "F": "Feminino"})

    # Para mostrar mensagem de informação para caso o gráfico não existir em 2019
    #Verifica se anos está vazio antes de usar anos[0] ou anos[1].
    # Adiciona checagem para dados_ano1 e dados_ano2 para garantir que não estejam vazios.
    # Mostra uma mensagem se não houver dados.
    if len(anos) == 0:
        st.warning("Não há dados disponíveis para os anos selecionados.")
    else:
        # Criando duas colunas para os gráficos
        col1, col2 = st.columns(2)

        # Gráfico do primeiro ano
        dados_ano1 = df_filtrado[df_filtrado["ANO"] == anos[0]]
        if not dados_ano1.empty:
            graf_pizza1 = px.pie(
                dados_ano1,
                names="TP_SEXO",
                hole=0.3,
                title=f"{anos[0]}"
            )
            col1.plotly_chart(graf_pizza1)
        else:
            col1.info(f"Sem dados para o ano {anos[0]}")

        # Para mostrar mensagem de informação para caso o gráfico não existir em 2019
        # Verifica se anos está vazio antes de usar anos[0] ou anos[1].
        # Adiciona checagem para dados_ano1 e dados_ano2 para garantir que não estejam vazios.
        # Mostra uma mensagem se não houver dados.
        if len(anos) > 1:
            dados_ano2 = df_filtrado[df_filtrado["ANO"] == anos[1]]
            if not dados_ano2.empty:
                graf_pizza2 = px.pie(
                    dados_ano2,
                    names="TP_SEXO",
                    hole=0.3,
                    title=f"{anos[1]}"
                )
                col2.plotly_chart(graf_pizza2)
            else:
                col2.info(f"Sem dados para o ano {anos[1]}")
        else:
            col2.info("Não há segundo ano disponível para comparar")

    # -=-=-=-=-=-=-=-=-=-=-=-==-=
    # GRÁFICO FAIXA ETÁRIA
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-

    #pegando a coluna de faixa etária dos participantes
    st.subheader("Faixa Etária dos participantes")
    # Mapa de faixas de idade
    mapa_idade = [
        "Menor de 17 anos", "17 a 25 anos", "26 a 30 anos", "31 a 35 anos",
        "36 a 40 anos", "41 a 45 anos", "46 a 50 anos", "51 a 55 anos",
        "56 a 60 anos", "61 a 65 anos", "66 a 70 anos", "Mais de 70 anos"
    ]

    # Substituindo valores numéricos por labels
    df_filtrado["TP_FAIXA_ETARIA"] = df_filtrado["TP_FAIXA_ETARIA"].replace(dict(enumerate(mapa_idade, start=0)))

    # Filtro pelo sidebar
    idade_selecionada = st.sidebar.multiselect("Selecione a faixa etária:", options=mapa_idade, default=mapa_idade)

    # Filtrando pelos anos e faixas selecionadas
    filtrado = df_filtrado[
        (df_filtrado["TP_FAIXA_ETARIA"].isin(idade_selecionada))
        ]

    contagem = filtrado.groupby(["ANO", "TP_FAIXA_ETARIA"]).size().reset_index(name="Quantidade")

    # Renomeia a coluna
    contagem = contagem.rename(columns={"TP_FAIXA_ETARIA": "Faixa Etária"})

    # Garantir ordem cronológica das faixas
    contagem["Faixa Etária"] = pd.Categorical(contagem["Faixa Etária"], categories=mapa_idade, ordered=True)
    contagem = contagem.sort_values(["ANO", "Faixa Etária"])

    # Gráfico comparando 2019 e 2023
    grafico_fx_etaria = px.bar(
        contagem,
        x="Faixa Etária",
        y="Quantidade",
        color="ANO",  # cada ano uma cor
        text="Quantidade"
    )

    # Remove a barra de cores da lateral
    grafico_fx_etaria.update_layout(coloraxis_showscale=False)
    st.plotly_chart(grafico_fx_etaria)

    #-=-=-=-=-=-=-=-=-=-=-=-
    # Gráfico Estado civil
    # -=-=-=-=-=-=-=-=-=-=-=-
    st.subheader("Estado Civil")
    dados_est_civil = df_filtrado["TP_ESTADO_CIVIL"].dropna().unique()

    mapa_est_civil = {
        0: "Não informado",
        1: "Solteiro(a)",
        2: "Casado(a)",
        3: "Divorciado(a)",
        4: "Viúvo(a)"
    }

    # aplica o mapeamento para a coluna, criando uma cópia
    df_filtrado_copy = df_filtrado.copy()
    df_filtrado_copy["Estado Civil"] = df_filtrado_copy["TP_ESTADO_CIVIL"].map(mapa_est_civil)

    # opções únicas para o multiselect (agora já com nomes)
    dados = df_filtrado_copy["Estado Civil"].dropna().unique()

    # Visualiza se existem os dados de Estado Civil e retorna uma mensagem caso não exista esses dados
    if len(dados) == 0:
        st.warning("Não há dados disponíveis para Estado Civil.")
    else:
        escola_selecionada = st.sidebar.multiselect(
            "Estado Civil:",
            options=dados,
            default=dados
        )

        # filtra os dados
        filtrado_estado_civil = df_filtrado_copy[df_filtrado_copy["Estado Civil"].isin(escola_selecionada)].copy()

        # conta os tipos de escola
        contagem = filtrado_estado_civil["Estado Civil"].value_counts().reset_index()
        contagem.columns = ["Estado Civil", "Quantidade"]

        # gráfico de barras
        grafico = px.bar(
            contagem,
            x="Estado Civil",
            y="Quantidade",
            text="Quantidade",
        )
        st.plotly_chart(grafico)

        # -=-=-=-=-=-=-=-=-=-=-=-=-=
        # Cor/ Raça dos estudantes
        # -=-=-=-=-=-=-=-=-=-=-=-=-=

        st.subheader("Distribuição por Cor/Raça")
        #Criação de uma paleta de cores para adicionar ao gráfico
        paleta_cor_raca = ["#08519c", "#08519c", "#2171b5", "#4292c6", "#6baed6", "#9ecae1", "#c6dbef", "#deebf7"]

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

        # Aplicar o mapeamento no DataFrame filtrado
        df_filtrado["TP_COR_RACA"] = df_filtrado["TP_COR_RACA"].map(mapa_cor_raca)

        # Contagem das categorias de cor/raça
        contagem_cor_raca = df_filtrado["TP_COR_RACA"].value_counts().reset_index()
        contagem_cor_raca.columns = ["Cor/Raça", "Quantidade"]

        # Gráfico de barras
        grafico_cor_raca = px.bar(
            contagem_cor_raca,
            x="Cor/Raça",
            y="Quantidade",
            text="Quantidade",
            color="Cor/Raça",
            color_discrete_sequence=paleta_cor_raca
        )

        st.plotly_chart(grafico_cor_raca)



#-=-=-=-=-=-=-=-=-=-=-=-==-=
# TIPO DE ESCOLA
#-=-=-=-=-=-=-=-=-=-=-=-=-=-
with tabs[2]:
    st.subheader("Quantidade de inscritos por Tipo de Escola")
    #cria um mapeamento para os dados dos códigos por nomes e não números
    mapa_escola = {
        1: "Federal",
        2: "Estadual",
        3: "Municipal",
        4: "Privada"
    }
    # aplica o mapeamento para a coluna, criando uma cópia
    df_filtrado_copy = df_filtrado.copy()
    df_filtrado_copy["Tipo de Escola"] = df_filtrado_copy["TP_DEPENDENCIA_ADM_ESC"].map(mapa_escola)

    # opções únicas para o multiselect (agora já com nomes)
    dados = df_filtrado_copy["Tipo de Escola"].dropna().unique()

    if len(dados) == 0:
        st.warning("Não há dados disponíveis para Tipo de Escola.")
    else:
        escola_selecionada = st.sidebar.multiselect(
            "Tipo de Escola:",
            options=dados,
            default=dados
        )

        # filtra os dados
        filtrado_escola = df_filtrado_copy[df_filtrado_copy["Tipo de Escola"].isin(escola_selecionada)].copy()

        # conta os tipos de escola
        contagem = filtrado_escola["Tipo de Escola"].value_counts().reset_index()
        contagem.columns = ["Dependência administrativa", "Quantidade"]

        # gráfico de barras
        grafico = px.bar(
            contagem,
            x="Dependência administrativa",
            y="Quantidade",
            text="Quantidade",
        )
        st.plotly_chart(grafico)

        # =-=-=-=-=-=-=-=-=-=-=-=-=
        # Gráfico com o Tipo de ensino
        # =-=-=-=-=-=-=-=-=-=-=-=-=
        st.subheader("Tipo de Escola")
        mapa_ensino = {
            1: "Ensino Regular",
            2: "Educação Especial - Modalidade Substitutiva"
        }

        df_filtrado["TP_ENSINO"] = df_filtrado["TP_ENSINO"].map(mapa_ensino)
        # Contagem por tipo de ensino
        contagem_ensino = df_filtrado["TP_ENSINO"].value_counts().reset_index()
        contagem_ensino.columns = ["Tipo de Ensino", "Quantidade"]

        cores_tp_ensino = ["#08306b", "#6baed6"]

        # Gráfico de barras
        import plotly.express as px

        fig = px.bar(
            contagem_ensino,
            x="Tipo de Ensino",
            y="Quantidade",
            text="Quantidade",
            color_discrete_sequence=cores_tp_ensino
        )

        st.plotly_chart(fig)

        # =-=-=-=-=-=-=-=-=-=-=-=-=
        # Gráfico com a Localização da Escola
        # =-=-=-=-=-=-=-=-=-=-=-=-=

        st.subheader("Tipo de Ensino")
        # 1 = Urbana, 2 = Rural
        mapa_localizacao = {
            1: "Urbana",
            2: "Rural"
        }

        # Aplicar o mapeamento de TP_localização
        df_filtrado["TP_LOCALIZACAO_ESC"] = df_filtrado["TP_LOCALIZACAO_ESC"].map(mapa_localizacao)

        # Contagem por localização
        contagem_localizacao = df_filtrado["TP_LOCALIZACAO_ESC"].value_counts().reset_index()
        contagem_localizacao.columns = ["Localização", "Quantidade"]

        # Paleta de cores azul (mais escuro para urbano, mais claro para rural)
        cores_localizacao = ["#6baed6", "#08306b"]

        # Gráfico de barras
        grafico_localizacao = px.bar(
            contagem_localizacao,
            x="Localização",
            y="Quantidade",
            text="Quantidade",
            color="Localização",
            color_discrete_sequence=cores_localizacao
        )

        st.plotly_chart(grafico_localizacao)


#=-=-=-=-=-=-=-=-=-=-=-=-=
# Aba com os dados de Renda
#=-=-=-=-=-=-=-=-=-=-=-=-=
with tabs[3]:
    # criando uma paleta de cores para renda
    paleta_renda = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2",
        "#7f7f7f", "#bcbd22", "#17becf", "#393b79", "#637939", "#8c6d31", "#843c39",
        "#7b4173", "#5254a3", "#9c9ede"
    ]
    # Mapeamento dos valores de Q006 para mudar as letras para o nome de A a Q
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
        "J": "De R$ 7.920,01 até R$ 9240,00",
        "K": "De R$ 9.240,01 até R$ 10.560,00",
        "L": "De R$ 10.560,01 até R$ 11.880,00",
        "M": "De R$ 11.880,01 até R$ 13.200,00",
        "N": "De R$ 13.200,01 até R$ 15.840,00",
        "O": "De R$ 15.840,01 até R$19.800,00",
        "P": "De R$ 19.800,01 até R$ 26.400,00",
        "Q": "Acima de R$ 26.400,00"

    }
    # Substitui diretamente na coluna renomeando as letras pelas faixas de renda pelo meio do mapa_renda
    df_filtrado["Q006"] = df_filtrado["Q006"].replace(mapa_renda)
    # Para o multiselect, pega valores únicos já traduzidos
    dados_renda = df_filtrado["Q006"].dropna().unique()
    renda_selecionado = st.sidebar.multiselect(
        "Renda",
        options=dados_renda,
        default=dados_renda
    )
    # Contagem dos dados filtrados
    renda = df_filtrado["Q006"].value_counts().reset_index()
    renda.columns = ["Dados de Renda", "Quantidade"]
    # Gráfico de renda
    grafico_renda = px.bar(
        renda,
        x="Dados de Renda",
        y="Quantidade",
        text="Quantidade",
        color="Dados de Renda", # para que cada cor vá para uma faixa de renda diferente
        color_discrete_map={r: c for r, c in zip(renda["Dados de Renda"], paleta_renda)}
    )
    st.plotly_chart(grafico_renda)

#-=-=-=-=-=-=-=-=-=-=-=-=-=
# Aba 4 - Dados de moradia
#-=-=-=-=-=-=-=-=-=-=-=-=-=

with tabs[4]:
    st.subheader("Dados de Moradia")
    # Mapeamento de pessoas que moram na mesma casa
    moradia_map = {
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
    moradia_2019["Moradores"] = moradia_2019["Moradores"].astype(int).map(moradia_map)
    moradia_2019["Ano"] = "2019"

    # Contagem dos dados dos filtros de  2023
    moradia_2023 = df_2023["Q005"].value_counts().reset_index()
    moradia_2023.columns = ["Moradores", "Quantidade"]
    moradia_2023["Moradores"] = moradia_2023["Moradores"].astype(int).map(moradia_map)
    moradia_2023["Ano"] = "2023"

    # Juntar os dois
    moradia_comparada = pd.concat([moradia_2019, moradia_2023])

    # Gráfico comparativo
    grafico = px.bar(
        moradia_comparada,
        x="Moradores",
        y="Quantidade",
        color="Ano",
        barmode="group",  # barras lado a lado (pode trocar por "overlay" ou "relative")
        title="Quantidade de Pessoas por Residência",
        text="Quantidade"
    )

    st.plotly_chart(grafico)


    #-==-=-==-=-=-=-=-=-=-=
    # Dados de Moradia / Quartos em casa
    #-==-=-==-=-=-=-=-=-=-=
    st.subheader("Quartos em casa")
    mapa_quartos = {
        "A": "Não",
        "B": "Um",
        "C": "Dois",
        "D": "Três",
        "E": "Quatro ou mais"
    }

    # Substitui letras pelos significados
    dados_quarto = df_filtrado["Q009"] = df_filtrado["Q009"].map(mapa_quartos)

    # Contagem das respostas
    dados_quartos = df_filtrado["Q009"].value_counts().reset_index()
    dados_quartos.columns = ["Quartos", "Quantidade"]

    # Gráfico de barras
    graf_quartos = px.bar(
        dados_quartos,
        x="Quartos",
        y="Quantidade",
        text="Quantidade",
        color="Quartos",
        title="Quantidade de Quartos por Residência",
    )
    chart = st.plotly_chart(graf_quartos)

    #-=-=-=-=-=-=-=-=
    #Banheiros em casa
    #-==-=-=-=-=-=-=-
    st.subheader("Banheiros em casa")
    mapa_banheiros = {
        "A": "Nenhum",
        "B": "Um",
        "C": "Dois",
        "D": "Três",
        "E": "Quatro ou mais"
    }

    df_filtrado["Q010"] = df_filtrado["Q010"].map(mapa_banheiros)

    dados_banheiros = df_filtrado["Q010"].value_counts().reset_index()
    dados_banheiros.columns = ["Banheiros", "Quantidade"]

    graf_banheiro = px.bar(
        dados_banheiros,
        x="Banheiros",
        y="Quantidade",
        text="Quantidade",
        color="Banheiros",
        title="Quantidade de Banheiros por Residência"
    )
    st.plotly_chart(graf_banheiro)


#-=-=-=-=-=-=--=-=-=-=-=
# Aba de Aparelhos digitais e etc
#-=-=-=-=-=-=--=-=-=-=-=
with tabs[5]:
    #-=-=-=-=-=-=
    #Gráfico celular em casa
    #=-=-=-=-=-=-
    st.subheader("Celulares em casa")
    mapa_celulares = {
        "A": "Nenhum",
        "B": "Um",
        "C": "Dois",
        "D": "Três",
        "E": "Quatro ou mais"
    }

    df_filtrado["Q011"] = df_filtrado["Q011"].map(mapa_celulares)

    dados_celulares = df_filtrado["Q011"].value_counts().reset_index()
    dados_celulares.columns = ["Celulares", "Quantidade"]

    graf_celular = px.bar(
        dados_celulares,
        x="Celulares",
        y="Quantidade",
        text="Quantidade",
        color="Celulares",
        title="Quantidade de Celulares por Residência"
    )
    st.plotly_chart(graf_celular)

    #-=-=-=-=-=-=
    #Gráfico computador em casa
    #=-=-=-=-=-=-

    st.subheader("Computadores em casa")
    mapa_computadores = {
        "A": "Nenhum",
        "B": "Um",
        "C": "Dois",
        "D": "Três",
        "E": "Quatro ou mais"
    }

    df_filtrado["Q024"] = df_filtrado["Q024"].map(mapa_computadores)

    dados_computadores = df_filtrado["Q024"].value_counts().reset_index()
    dados_computadores.columns = ["Computadores", "Quantidade"]

    graf_computador = px.bar(
        dados_computadores,
        x="Computadores",
        y="Quantidade",
        text="Quantidade",
        color="Computadores",
        title="Quantidade de Computadores por Residência"
    )
    st.plotly_chart(graf_computador)

    #-=-=-=-=-=-=-=-=
    # Internet em casa
    #-=-==-=-=-=-=-=

    st.subheader("Internet em casa")
    mapa_internet = {
        "A": "Não",
        "B": "Sim"
    }

    df_filtrado["Q025"] = df_filtrado["Q025"].map(mapa_internet)

    dados_internet = df_filtrado["Q025"].value_counts().reset_index()
    dados_internet.columns = ["Internet", "Quantidade"]

    graf_internet = px.bar(
        dados_internet,
        x="Internet",
        y="Quantidade",
        text="Quantidade",
        color="Internet",
        title="Acesso à Internet nas Residências"
    )
    st.plotly_chart(graf_internet)
