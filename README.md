# Projeto ETL — Spotify

## Autores
   - **Nome**: Adriana Abreu, 53672 (Github: adriana1005 )
   - **Nome**: Leonor Rebola, 53663 (Github: leonorrebola9)

## Descrição do Trabalho
Este projeto implementa um pipeline ETL para análise de dados musicais, combinando dados do Million Playlist Dataset (MPD) e do Spotify Tracks Dataset do Kaggle com dados extraídos da Spotify Web API, com o objetivo de gerar insights sobre popularidade, géneros musicais e características das tracks.

---

## Estrutura do Projeto
projetoetl/
├── config/
├── data/
│   ├── raw/
│   │   ├── mpd/
│   │   └── spotify_api/
│   └── transformed/
├── extract/
│   ├── init.py
│   └── spotify_extractor.py
├── loading/
│   ├── load.py
├── tratamento/
│   ├── concatenate.py
│   └── duplicados.py
│   ├── juntar.py
│   └── missing_values.py
│   ├── outro.py
│   └── transformar.py
│   └── relatorio_qualidade.py
├── logs/
├── .env
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md

---

## Fontes de Dados
- **Million Playlist Dataset (MPD)** — dataset principal com playlists e tracks
- **Spotify Tracks Dataset** - dataset com dados complementares como `danceability` e `energy`
- **Spotify Web API** — dados complementares como `release_date` e `explicit`

---

## Requisitos

```bash
pip install -r requirements.txt
```

---

## Como Executar

1. Copiar o ficheiro `.env.example` para `.env` e preencher com as credenciais da Spotify API:
```bash
cp .env.example .env
```

2. Executar o pipeline:
```bash
python main.py
```

---

## Outputs
Ao longo do pipeline são gerados os seguintes ficheiros na pasta `data/`:
1. **tracks_batch_001.csv** — dados extraídos da Spotify API
2. **silver.csv** — dataset completo após limpeza e transformação
3. **gold.csv** — dataset com as variáveis usadas para análise

---

## Dashboard
O dashboard foi construído através do Power BI. Para visualizar:
1. Abrir o ficheiro `.pbix` incluído no repositório
2. Ligar ao SQL Server local com a base de dados `SpotifyDataset`

---

## Limitações
- A Spotify Web API tem restrições de rate limit que limitaram o volume de dados extraídos
- O campo `release_date` foi preenchido com a média por artista devido a valores em falta
- O campo `playlist_name` apresenta valores em branco no dataset original