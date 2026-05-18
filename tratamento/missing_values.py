import pandas as pd

# --- Carregar dados ---
df = pd.read_csv("data/transformed/final_combinado.csv")

print("=== Antes do preenchimento ===")
print(df.isnull().sum()[df.isnull().sum() > 0])
print(f"Total de linhas: {len(df)}\n")

# --- Identificar colunas com valores em falta ---
# Inclui colunas numéricas (float64/int64) e colunas object com NaN (ex: release_date, explicit)
colunas_com_nulos = [col for col in df.columns if df[col].isnull().any()]
print(f"Colunas com valores em falta: {colunas_com_nulos}\n")

# --- Preencher com a média por artista (apenas colunas numéricas) ---
# Para colunas como 'explicit' e 'release_date' que são lidas como object mas têm NaN,
# tentamos converter para numérico e calcular a média
for col in colunas_com_nulos:
    # Tentar converter para numérico (ignora valores não convertíveis)
    col_numerica = pd.to_numeric(df[col], errors="coerce")

    if col_numerica.notnull().any():
        # É uma coluna com valores numéricos → preencher com média por artista
        df[col] = col_numerica  # garantir tipo numérico
        media_por_artista = df.groupby("artist_name")[col].transform("mean")
        df[col] = df[col].fillna(media_por_artista)

        # Fallback: média global para artistas sem nenhum valor
        media_global = df[col].mean()
        df[col] = df[col].fillna(media_global)

        print(f"[Numérica] '{col}' preenchida com média por artista.")
    else:
        # Coluna de texto → preencher com o valor mais frequente (moda) por artista
        moda_por_artista = df.groupby("artist_name")[col].transform(
            lambda x: x.mode().iloc[0] if x.notna().any() else pd.NA
        )
        df[col] = df[col].fillna(moda_por_artista)

        # Fallback: moda global
        moda_global = df[col].mode()
        if not moda_global.empty:
            df[col] = df[col].fillna(moda_global.iloc[0])

        print(f"[Texto]    '{col}' preenchida com moda por artista.")

print()
print("=== Depois do preenchimento ===")
restantes = df.isnull().sum()[df.isnull().sum() > 0]
if restantes.empty:
    print("Nenhum valor em falta restante!")
else:
    print(restantes)

# --- Remover duplicados ---
antes = len(df)
df = df.drop_duplicates(subset=["track_id", "playlist_id"])
depois = len(df)
print(f"Duplicados removidos: {antes - depois}")

# --- Normalizar tipos ---
df["duration_min"] = (df["duration_ms"] / 60000).round(2)
df["explicit"] = df["explicit"].map({True: 1, False: 0, "True": 1, "False": 0}).fillna(0).astype(int)

# --- Camada gold: só colunas relevantes para análise ---
colunas_gold = [
    "track_id", "track_name", "artist_name", "album_name",
    "playlist_name", "playlist_id", "track_genre",
    "popularity", "energy", "danceability", "liveness", "valence",
    "duration_min", "explicit"
]
df_gold = df[colunas_gold]

# --- Guardar camada staging (silver) ---
df.to_csv("data/transformed/silver.csv", index=False)
print("Camada silver guardada!")

# --- Guardar camada gold ---
df_gold.to_csv("data/transformed/gold.csv", index=False)
print("Camada gold guardada!")


# --- Guardar resultado ---
output_path = "data/transformed/final_combinado_preenchido.csv"
df.to_csv(output_path, index=False)
print(f"\nFicheiro guardado em: {output_path}")