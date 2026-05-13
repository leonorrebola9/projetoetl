from dotenv import load_dotenv
import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

# carregar variáveis
load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# autenticação
auth_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

sp = spotipy.Spotify(auth_manager=auth_manager)

artists = [
    "Drake",
    "The Weeknd",
    "Kendrick Lamar",
    "Taylor Swift",
    "Bad Bunny"
]

tracks = []

for artist_name in artists:

    results = sp.search(
        q=artist_name,
        type="track",
        limit=10
    )

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

# dataframe
df = pd.DataFrame(tracks)

# remover duplicados
df = df.drop_duplicates(subset=["track_id"])

# criar pasta
os.makedirs("data/raw", exist_ok=True)

# guardar
df.to_csv("data/raw/tracks.csv", index=False)

print(df.head())
