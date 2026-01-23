from src.lyrics_generator import generate_lyrics

# lyrics_path = "examples/all_albums.csv"
lyrics_path = "examples/into_glory_ride.csv"

generate_lyrics(lyrics_path, "examples/settings_original.json")
