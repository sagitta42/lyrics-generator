import numpy as np
import pandas as pd

from lyrics_generator.logger import log
from lyrics_generator.schemas import WordSequence, Word, Lyrics


# TODO: rename to LyricsAnalyzer
class LyricsData:
    def __init__(self, lyrics_input: Lyrics) -> None:
        self._lyrics_input = lyrics_input

        self._min_valid_sequence: int = None

        self._text_words: WordSequence = sum(self._lyrics_input.values(), [])

        self._frequencies = {}
        for w in self._text_words:
            self._frequencies[w] = self._frequencies.get(w, 0) + 1

        self._df_common_words = pd.DataFrame()
        self._uncommon_words = set()
        self._valid_sequences: list[WordSequence] = []
        self._sequence_end_words: list[Word] = []

    def set_min_valid_sequence(self, value: int):
        self._min_valid_sequence = value

    @property
    def min_valid_sequence(self) -> int:
        return self._min_valid_sequence

    @property
    def valid_sequences(self) -> list[WordSequence]:
        return self._valid_sequences

    @property
    def sequence_end_words(self) -> list[Word]:
        return self._sequence_end_words

    @property
    def num_common_words(self) -> int:
        ret = len(self._df_common_words)
        return ret

    @property
    def num_valid_sequences(self) -> int:
        ret = len(self.valid_sequences)
        return ret

    def get_statistics(self, min_common_word_frequency: int):
        self._uncommon_words = set(
            [
                key
                for key in self._frequencies.keys()
                if self._frequencies[key] < min_common_word_frequency
            ]
        )

        common_words = set(
            [w for w in self._frequencies.keys() if not w in self._uncommon_words]
        )
        self._df_common_words = pd.DataFrame({"word": sorted(common_words)})
        self._df_common_words["index"] = self._df_common_words.index

        for i in range(len(self._text_words) - self._min_valid_sequence):
            start_slice = i
            end_slice = start_slice + self._min_valid_sequence
            # TODO: why +1 here and not later
            words_slice = set(self._text_words[i : end_slice + 1])

            if len(words_slice.intersection(self._uncommon_words)) == 0:
                self._valid_sequences.append(self._text_words[start_slice:end_slice])
                self._sequence_end_words.append(self._text_words[end_slice])

        self._log_statistics()

    def generator(self, sentence_list, next_word_list, batch_size: int):
        index = 0

        while True:
            x = np.zeros((batch_size, self._min_valid_sequence), dtype=np.int32)
            y = np.zeros((batch_size), dtype=np.int32)

            for i in range(batch_size):
                for t, w in enumerate(sentence_list[index % len(sentence_list)]):
                    x[i, t] = self.get_word_index(w)

                w_next = next_word_list[index % len(sentence_list)]
                y[i] = self.get_word_index(w_next)
                index = index + 1

            yield x, y

    # TODO: DataFrame unnecesary, use dict / reversed dict
    def get_word_index(self, word: Word) -> int:
        ret = self._df_common_words.set_index("word")["index"].loc[word]
        return ret

    def get_word(self, index: int) -> Word:
        ret = self._df_common_words["word"].loc[index]
        return ret

    def _log_statistics(self):
        # TODO: tabulate
        log_info = {
            "Total words": len(self._text_words),
            "Unique words": len(self._frequencies),
            "Uncommon words": len(self._uncommon_words),
            "Valid sequences": len(self._valid_sequences),
        }
        for descr, num in log_info.items():
            log.info(f"{descr}: \t {num}")
