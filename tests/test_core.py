from lyrics_generator import generate_lyrics

from . import SETTINGS_DIR, STANDARD_TEST, STANDARD_SETTINGS


def test_print():
    output_type = "print"
    generate_lyrics(
        lyrics_path=STANDARD_TEST,
        settings_path=STANDARD_SETTINGS,
        output_type=output_type,
    )


def test_txt():
    output_type = "save_txt"
    generate_lyrics(
        lyrics_path=STANDARD_TEST,
        settings_path=STANDARD_SETTINGS,
        output_type=output_type,
    )
