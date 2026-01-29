from lyrics_generator import generate_lyrics

from . import SETTINGS_DIR, STANDARD_TEST


def test_core():
    settings_file = SETTINGS_DIR / "test_settings.json"
    output_type = "print"
    generate_lyrics(
        lyrics_path=STANDARD_TEST, settings_path=settings_file, output_type=output_type
    )
