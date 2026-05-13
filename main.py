from extract.spotify_extractor import get_access_token, get_audio_features, get_artist_info, save_raw

token = get_access_token()

# exemplo com uma lista de track IDs vindos do MPD
track_ids = ["3n3Ppam7vgaVa1iaRUIOKE", "6PCUP3dWmTjcTtXY02oFdT"]
features = get_audio_features(track_ids, token)
save_raw(features, "audio_features_batch_001.json")

artist_ids = ["06HL4z0CvFAxyc27GXpf02"]
artists = get_artist_info(artist_ids, token)
save_raw(artists, "artists_batch_001.json")