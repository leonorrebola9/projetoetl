import pandas as pd
'''
# Ler CSV
df = pd.read_csv("projetoetl/data/final.csv")

dups = df.duplicated(subset=["track_name"], keep=False)
print(f"Total de duplicados: {dups.sum()}")

# Remover duplicados pela coluna track_name
df = df.drop_duplicates(subset=["track_name"])

# Guardar novo CSV
df.to_csv("sem_duplicados.csv", index=False)

print("Duplicados removidos!")
'''

import pandas as pd

# Ler CSV
df = pd.read_csv("projetoetl/data/resultado_final.csv",
    encoding="latin1",
    sep=None,
    engine="python")

# Remover linhas onde popularity está vazia
df = df.dropna(subset=["popularity"])

# Guardar novo CSV
df.to_csv("projetoetl/data/final_limpo.csv", index=False)

print("Linhas removidas!")