from extract.spotify_extractor import get_artists_from_csv, search_tracks, save_raw

artists = get_artists_from_csv("data/final_limpo.csv")
artists = artists[:5]
print(f"Artistas encontrados: {len(artists)}")

tracks = search_tracks(artists)
save_raw(tracks, "tracks_batch_001.csv")
print(f"Tracks guardadas: {len(tracks)}")