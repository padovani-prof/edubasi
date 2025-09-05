import pandas as pd
import os
import duckdb
import numpy as np

# (1) Q006: 
#       a. Atualizar dicionário de dados para:
#           A Nenhuma renda
#           B Até 1 salário mínimo
#           C Mais de 1 salário(s) até 1.5 salários
#           D Mais de 1.5 salário(s) até 2.0 salários
#           E Mais de 2.0 salário(s) até 2.5 salários
#           F Mais de 2.5 salário(s) até 3.0 salários
#           G Mais de 3.0 salário(s) até 4.0 salários
#           H Mais de 4.0 salário(s) até 5.0 salários
#           I Mais de 5.0 salário(s) até 6.0 salários
#           J Mais de 6.0 salário(s) até 7.0 salários
#           K Mais de 7.0 salário(s) até 8.0 salários
#           L Mais de 8.0 salário(s) até 9.0 salários
#           M Mais de 9.0 salário(s) até 10.0 salários
#           N Mais de 10.0 salário(s) até 12.0 salários
#           O Mais de 12.0 salário(s) até 15.0 salários
#           P Mais de 15.0 salário(s) até 20.0 salários
#           Q Mais de 20 salários
# (2) TP_ESCOLA: Transformar 3 em 4 e 4 em 3 em 2018
# (3) TP_ESTADO_CIVIL: 
#       a. Somar 1 em 2018
#       b. Substituir nulos por 0
# (4) TP_PRESENCA_CN, TP_PRESENCA_CH, TP_PRESENCA_LC e TP_PRESENCA_MT: substituir nan por 0 em 2018

def apagar_colunas_mescladas(df):
    subset_cols = df.columns[1:6]
    return df.dropna(subset=subset_cols, how="all")
    
def preencher_colunas(df):
    for i in [0, 4, 5]:
        df.iloc[:, i] = df.iloc[:, i].fillna(method="ffill")
    return df

def obter_nomes_das_colunas(df):
    nomes = df.iloc[:, 0].unique()
    return set(nomes)

# (1) Tudo igual até coluna Q025 - as demais colunas não são usadas na análise    
def mostrar_diferenca_de_nomes_de_colunas(ano1, ano2):
    caminho = f"C:/Users/klebe/Downloads/microdados_enem_{ano1}/DICIONÁRIO/Dicionário_Microdados_Enem_{ano1}.xlsx"
    df1 = pd.read_excel(caminho, skiprows=6, dtype=str)
    df1 = apagar_colunas_mescladas(df1)
    df1 = preencher_colunas(df1)
    caminho = f"C:/Users/klebe/Downloads/microdados_enem_{ano2}/DICIONÁRIO/Dicionário_Microdados_Enem_{ano2}.xlsx"
    df2 = pd.read_excel(caminho, skiprows=6, dtype=str)
    df2 = apagar_colunas_mescladas(df2)
    df2 = preencher_colunas(df2)
    cols1 = obter_nomes_das_colunas(df1)
    cols2 = obter_nomes_das_colunas(df2)
    aux = cols1.difference(cols2)
    aux = ", ".join(aux) if len(aux) > 0 else "Nenhuma"
    aux = f"{ano1} - {ano2}: " + aux
    print(aux)    

def colunas_comuns():
    print("Diferenças entre as colunas")
    for ano1 in range(2018,2023):
        for ano2 in range(ano1 + 1,2024):
            mostrar_diferenca_de_nomes_de_colunas(ano1, ano2)
    print()

