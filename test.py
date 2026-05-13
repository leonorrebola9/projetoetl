import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

print("CLIENT ID:", os.getenv("SPOTIFY_CLIENT_ID"))
print("CLIENT SECRET:", os.getenv("SPOTIFY_CLIENT_SECRET"))

auth_manager = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
)

sp = spotipy.Spotify(
    auth_manager=auth_manager,
    requests_timeout=5
)

print("ANTES DA PESQUISA")

result = sp.search(
    q="drake",
    type="artist",
    limit=1
)

print("DEPOIS DA PESQUISA")

print(result)