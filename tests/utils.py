from pathlib import Path

from lyrics_generator.lyrics_reader import LyricsReaderBuilder
from lyrics_generator.schemas import Lyrics


def _get_txt_lyrics_input(path_to_test_input: Path) -> Lyrics:
    lyrics_builder = LyricsReaderBuilder()
    txt_lyrics = lyrics_builder.build_lyrics_reader(path_to_test_input)

    ret = txt_lyrics.get_lyrics()
    return ret
