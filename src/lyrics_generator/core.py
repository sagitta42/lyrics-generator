import json
from pathlib import Path


from .lyrics_data import LyricsData
from .lyric_generator import LyricGenerator
from .model import ModelBuilder
from .output import OutputBuilder
from .schemas import Settings
from .song_lyrics import SongLyricsBuilder
from .utils import get_keras_filepath


# TODO: more step-by-step methods
def generate_lyrics(
    lyrics_path: str | Path, settings_path: str | Path, output_type: str
):
    # TODO: improve and validate
    if isinstance(lyrics_path, str):
        lyrics_path = Path(lyrics_path)
    if isinstance(settings_path, str):
        settings_path = Path(settings_path)

    with open(settings_path) as f:
        settings = Settings(**json.load(f))

    lyrics_builder = SongLyricsBuilder()
    song_lyrics = lyrics_builder.build_song_lyrics(lyrics_path)
    lyrics_input = song_lyrics.get_input()

    output_builder = OutputBuilder()
    output_manager = output_builder.build_output(output_type, lyrics_path.stem)

    data_lyrics = LyricsData(lyrics_input)
    data_lyrics.set_min_valid_sequence(settings.min_valid_sequence)
    data_lyrics.get_statistics(
        min_common_word_frequency=settings.min_common_word_frequency,
    )

    model_builder = ModelBuilder()
    lyrics_model = model_builder.build_model(input_dim=data_lyrics.num_common_words)
    lyrics_model.compile_model(
        loss=settings.loss, optimizer=settings.optimizer, metrics=settings.metrics
    )
    file_path = get_keras_filepath(
        data_lyrics.num_common_words,
        settings.min_valid_sequence,
        settings.min_common_word_frequency,
    )
    lyrics_model.set_checkpoint(file_path, settings.monitor)
    lyrics_model.set_early_stopping(settings.monitor, settings.patience)

    lyric_generator = LyricGenerator(lyrics_data=data_lyrics, model=lyrics_model)
    lyric_generator.set_text_length(settings.text_length)
    lyric_generator.set_diversities(settings.diversities)

    lyrics_model.set_print_callback(lyric_generator.generate_epoch_result)
    lyrics_model.get_training_data(
        data_lyrics.valid_sequences,
        data_lyrics.sequence_end_words,
        test_size=settings.test_size,
        random_state=settings.random_state,
    )
    lyrics_model.train(data_lyrics, settings.batch_size, settings.num_epochs)

    output_manager.produce_output(lyric_generator.results)
