import pandas as pd
import os

df_mpd = pd.read_csv("data/final_limpo.csv", sep=";", encoding="latin1")
df_api = pd.read_csv("data/tracks_batch_002.csv", encoding="latin1")

# Extrair track_id do track_uri
df_mpd["track_id"] = df_mpd["track_uri"].str.split(":").str[-1]

# Manter só as colunas úteis da API
df_api = df_api[["track_id", "release_date", "explicit"]]

# Join
df_final = df_mpd.merge(df_api, on="track_id", how="left")

os.makedirs("data/transformed/", exist_ok=True)
df_final.to_csv("data/transformed/final_combinado2.csv", index=False)
print(df_final.shape)
print(df_final.head())