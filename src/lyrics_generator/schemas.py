from pydantic import BaseModel

# TODO: improve to validate pydantic models
# instead of dict use list of pydantic model with ID and word sequence
Text = str
Word = str
WordSequence = list[Word]
SongId = str
ParsedLyrics = dict[SongId, Text]
Lyrics = dict[SongId, WordSequence]


# TODO: split into multiple categories of settings
class Settings(BaseModel):
    min_common_word_frequency: int
    min_valid_sequence: int
    batch_size: int
    diversities: list[float]
    test_size: float
    random_state: int
    text_length: int
    loss: str
    optimizer: str
    metrics: list[str]
    num_epochs: int
    monitor: str
    patience: int


class TrainingData(BaseModel):
    sentences_train: list[WordSequence]
    sentences_test: list[WordSequence]
    end_words_train: list[Word]
    end_words_test: list[Word]

    @property
    def all_sentences(self) -> list[WordSequence]:
        """All sentence data"""
        ret = self.sentences_train + self.sentences_test
        return ret
