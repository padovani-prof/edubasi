# Instruções

1) Instale as bibliotecas do Python (numpy, pandas, streamlit, duckdb, matplotlib, plotly, openpyxl) com esse comando py -m pip install -r requirements.txt
2) Baixe os códigos deste repositório
3) Baixe os arquivos do banco de dados e os extraia em uma pasta
4) Altere as definições do arquivo config.ini da pasta app
5) Execute o streamlit sobre app.py a partir da pasta app



6) Configure os caminhos dos microdados no arquivo config.ini:
   - parquet_dir: pasta com os arquivos parquet dos participantes (por ano/município)
   - parquet_provas_questoes: pasta com os arquivos ITENS_PROVA_{ano}.csv

exe:
parquet_dir=C:\caminho\microdados\participantes
parquet_provas_questoes=C:\caminho\microdados\provas
