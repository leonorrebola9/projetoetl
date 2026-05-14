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
        requests_timeout=5
    )


def get_artists_from_csv(csv_path: str) -> list:
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


def search_tracks(artist_names: list) -> list:
    sp = get_spotify_client()
    all_tracks = []
    total_artists = len(artist_names)

    for i, artist_name in enumerate(artist_names):
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
                    "popularity": item["popularity"],
                    "duration_ms": item["duration_ms"],
                    "explicit": item["explicit"],
                    "track_id": item["id"]
                })

            logging.info(f"{artist_name} -> {len(result['tracks']['items'])} tracks")
            time.sleep(0.2)

        except SpotifyException as e:
            print(f"Spotify error em {artist_name}: {e}")
            logging.error(f"Spotify error {artist_name}: {e}")
            time.sleep(3)

        except Exception as e:
            print(f"Erro em {artist_name}: {e}")
            logging.error(f"Erro {artist_name}: {e}")

    return all_tracks


def save_raw(data: list, filename: str, output_path: str = OUTPUT_PATH):
    Path(output_path).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_path) / filename
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    logging.info(f"Saved {len(data)} records to {filepath}")
    print(f"CSV guardado: {filepath}")