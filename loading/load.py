import pandas as pd
from sqlalchemy import create_engine

# Ler o gold
df = pd.read_csv("data/transformed/gold.csv")

# Ligação ao SQL Server
engine = create_engine(
    "mssql+pyodbc://localhost/SpotifyDataset?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# Carregar para a tabela
df.to_sql("tracks", engine, if_exists="replace", index=False)
print(f"Carregadas {len(df)} linhas para a tabela 'tracks'")