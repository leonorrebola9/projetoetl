import requests
import logging
import time
import json
from pathlib import Path
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

logging.basicConfig(
    filename="logs/extract.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def get_access_token() -> str:
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    )
    response.raise_for_status()
    token = response.json()["access_token"]
    logging.info("Spotify access token obtained")
    return token

def get_audio_features(track_ids: list, token: str) -> list:
    """Busca audio features para até 100 tracks de uma vez."""
    url = "https://api.spotify.com/v1/audio-features"
    headers = {"Authorization": f"Bearer {token}"}
    
    results = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        params = {"ids": ",".join(batch)}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            logging.warning(f"Rate limited. Waiting {retry_after}s")
            time.sleep(retry_after)
            response = requests.get(url, headers=headers, params=params)
        
        response.raise_for_status()
        features = response.json().get("audio_features", [])
        results.extend([f for f in features if f is not None])
        
        time.sleep(0.1)
    
    return results

def get_artist_info(artist_ids: list, token: str) -> list:
    """Busca géneros e popularidade de artistas."""
    url = "https://api.spotify.com/v1/artists"
    headers = {"Authorization": f"Bearer {token}"}
    
    results = []
    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i:i+50]
        params = {"ids": ",".join(batch)}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            time.sleep(retry_after)
            response = requests.get(url, headers=headers, params=params)
        
        response.raise_for_status()
        artists = response.json().get("artists", [])
        results.extend([a for a in artists if a is not None])
        
        time.sleep(0.1)
    
    return results

def save_raw(data: list, filename: str, output_path: str = "data/raw/spotify_api/"):
    """Guarda os dados brutos em JSON sem transformações."""
    Path(output_path).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_path) / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f"Saved {len(data)} records to {filepath}")