# (1) Q006: Renda - Salários mínimos?
# (2) TP_ANO_CONCLUIU: não usamos
#        - valor 1 corresponde ao ano - 1
#        - valor 2 corresponde ao ano - 2
#        ...
#        - último valor varia de um ano para outro, mas corresponde a antes do anterior
#        - Intervalos:
#           + 2023: 0=Não informado, 1=2022, 2=2021, ..., 17=antes de 2007
#           + 2022: 0=Não informado, 1=2021, 2=2020, ..., 16=antes de 2007
#           + 2021: 0=Não informado, 1=2020, 2=2019, ..., 15=antes de 2007
#           + 2020: 0=Não informado, 1=2019, 2=2018, ..., 14=antes de 2007
#           + 2019: 0=Não informado, 1=2018, 2=2017, ..., 13=antes de 2007
#           + 2018: 0=Não informado, 1=2017, 2=2016, ..., 12=antes de 2007
# (3) TP_ESCOLA: 1 e 2 consistentes; 3 é exterior em 2018 e privada nos demais; 4 é privada em 2018 e exterior nos demais
# (4) TP_ESTADO_CIVIL: 
#           + 0 é solteiro(a) em 2018 e não informado nos demais
#           + 1 é casado/mora com companheiro(a) em 2018 e solteiro(a) nos demais
#           + 2 é Divorciado(a)/Desquitado(a)/Separado(a) em 2018 e casado/mora com companheiro(a)
#           + 3 é Viúvo(a) em 2018 e Divorciado(a)/Desquitado(a)/Separado(a) nos demais
#           + 4 é Viúvo nos demais (2018 não tem esse valor)
#           = Ou seja, 2018 precisa ser somado em 1
# (5) TP_ST_CONCLUSAO: Não usamos
# (6) TP_ENSINO: Tem ano que não tem alguns valores, mas os que existem estão consistentes
# (7) TP_COR_RACA: Tem ano que não tem alguns valores, mas os que existem estão consistentes 
def mostrar_colunas_com_valores_diferentes_entre_dois_anos(ano1, ano2):
    caminho = f"C:/Users/klebe/Downloads/microdados_enem_{ano1}/DICIONÁRIO/Dicionário_Microdados_Enem_{ano1}.xlsx"
    df1 = pd.read_excel(caminho, skiprows=6, dtype=str)
    df1 = apagar_colunas_mescladas(df1)
    df1 = preencher_colunas(df1)
    for i in range(6):
        df1.iloc[:, i] = df1.iloc[:, i].str.strip()
    caminho = f"C:/Users/klebe/Downloads/microdados_enem_{ano2}/DICIONÁRIO/Dicionário_Microdados_Enem_{ano2}.xlsx"
    df2 = pd.read_excel(caminho, skiprows=6, dtype=str)
    df2 = apagar_colunas_mescladas(df2)
    df2 = preencher_colunas(df2)
    for i in range(6):
        df2.iloc[:, i] = df2.iloc[:, i].str.strip()
    
    set1 = set(df1.itertuples(index=False, name=None))
    set2 = set(df2.itertuples(index=False, name=None))

    df1_not_in_df2 = set1 - set2
    df2_not_in_df1 = set2 - set1

    #for i in df1_not_in_df2:
    #    input(i)

    valores_df1_unicos = sorted({t[0] for t in df1_not_in_df2})
    valores_df2_unicos = sorted({t[0] for t in df2_not_in_df1})


        

    print(f"==> {ano1} - {ano2}:", ", ".join(list(valores_df1_unicos)))
    print()
    print(f"==> {ano2} - {ano1}:", ", ".join(list(valores_df2_unicos)))
    print()
    return valores_df1_unicos, valores_df2_unicos
    
    
def colunas_com_valores_diferentes():
    print("Diferenças entre as colunas")
    print()
    colunas_problematicas = set()
    for ano1 in range(2018,2023):
        for ano2 in range(ano1 + 1,2024):
            a, b = mostrar_colunas_com_valores_diferentes_entre_dois_anos(ano1, ano2)
            for i in a:
                colunas_problematicas.add(i)
            for i in b:
                colunas_problematicas.add(i)
            #input()
    print()
    print("Resumo de colunas com problema: " + ", ".join(colunas_problematicas))
    
def mostrar_valores_da_coluna():
    coluna = input("Coluna: ").strip().upper()
    aux = []
    for ano in range(2018, 2024):
        caminho = f"C:/Users/klebe/Downloads/microdados_enem_{ano}/DICIONÁRIO/Dicionário_Microdados_Enem_{ano}.xlsx"
        df1 = pd.read_excel(caminho, skiprows=6, dtype=str)
        df1 = apagar_colunas_mescladas(df1)
        df1 = preencher_colunas(df1)
        df1.iloc[:, 0] = df1.iloc[:, 0].str.strip()
        for i in set(df1.itertuples(index=False, name=None)):
            if i[0] == coluna:
                aux.append((str(ano), i[0], i[2], i[3]))
    aux.sort(key=lambda x : x[2])
    print("\n".join([str(i) for i in aux]))
    input()

