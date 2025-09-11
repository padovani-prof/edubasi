import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from numpy.random import default_rng as rng


def titulo():
    st.title("Análise dos dados do ENEM - Desempenho")


def inscritos():
    exp = st.expander("Inscrições no exame")
    total_inscritos(exp)
    inscritos_por_ano(exp)


def total_inscritos(exp):
    with exp:
        st.metric(label="Inscritos", value="1.633")


def inscritos_por_ano(exp):
    with exp:
        col, _ = st.columns(2)
        df = pd.DataFrame(
            {"valor": [949, 684]},
            index=[2019, 2023]
        )
        with col:
            st.write("Inscritos por ano")
            st.bar_chart(df)

def filtros():
    st.sidebar.title("Filtros")

    st.sidebar.selectbox(
        "Anos",
        ["2019", "2023", "2019 e 2023"]
    )

    st.sidebar.checkbox(
        "Incluir inscrições sem definição de escola",
        value=True
    )


def presenca():
    with st.expander("Presença nas provas"):
        col1, col2 = st.columns(2)

        with col1:
            df = pd.DataFrame({
                "Situação": ["Presentes", "Ausentes"],
                "Percentual": [68.2, 31.8]
            })

            chart = (
                alt.Chart(df)
                .mark_arc(innerRadius=50)
                .encode(
                    theta="Percentual:Q",
                    color="Situação:N",
                    tooltip=["Situação", "Percentual"]
                )
            )
            st.altair_chart(chart, use_container_width=True)

        with col2:
            df = pd.DataFrame({
                "Ano": [2019, 2023],
                "Presentes": [747, 367],
                "Ausentes": [202, 317]
            })

            df_melt = df.melt("Ano", var_name="Situação", value_name="Quantidade")

            chart = (
                alt.Chart(df_melt)
                .mark_bar()
                .encode(
                    x=alt.X("Ano:N", axis=alt.Axis(labelAngle=0)),
                    y="Quantidade:Q",
                    color="Situação:N"
                )
            )
            st.altair_chart(chart, use_container_width=True)


def medias_por_area():
    with st.expander("Notas médias por área de conhecimento"):
        df = pd.DataFrame({
            "area": [
                "Ciências da Natureza", "Ciências da Natureza",
                "Ciências Humanas", "Ciências Humanas",
                "Ling. e Códigos", "Ling. e Códigos",
                "Matematica", "Matematica",
                "Redação", "Redação"
            ],
            "ano": [
                "2019", "2023", "2019", "2023",
                "2019", "2023", "2019", "2023",
                "2019", "2023"
            ],
            "media": [433, 460, 459, 480, 477, 485, 469, 471, 490, 519]
        })

        ordem_areas = df["area"].unique().tolist()

        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X(
                    "area:N",
                    sort=ordem_areas,
                    axis=alt.Axis(labelAngle=0, title="Área de Conhecimento")
                ),
                y=alt.Y("media:Q", title="Média das Notas"),
                color=alt.Color("ano:N", title="Ano")
            )
        )

        st.altair_chart(chart, use_container_width=True)


def boxplot_por_area():
    with st.expander("Boxplot das notas por área de conhecimento"):
        dados = {
            "Ciências da Natureza": {
                "2019": [400, 420, 450, 380, 500, 410, 430, 470, 395, 600],
                "2023": [420, 460, 490, 410, 520, 450, 470, 495, 430, 680]
            },
            "Ciências Humanas": {
                "2019": [450, 470, 490, 420, 510, 460, 480, 495, 430, 520],
                "2023": [470, 490, 510, 450, 530, 495, 500, 515, 460, 540]
            },
            "Linguagens e Códigos": {
                "2019": [470, 490, 500, 440, 510, 480, 495, 505, 460, 520],
                "2023": [480, 500, 510, 460, 520, 495, 505, 515, 470, 530]
            },
            "Matemática": {
                "2019": [450, 470, 480, 430, 490, 460, 470, 485, 440, 500],
                "2023": [460, 480, 490, 450, 500, 470, 480, 490, 460, 510]
            },
            "Redação": {
                "2019": [480, 500, 520, 460, 540, 490, 510, 530, 470, 560],
                "2023": [500, 520, 540, 480, 560, 510, 530, 550, 490, 580]
            }
        }

        cols = st.columns(2)
        i = 0
        for area, notas in dados.items():
            with cols[i % 2]:
                fig, ax = plt.subplots()
                ax.boxplot([notas["2019"], notas["2023"]], labels=["2019", "2023"])
                ax.set_title(area)
                ax.set_xlabel("Ano")
                ax.set_ylabel("Notas")
                st.pyplot(fig)
            i += 1


# Execução da aplicação
titulo()
inscritos()
filtros()
presenca()
medias_por_area()
boxplot_por_area()
