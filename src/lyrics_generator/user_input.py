import json
from pathlib import Path
from pydantic import BaseModel, Field

from lyrics_generator.schemas import OutputType, Settings


class StrInputs(BaseModel):
    lyrics_path_: str = Field(alias="lyrics_path")
    settings_path_: str = Field(alias="settings_path")

    @property
    def lyrics_path(self):
        return Path(self.lyrics_path_)

    @property
    def settings_path(self):
        return Path(self.settings_path_)


class PathInputs(BaseModel):
    lyrics_path: Path
    settings_path: Path


class UserInput(BaseModel):
    inputs: StrInputs | PathInputs
    output_type: OutputType

    @property
    def lyrics_path(self) -> Path:
        return self.inputs.lyrics_path

    @property
    def identifier(self) -> str:
        return self.lyrics_path.stem

    def get_settings(self) -> Settings:
        with open(self.inputs.settings_path) as f:
            settings = Settings(**json.load(f))
            return settings