def verificar_colunas_com_nulo(df: pd.DataFrame):
    """
    Mostra os nomes das colunas que contêm pelo menos:
    - valor nulo real (None ou np.nan)
    - string 'nan' (qualquer caixa)
    - string 'none' (qualquer caixa)
    """
    colunas_com_nulo = []
    for col in df.columns:
        
        # Verifica valores nulos reais (None ou np.nan)
        tem_nulo = df[col].isna()
        # Verifica strings 'nan' ou 'none', ignorando maiúsculas/minúsculas
        tem_nan_none_str = df[col].astype(str).str.lower().str.strip().isin(['nan', 'none', ''])
        
        if tem_nulo.any() or tem_nan_none_str.any():
            colunas_com_nulo.append(col)
    return colunas_com_nulo

# 2018: ['TP_ESTADO_CIVIL', 'TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO', 'Q026']
# 2019: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO']
# 2020: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO', 'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022', 'Q023', 'Q024', 'Q025']
# 2021: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO', 'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022', 'Q023', 'Q024', 'Q025']
# 2022: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO']
# 2023: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO']
def processar_parquets_e_verificar_nulos(diretorio: str):
    for ano in range(2018, 2024):
        print(ano, flush=True, end=": ")
        path = f"C:\\Users\\klebe\\Downloads\\microdados_enem_{ano}\\DADOS\\MICRODADOS_ENEM_{ano}.csv"
        df = pd.read_csv(path, encoding="ISO-8859-1", sep=";", dtype=str)
        cols = verificar_colunas_com_nulo(df)
        print(cols)
        del df

# Comuns: ['CO_MUNICIPIO_ESC', 'CO_PROVA_CH', 'CO_PROVA_CN', 'CO_PROVA_LC', 'CO_PROVA_MT', 'CO_UF_ESC', 'NO_MUNICIPIO_ESC', 'NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_ENSINO', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'TP_STATUS_REDACAO', 'TX_GABARITO_CH', 'TX_GABARITO_CN', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT']
# Exclusivas:
#   2018 ['TP_ESTADO_CIVIL', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'Q026']
#   2020 ['Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022', 'Q023', 'Q024', 'Q025']
#   2021 ['Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022', 'Q023', 'Q024', 'Q025']
def ver_colunas_com_nulos_agrupadas():
    cols = {
        2018: ['TP_ESTADO_CIVIL', 'TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO', 'Q026'],
        2019: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO'],
        2020: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO', 'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022', 'Q023', 'Q024', 'Q025'],
        2021: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO', 'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022', 'Q023', 'Q024', 'Q025'],
        2022: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO'],
        2023: ['TP_ENSINO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO']
    }
    comuns = None
    for a, c in cols.items():
        aux = set()
        for i in c:
            aux.add(i)
        if comuns is None:
            comuns = aux
        else:
            comuns = comuns.intersection(aux)
    comuns = list(comuns)
    comuns.sort()
    print("Comuns: " + str(comuns))
    exclusivas = {}
    for a, c in cols.items():
        for i in c:
            if i not in comuns:
                exclusivas[a] = exclusivas.get(a, [])
                exclusivas[a].append(i)
    aux = list(exclusivas.keys())
    aux.sort()
    print("Exclusivas: ")
    for a in aux:
        c = exclusivas[a]
        print(a, c)

def auxiliar2():
    salarios = {}
    for ano1 in range(2018, 2024):
        caminho = f"C:/Users/klebe/Downloads/microdados_enem_{ano1}/DICIONÁRIO/Dicionário_Microdados_Enem_{ano1}.xlsx"
        df1 = pd.read_excel(caminho, skiprows=[0,1,3,4], dtype=str)
        df1 = apagar_colunas_mescladas(df1)
        df1 = preencher_colunas(df1)
        df1 = df1[df1["NOME DA VARIÁVEL"] == "Q006"][["NOME DA VARIÁVEL", 'Variáveis Categóricas', 'Unnamed: 3']]
        df2 = df1[df1["Variáveis Categóricas"] == "B"][["NOME DA VARIÁVEL", 'Variáveis Categóricas', 'Unnamed: 3']]
        aux = list(df2["Unnamed: 3"].str.split(" "))[0]
        for ix, valor in enumerate(aux):
            if valor == "R$":
                minimo = aux[ix+1].strip()
                if not minimo[-1].isdigit():
                    minimo = minimo[:-1]
                minimo = minimo.replace('.', '')
                minimo = float(minimo.replace(',', '.'))
                print("=============================================")
                print("Mínimo:", minimo)
                letra = "C"
                i = 1.5
                while ord(letra) <= ord("Q"):
                    texto = list(df1[df1["Variáveis Categóricas"] == letra][["NOME DA VARIÁVEL", 'Variáveis Categóricas', 'Unnamed: 3']]["Unnamed: 3"])[0]
                    if texto[-1] == '.':
                        texto = texto[:-1]
                    print("Alvo:", texto)
                    inicial = minimo + 0.01
                    inicial = f"{inicial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    achou = None
                    while i <= 50:
                        final = minimo * i
                        proximo = final + 0.01
                        final = f"{final:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        novo = f"De R$ {inicial} até R$ {final}"
                        print("\tXXXXXXXXXXXXXXXXXX", novo)
                        #input()
                        if texto == novo:
                            achou = (letra, i)
                            break
                        inicial = proximo
                        inicial = f"{inicial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        i += 0.5
                    print(achou)
                    letra = chr(ord(letra)+1)
                # print(f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                break
                # df_ordenado = df.sort_values(by="idade")
        break

