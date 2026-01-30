from pathlib import Path
from lyrics_generator.user_input import UserInput
from lyrics_generator.schemas import OutputType, Settings
from lyrics_generator.user_output import OutputManager
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

    output_manager = OutputManager(identifier)
    print(output_manager.output_id)


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
