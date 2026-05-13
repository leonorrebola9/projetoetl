import logging
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

load_dotenv()

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/extract.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
    return spotipy.Spotify(auth_manager=auth_manager, requests_timeout=10)

def search_tracks(artist_names: list, limit: int = 10) -> list:
    """Busca tracks por nome de artista."""
    sp = get_spotify_client()
    tracks = []

    for artist_name in artist_names:
        print(f"A buscar: {artist_name}")
        results = sp.search(q=artist_name, type="track", limit=limit)

        for item in results["tracks"]["items"]:
            tracks.append({
                "track_name": item.get("name"),
                "artist": item["artists"][0]["name"],
                "album": item["album"]["name"],
                "release_date": item["album"]["release_date"],
                "popularity": item.get("popularity"),
                "duration_ms": item.get("duration_ms"),
                "explicit": item.get("explicit"),
                "track_id": item.get("id")
            })

        logging.info(f"Fetched {limit} tracks for artist: {artist_name}")

    return tracks

def save_raw(data: list, filename: str, output_path: str = "data/raw/spotify_api/"):
    """Guarda os dados brutos em CSV sem transformações."""
    Path(output_path).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_path) / filename
    pd.DataFrame(data).to_csv(filepath, index=False)
    logging.info(f"Saved {len(data)} records to {filepath}")

def get_artists_from_slices(slices_path: str) -> list:
    """Extrai nomes de artistas únicos dos slices do MPD."""
    path = Path(slices_path)
    slices = sorted(path.glob("*.json"))
    
    artists = set()
    
    for filepath in slices:
        logging.info(f"Reading slice: {filepath.name}")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for playlist in data["playlists"]:
            for track in playlist["tracks"]:
                artists.add(track["artist_name"])
    
    logging.info(f"Found {len(artists)} unique artists")
    return list(artists)

def get_artists_from_csv(csv_path: str) -> list:
    """Extrai nomes de artistas únicos do CSV."""
    df = pd.read_csv(csv_path)
    artists = df["artist_name"].dropna().unique().tolist()
    logging.info(f"Found {len(artists)} unique artists from CSV")
    return artists