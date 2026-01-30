from pathlib import Path

from lyrics_generator.logger import log
from lyrics_generator.lyrics_data import LyricsData
from lyrics_generator.schemas import SongId, Lyrics
from lyrics_generator.song_lyrics import LyricsReaderBuilder

from . import STANDARD_TEST


def test_txt_lyrics():
    lyrics_input = _get_txt_lyrics_input(STANDARD_TEST)

    # TODO: improve
    assert len(lyrics_input) > 0
    assert all(isinstance(key, SongId) for key in lyrics_input.keys())

    log.debug(lyrics_input)


def test_lyrics_data():
    lyrics_input = _get_txt_lyrics_input(STANDARD_TEST)

    lyrics_data = LyricsData(lyrics_input)
    lyrics_data.set_min_valid_sequence(5)

    lyrics_data.get_statistics(min_common_word_frequency=4)


def _get_txt_lyrics_input(path_to_test_input: Path) -> Lyrics:
    lyrics_builder = LyricsReaderBuilder()
    txt_lyrics = lyrics_builder.build_lyrics_reader(path_to_test_input)

    ret = txt_lyrics.get_lyrics()
    return ret
