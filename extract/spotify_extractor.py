import logging
import os
import time
from pathlib import Path

import pandas as pd
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException


# =========================================================
# CONFIG
# =========================================================

load_dotenv()

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/extract.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

OUTPUT_PATH = "data/raw/spotify_api/"


# =========================================================
# SPOTIFY CLIENT
# =========================================================

def get_spotify_client():
    """
    Cria cliente Spotify.
    """

    auth_manager = SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )

    return spotipy.Spotify(
        auth_manager=auth_manager,
        requests_timeout=5
    )


# =========================================================
# GET ARTISTS FROM CSV
# =========================================================

def get_artists_from_csv(csv_path: str) -> list:
    """
    Extrai artistas únicos do CSV.
    """

    df = pd.read_csv(csv_path)

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


# =========================================================
# FETCH TRACKS
# =========================================================

def search_tracks(artist_names: list) -> list:
    """
    Busca top tracks de cada artista.
    """

    sp = get_spotify_client()

    all_tracks = []

    total_artists = len(artist_names)

    for i, artist_name in enumerate(artist_names):

        try:

            print(
                f"[{i+1}/{total_artists}] "
                f"A buscar: {artist_name}"
            )

            # -------------------------------------------------
            # Procurar artista
            # -------------------------------------------------

            result = sp.search(
                q=f'artist:"{artist_name}"',
                type="artist",
                limit=1
            )

            items = result["artists"]["items"]

            if not items:

                print(f"Nenhum artista encontrado: {artist_name}")

                continue

            artist_data = items[0]

            artist_id = artist_data["id"]

            # -------------------------------------------------
            # Buscar top tracks
            # -------------------------------------------------

            top_tracks = sp.artist_top_tracks(artist_id)["tracks"]

            for track in top_tracks:

                all_tracks.append({
                    "artist_searched": artist_name,
                    "artist": track["artists"][0]["name"],
                    "track_name": track["name"],
                    "album": track["album"]["name"],
                    "release_date": track["album"]["release_date"],
                    "popularity": track["popularity"],
                    "duration_ms": track["duration_ms"],
                    "explicit": track["explicit"],
                    "track_id": track["id"]
                })

            logging.info(
                f"{artist_name} -> "
                f"{len(top_tracks)} tracks"
            )

            # -------------------------------------------------
            # Pequena pausa anti-rate-limit
            # -------------------------------------------------

            time.sleep(0.2)

        except SpotifyException as e:

            print(f"Spotify error em {artist_name}: {e}")

            logging.error(
                f"Spotify error {artist_name}: {e}"
            )

            # esperar um pouco se houver rate limit
            time.sleep(3)

        except Exception as e:

            print(f"Erro em {artist_name}: {e}")

            logging.error(
                f"Erro {artist_name}: {e}"
            )

    return all_tracks


# =========================================================
# SAVE CSV
# =========================================================

def save_raw(
    data: list,
    filename: str,
    output_path: str = OUTPUT_PATH
):
    """
    Guarda CSV.
    """

    Path(output_path).mkdir(
        parents=True,
        exist_ok=True
    )

    filepath = Path(output_path) / filename

    df = pd.DataFrame(data)

    df.to_csv(filepath, index=False)

    logging.info(
        f"Saved {len(data)} records to {filepath}"
    )

    print(f"CSV guardado: {filepath}")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    artists = get_artists_from_csv(
        "data/final_limpo.csv"
    )

    # TESTE PEQUENO PRIMEIRO
    artists = artists[:20]

    print(
        f"Artistas encontrados: {len(artists)}"
    )

    tracks = search_tracks(artists)

    save_raw(
        tracks,
        "tracks_batch_001.csv"
    )

    print(
        f"Tracks guardadas: {len(tracks)}"
    )