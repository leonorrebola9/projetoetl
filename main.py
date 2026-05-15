import pandas as pd
import os
from extract.spotify_extractor import get_artists_from_csv, search_tracks, save_raw

# 1. Carregar todos os artistas
artists = get_artists_from_csv("data/final_limpo.csv")

# 2. Verificar quem já foi processado
ficheiro_saida = "tracks_batch_001.csv"
artistas_feitos = set()

if os.path.exists(f"data/raw/spotify_api/{ficheiro_saida}"):
    df_existente = pd.read_csv(f"data/raw/spotify_api/{ficheiro_saida}")
    # Guarda os nomes dos artistas que já estão no CSV
    artistas_feitos = set(df_existente["artist_searched"].unique())

# 3. Filtrar a lista: só pesquisar quem falta
artists_em_falta = [a for a in artists if a not in artistas_feitos]

print(f"Total inicial: {len(artists)} | Já feitos: {len(artistas_feitos)} | A pesquisar agora: {len(artists_em_falta)}")

# 4. Correr o script apenas para os que faltam
if artists_em_falta:
    tracks = search_tracks(artists_em_falta)
    # ATENÇÃO: Deves alterar a tua função save_raw para fazer "append" se o ficheiro já existir!