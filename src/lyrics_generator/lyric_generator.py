import numpy as np
import pandas as pd

from lyrics_generator.logger import log
from lyrics_generator.lyrics_data import LyricsData
from lyrics_generator.model import LyricsModel
from lyrics_generator.schemas import WordSequence
from lyrics_generator.utils import sample


class LyricGenerator:
    def __init__(self, lyrics_data: LyricsData, model: LyricsModel):
        self._lyrics_data = lyrics_data
        self._model = model

        self._text_length: int = None
        self._diversities: list[float] = None
        self._results = pd.DataFrame({"epoch": [], "diversity": []})
        self._results = self._results.set_index(["epoch", "diversity"])

    @property
    def results(self) -> pd.DataFrame:
        return self._results

    def set_text_length(self, value: int):
        self._text_length = value

    def set_diversities(self, div: list[float]):
        self._diversities = div

    def generate_epoch_result(self, epoch, logs):
        """Function invoked at end of each epoch. Prints generated text."""
        log.info("Generating lyrics at epoch end...")
        seed_index = np.random.randint(len(self._model.training_data.all_sentences))
        seed_sentence = (self._model.training_data.all_sentences)[seed_index]

        for d in self._diversities:
            text = self._generate_text(seed_sentence, d)
            self._results.at[(epoch, d), "seed"] = self._get_string_sentence(
                seed_sentence
            )
            self._results.at[(epoch, d), "text"] = self._get_string_sentence(text)

    def _generate_text(
        self,
        seed_sentence: WordSequence,
        diversity: float,
    ) -> WordSequence:
        text: WordSequence = []
        sentence = seed_sentence
        for i in range(self._text_length):
            predicted_indices = np.zeros((1, self._lyrics_data.min_valid_sequence))

            for t, word in enumerate(sentence):
                predicted_indices[0, t] = self._lyrics_data.get_word_index(word)

            predictions = self._model.model.predict(predicted_indices, verbose=0)[0]
            next_index = sample(predictions, diversity)
            next_word = self._lyrics_data.get_word(next_index)
            text.append(next_word)

            sentence = sentence[1:] + [next_word]
        return text

    def _get_string_sentence(self, sentence: WordSequence) -> str:
        return " ".join(sentence)
