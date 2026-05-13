import json
import csv

# Ler JSON
with open('data/mpd.slice.23000-23999.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)

# Lista para guardar todas as músicas
linhas = []

# Percorrer playlists
for playlist in dados["playlists"]:

    nome_playlist = playlist["name"]
    pid = playlist["pid"]

    # Percorrer tracks
    for track in playlist["tracks"]:

        linha = {
            "playlist_name": nome_playlist,
            "playlist_id": pid,
            "pos": track["pos"],
            "artist_name": track["artist_name"],
            "track_name": track["track_name"],
            "album_name": track["album_name"],
            "duration_ms": track["duration_ms"],
            "track_uri": track["track_uri"]
        }

        linhas.append(linha)

# Escrever CS
with open('03.csv', 'w', newline='', encoding='utf-8') as csvfile:

    colunas = linhas[0].keys()

    writer = csv.DictWriter(csvfile, fieldnames=colunas)

    writer.writeheader()
    writer.writerows(linhas)

print("CSV criado com sucesso!")