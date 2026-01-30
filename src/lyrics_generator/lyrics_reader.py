from abc import abstractmethod
from pathlib import Path

from lyrics_generator.schemas import Lyrics, ParsedLyrics
from lyrics_generator.utils import clean_text, extract_words


class LyricsReader:
    def get_lyrics(self) -> Lyrics:
        """
        Return final lyrics input.

        Parse input.
        Clean text.
        Extract words.
        """
        parsed_input = self._parse_input()
        ret = {}
        for song_id, text in parsed_input.items():
            cleaned_text = clean_text(text)
            ret[song_id] = extract_words(cleaned_text)

        return ret

    @abstractmethod
    def _parse_input(self) -> ParsedLyrics:
        pass


class TxtLyricsReader(LyricsReader):
    def __init__(self, path_to_lyrics: Path) -> None:
        self.path_to_lyrics = path_to_lyrics

        with open(self.path_to_lyrics) as f:
            self.filelines: list[str] = f.readlines()

    # TODO: add validation output is not empty
    def _parse_input(self) -> ParsedLyrics:
        """
        Parse file lines to detect song titles and song lyrics.
        """
        song_id = None
        ret = {}
        for line in self.filelines:
            if self._is_song_title(line):
                song_id = line.rstrip()
                ret[song_id] = ""
            # TODO: generalize detect empty line (can have spaces, tabs etc.)
            elif line == "\n":
                continue
            else:
                ret[song_id] += line
        return ret

    def _is_song_title(self, line: str) -> bool:
        ret = line[0].isnumeric() and line[1] == "."
        return ret


class LyricsReaderBuilder:
    def build_lyrics_reader(self, path: str | Path) -> LyricsReader:
        path_to_lyrics = Path(path) if isinstance(path, str) else path
        if path_to_lyrics.suffix == ".txt":
            return TxtLyricsReader(path_to_lyrics)

        raise NotImplementedError(
            f"Only .txt file input is supported. Your input: {path}"
        )
