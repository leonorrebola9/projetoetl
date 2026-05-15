import logging
import os
import time
from pathlib import Path

import pandas as pd
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

load_dotenv()

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/extract.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

OUTPUT_PATH = "data/raw/spotify_api/"


def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
    return spotipy.Spotify(
        auth_manager=auth_manager,
        requests_timeout=5,
        retries=0,           # Impede que o urllib3 tente novamente em loop
        status_retries=0     # Desliga as tentativas de retry em erros 429
    )


def get_artists_from_csv(csv_path: str) -> list:
    df = pd.read_csv(csv_path, encoding="latin1", sep=';')
    artists = (
        df["artist_name"]
        .dropna()
        .str.strip()
        .str.lower()
        .unique()
        .tolist()
    )
    logging.info(f"{len(artists)} artistas únicos encontrados")
    return artists


def search_tracks(artist_names: list) -> list:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    print(f"DEBUG: Client ID carregado? {'Sim' if client_id else 'Não'}")

    sp = get_spotify_client()
    all_tracks = []
    total_artists = len(artist_names)

    for i, artist_name in enumerate(artist_names):
            sucesso = False
            
            while not sucesso:
                try:
                    print(f"[{i+1}/{total_artists}] A buscar: {artist_name}")

                    result = sp.search(
                        q=f'artist:{artist_name}',
                        type="track",
                        limit=10
                    )

                    for item in result["tracks"]["items"]:
                        all_tracks.append({
                            "artist_searched": artist_name,
                            "artist": item["artists"][0]["name"],
                            "track_name": item["name"],
                            "album": item["album"]["name"],
                            "release_date": item["album"]["release_date"],
                            "popularity": item.get("popularity"),
                            "duration_ms": item.get("duration_ms"),
                            "explicit": item.get("explicit"),
                            "track_id": item["id"]
                        })

                    logging.info(f"{artist_name} -> {len(result['tracks']['items'])} tracks")
                    time.sleep(1) 
                    sucesso = True 

                except SpotifyException as e:
                    if e.http_status == 429:
                        espera = 60
                        if hasattr(e, 'headers') and 'Retry-After' in e.headers:
                            try:
                                espera = int(e.headers['Retry-After'])
                            except ValueError:
                                pass
                        
                        print(f"Rate limit atingido! A dormir por {espera} segundos")
                        time.sleep(espera)
                    else:
                        print(f"Spotify error em {artist_name}: {e}")
                        logging.error(f"Spotify error {artist_name}: {e}")
                        break

                except KeyboardInterrupt:
                    # 1. COLETE SALVA-VIDAS: Se carregares Ctrl+C, ele apanha o aviso!
                    print(f"\n🚨 Paragem manual detetada no artista {artist_name}! A sair e a guardar o que temos...")
                    return all_tracks # Devolve logo o que já sacou para o main.py guardar

                except Exception as e:
                    print(f"Erro inesperado em {artist_name}: {e}")
                    logging.error(f"Erro inesperado {artist_name}: {e}")
                    break 
                    
            # 2. AUTO-SAVE: A cada 50 artistas processados com sucesso, guarda um backup
            if (i + 1) % 50 == 0:
                df_backup = pd.DataFrame(all_tracks)
                # Guarda na mesma pasta com o nome backup
                df_backup.to_csv("data/raw/spotify_api/backup_temporario.csv", index=False)
                print(f"Auto-save feito para {i+1} artistas!")

    return all_tracks


def save_raw(data: list, filename: str, output_path: str = OUTPUT_PATH):
    Path(output_path).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_path) / filename
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    logging.info(f"Saved {len(data)} records to {filepath}")
    print(f"CSV guardado: {filepath}")