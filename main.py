import sys

from src.lyrics_generator import generate_lyrics

lyrics_path = sys.argv[1]
settings_path = sys.argv[2]

generate_lyrics(
    lyrics_path=lyrics_path, settings_path=settings_path, output_type="save_txt"
)
