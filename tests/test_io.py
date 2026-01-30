import json
from pathlib import Path
from lyrics_generator.user_input import UserInput
from lyrics_generator.schemas import OutputType, Settings
from lyrics_generator.user_output import OutputBuilder, OutputManager
from tests.utils import _get_txt_lyrics_input
from . import STANDARD_TEST, STANDARD_SETTINGS


def test_path_input():
    lyrics_path = STANDARD_TEST
    settings_path = STANDARD_SETTINGS
    output_type = "save_txt"

    _test_input(lyrics_path, settings_path, output_type)


def test_str_input():
    lyrics_path = "../examples/into_glory_ride.txt"
    settings_path = "tests/settings/test_settings.json"
    output_type = "save_txt"

    _test_input(lyrics_path, settings_path, output_type)


def test_output():
    identifier = "test"
    output_type = "save_txt"

    output_builder = OutputBuilder()
    output_manager = output_builder.build_output(OutputType[output_type], identifier)

    lyrics = _get_txt_lyrics_input(STANDARD_TEST)
    with open(STANDARD_SETTINGS) as f:
        settings = Settings(**json.load(f))

    output_manager.manage_metadata(lyrics, settings)


def _test_input(lyrics_path, settings_path, output_type):

    user_input = UserInput(
        **{
            "inputs": {"lyrics_path": lyrics_path, "settings_path": settings_path},
            "output_type": output_type,
        }
    )
    assert isinstance(user_input.lyrics_path, Path)
    print(user_input.lyrics_path.name)

    settings = user_input.get_settings()
    assert isinstance(settings, Settings)
    assert settings.patience == 20

    assert isinstance(user_input.output_type, OutputType)
