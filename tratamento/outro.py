import pandas as pd

# --- Carregar dados ---
df = pd.read_csv("data/transformed/final_combinado.csv")

print("=== Antes do preenchimento ===")
print(df.isnull().sum()[df.isnull().sum() > 0])
print(f"Total de linhas: {len(df)}\n")

# --- Identificar colunas com valores em falta ---
colunas_com_nulos = [col for col in df.columns if df[col].isnull().any()]
print(f"Colunas com valores em falta: {colunas_com_nulos}\n")

# --- Preencher com a média por artista ---
for col in colunas_com_nulos:
    col_numerica = pd.to_numeric(df[col], errors="coerce")

    if col_numerica.notnull().any():
        df[col] = col_numerica
        media_por_artista = df.groupby("artist_name")[col].transform("mean")
        df[col] = df[col].fillna(media_por_artista)

        media_global = df[col].mean()
        df[col] = df[col].fillna(media_global)

        print(f"[Numérica] '{col}' preenchida com média por artista.")
    else:
        moda_por_artista = df.groupby("artist_name")[col].transform(
            lambda x: x.mode().iloc[0] if x.notna().any() else pd.NA
        )
        df[col] = df[col].fillna(moda_por_artista)

        moda_global = df[col].mode()
        if not moda_global.empty:
            df[col] = df[col].fillna(moda_global.iloc[0])

        print(f"[Texto]    '{col}' preenchida com moda por artista.")

# --- Converter 'explicit' para True/False ---
df["explicit"] = df["explicit"].apply(lambda x: True if x >= 0.5 else False)
print("\n'explicit' convertida para True/False (>= 0.5 → True, caso contrário → False).")

print()
print("=== Depois do preenchimento ===")
restantes = df.isnull().sum()[df.isnull().sum() > 0]
if restantes.empty:
    print("Nenhum valor em falta restante!")
else:
    print(restantes)

# --- Guardar resultado ---
output_path = "data/transformed/final_combinado2_preenchido.csv"
df.to_csv(output_path, index=False)
print(f"\nFicheiro guardado em: {output_path}")