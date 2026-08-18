# Edubasi

Painel Streamlit para análise de microdados do ENEM.

## Rodar com Docker (1 container)

Pré-requisitos: [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.

Na raiz do projeto:

```bash
docker compose up --build
```

Acesse: http://localhost:8501

Para parar:

```bash
docker compose down
```

### Como funciona

- **Imagem**: app Python + Streamlit (`Dockerfile`)
- **Volumes**: microdados montados de `./microdados/` (não entram na imagem)
- **Config**: `app/config.docker.ini` montado como `/app/config.ini`

Estrutura esperada dos dados:

```
microdados/
├── participantes/
│   ├── 2018/
│   │   └── 2018_1301902.parquet
│   └── 2022/
└── provas/
    ├── ITENS_PROVA_2018.csv
    └── ITENS_PROVA_2022.csv
```

## Rodar localmente (sem Docker)

```bash
cd app
pip install -r ../requirements.txt
streamlit run app.py
```

Configure os caminhos em `app/config.ini`.
