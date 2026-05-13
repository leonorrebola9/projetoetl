from extract.spotify_extractor import get_artists_from_csv, search_tracks, save_raw

artists = get_artists_from_csv("data/final_limpo.csv")

# TESTE
artists = artists[:100]
tracks = search_tracks(artists)

save_raw(tracks, "tracks_final.csv")
print(f"Total tracks: {len(tracks)}")