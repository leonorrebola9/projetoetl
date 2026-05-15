import pandas as pd

# Ler os CSVs
df1 = pd.read_csv("projetoetl/data/03.csv")
df2 = pd.read_csv(
    "projetoetl/data/sem_duplicados.csv",
    encoding="cp1252",
    sep=";"
)

# Escolher apenas as colunas necessárias do segundo CSV
df2 = df2[
    [
        "artists",
        "track_name",
        "popularity",
        "energy",
        "danceability",
        "liveness",
        "valence",
        "track_genre"
    ]
]

# Fazer o merge
resultado = pd.merge(
    df1,
    df2,
    left_on=["artist_name", "track_name"],
    right_on=["artists", "track_name"],
    how="left"
)

# (Opcional) remover coluna duplicada artists
resultado = resultado.drop(columns=["artists"])

# Guardar resultado
resultado.to_csv("resultado_final03.csv", index=False)

print("Merge concluído!")