# Projeto ETL — Spotify

## Autores
   - **Nome**: Adriana Abreu, 53672 (Github: adriana1005 )
   - **Nome**: Leonor Rebola, 53663 (Github: leonorrebola9)

## Descrição do Trabalho
Este projeto implementa um pipeline ETL para análise de dados musicais, combinando dados do Million Playlist Dataset (MPD) e do Spotify Tracks Dataset do Kaggle com dados extraídos da Spotify Web API, com o objetivo de gerar insights sobre popularidade, géneros musicais e características das tracks.

---

## Estrutura do Projeto
projetoetl/
├── extract/
│   ├── init.py
│   └── spotify_extractor.py
├── data/
│   ├── raw/
│   │   ├── mpd/
│   │   └── spotify_api/
│   └── transformed/
├── logs/
├── .env
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md

---

## Requisitos

```bash
pip install -r requirements.txt
```

---

## 
```

---

## Fontes de Dados
- **Million Playlist Dataset (MPD)** — dataset principal com playlists e tracks
- **Spotify Tracks Dataset** - dataset com dados complementares como `danceability` e `energy`
- **Spotify Web API** — dados complementares como `release_date` e `explicit`

---
