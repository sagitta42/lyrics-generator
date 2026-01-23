from pydantic import BaseModel

Word = str
Sentence = list[Word]


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
    sentences_train: list[Sentence]
    sentences_test: list[Sentence]
    end_words_train: list[Word]
    end_words_test: list[Word]

    @property
    def all_sentences(self) -> list[Sentence]:
        """All sentence data"""
        ret = self.sentences_train + self.sentences_test
        return ret
