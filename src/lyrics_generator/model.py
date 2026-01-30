from keras.callbacks import LambdaCallback, ModelCheckpoint, EarlyStopping
from keras.models import Model, Sequential
from keras.layers import (
    Embedding,
    Bidirectional,
    Dense,
    Activation,
    LSTM,
)
import numpy as np
from sklearn.model_selection import train_test_split

from lyrics_generator.lyrics_data import LyricsData
from lyrics_generator.schemas import WordSequence, TrainingData, Word
from lyrics_generator.logger import log


class LyricsModel:
    def __init__(
        self,
        model: Model,
    ):
        self._model = model

        self._training_data: TrainingData = None
        self._checkpoint: ModelCheckpoint = None
        self._early_stopping: EarlyStopping = None
        self._print_callback: LambdaCallback = None

    @property
    def model(self) -> Model:
        return self._model

    @property
    def training_data(self) -> TrainingData:
        return self._training_data

    @property
    def callbacks_list(self) -> list:
        return [self._checkpoint, self._print_callback, self._early_stopping]

    def compile_model(self, loss: str, optimizer: str, metrics: list[str]):
        self.model.compile(loss=loss, optimizer=optimizer, metrics=metrics)

    def set_checkpoint(self, file_path: str, monitor: str):
        self._checkpoint = ModelCheckpoint(
            filepath=file_path, monitor=monitor, save_best_only=True
        )

    def set_early_stopping(self, monitor: str, patience: int):
        # early_stopping = EarlyStopping(monitor='val_accuracy', patience=20)
        self._early_stopping = EarlyStopping(monitor=monitor, patience=patience)

    def set_print_callback(self, on_epoch_end):
        self._print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

    def train(self, data_lyrics: LyricsData, batch_size: int, num_epochs: int):
        self._model.fit(
            data_lyrics.generator(
                self._training_data.sentences_train,
                self._training_data.end_words_train,
                batch_size,
            ),
            steps_per_epoch=int(data_lyrics.num_valid_sequences / batch_size) + 1,
            epochs=num_epochs,
            callbacks=self.callbacks_list,
            validation_data=data_lyrics.generator(
                self._training_data.sentences_test,
                self._training_data.end_words_test,
                batch_size,
            ),
            validation_steps=int(len(self._training_data.end_words_test) / batch_size)
            + 1,
        )

    def get_training_data(
        self,
        word_sequences: list[WordSequence],
        sequence_ends: list[Word],
        test_size: float,
        random_state: int,
    ) -> None:
        sequences_train, sequences_test, end_words_train, end_words_test = (
            train_test_split(
                word_sequences,
                sequence_ends,
                test_size=test_size,
                random_state=random_state,
            )
        )
        self._training_data = TrainingData(
            sentences_train=sequences_train,
            sentences_test=sequences_test,
            end_words_train=end_words_train,
            end_words_test=end_words_test,
        )


class ModelBuilder:
    def build_model(self, input_dim: int) -> LyricsModel:
        log.debug("Building model...")

        model = Sequential()
        model.add(Embedding(input_dim=input_dim, output_dim=1024))
        model.add(Bidirectional(LSTM(128)))
        model.add(Dense(input_dim))
        model.add(Activation("softmax"))

        ret = LyricsModel(model)
        return ret