def auxiliar3():
    salarios = {}
    
    for ano1 in range(2018, 2024):
        salarios[ano1] = []
        caminho = f"C:/Users/klebe/Downloads/microdados_enem_{ano1}/DICIONÁRIO/Dicionário_Microdados_Enem_{ano1}.xlsx"
        df1 = pd.read_excel(caminho, skiprows=[0,1,3,4], dtype=str)
        df1 = apagar_colunas_mescladas(df1)
        df1 = preencher_colunas(df1)
        df1 = df1[df1["NOME DA VARIÁVEL"] == "Q006"][["NOME DA VARIÁVEL", 'Variáveis Categóricas', 'Unnamed: 3']]
        df2 = df1[df1["Variáveis Categóricas"] == "B"][["NOME DA VARIÁVEL", 'Variáveis Categóricas', 'Unnamed: 3']]
        aux = list(df2["Unnamed: 3"].str.split(" "))[0]
        for ix, valor in enumerate(aux):
            if valor == "R$":
                minimo = aux[ix+1].strip()
                if not minimo[-1].isdigit():
                    minimo = minimo[:-1]
                minimo = minimo.replace('.', '')
                minimo = float(minimo.replace(',', '.'))
                inicial = minimo + 0.01
                base = 1
                print("=============================================")
                print("Mínimo:", minimo, "Ano:", ano1)
                letra = "C"
                i = 1.5
                while ord(letra) <= ord("P"):
                    texto = list(df1[df1["Variáveis Categóricas"] == letra][["NOME DA VARIÁVEL", 'Variáveis Categóricas', 'Unnamed: 3']]["Unnamed: 3"])[0]
                    if texto[-1] == '.':
                        texto = texto[:-1]
                    #print("\tAlvo:", texto)

                    while i < 50:
                        final = minimo * i
                        inicial_str = f"{inicial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        final_str = f"{final:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        novo = f"De R$ {inicial_str} até R$ {final_str}"
                        #print("\t\t" + novo)
                        #input()
                        i += 0.5
                        if novo == texto:
                            inicial = final + 0.01
                            print("\t\tAchou!", letra, base, final/minimo)
                            salarios[ano1].append((base, final/minimo))
                            base = final/minimo
                            break


                    # segura inicial e vai aumentando final de meio em meio
                    # quando achar, inicial = final + 0.01
                    letra = chr(ord(letra)+1)
    for ano, v in salarios.items():
        print(ano, v)
    print("A", "Nenhuma renda")
    print("B", "Até 1 salário mínimo")
    for i in range(14):
        aux = None
        intervalo = salarios[2018][i]
        print(chr(ord('C') + i), "Mais de", intervalo[0], "salário(s) até", intervalo[1], "salários")
    print("Q", "Mais de 20 salários")
# mostrar_valores_da_coluna(), exit()
# colunas_comuns() # verifica quais colunas aparecem em um ano e não aparecem no outro (combinados os anos aos pares)
# colunas_com_valores_diferentes() # verifica quais colunas entre os anos que possuem valores diferentes (como a renda)
# processar_parquets_e_verificar_nulos("C:\\Users\\klebe\\Downloads\\dash\\dados_parquet\\")
# ver_colunas_com_nulos_agrupadas()
auxiliar3()
