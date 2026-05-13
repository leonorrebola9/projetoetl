from extract.spotify_extractor import get_artists_from_csv, search_tracks, save_raw

artists = get_artists_from_csv("data/01.csv")
print(f"Artistas únicos encontrados: {len(artists)}")

tracks = search_tracks(artists, limit=10)
save_raw(tracks, "tracks_batch_001.csv")
print(f"Tracks guardadas: {len(tracks)}")