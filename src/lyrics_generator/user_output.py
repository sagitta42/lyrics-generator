from abc import abstractmethod
from datetime import datetime
import enum
import json
import os
from pathlib import Path
import pandas as pd

from lyrics_generator.logger import log
from lyrics_generator.schemas import Lyrics, OutputType, Settings


class OutputManager:
    def __init__(self, identifier: str) -> None:
        self._output_id: str = identifier + "_" + datetime.now().strftime("%Y%m%d%H%M")

    @abstractmethod
    def manage_output(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def manage_metadata(self, lyrics: Lyrics, settings: Settings):
        pass


class MonoOutput:
    def _get_output_lines(self, df: pd.DataFrame) -> list[str]:
        ret = []

        df_output = df.copy()
        df_output = df_output.reset_index()
        df_output["diversity_result"] = (
            "--- Diversity "
            + df_output["diversity"].astype(str)
            + "\n"
            + df_output["text"].astype(str)
            + "\n"
        )

        for epoch in df_output["epoch"].unique():
            df_epoch = df_output[df_output["epoch"] == epoch]

            seed = df_epoch["seed"].unique()[0]
            header = []
            header.append(f"===== Epoch {int(epoch)}")
            header.append(f"Seed: {seed}")
            header.append("")
            ret.append("\n".join(header))
            ret.append("\n".join(df_epoch["diversity_result"]))

        return ret


class FileOutput(OutputManager):
    def __init__(self, identifier: str, output_folder: Path = Path("results")) -> None:
        super().__init__(identifier)

        self._output_folder = output_folder

        if not os.path.exists(self._output_folder):
            os.makedirs(self._output_folder)

        self._output_basepath: Path = self._output_folder / self._output_id
        self._results_basepath: str = f"{self._output_basepath}_results"

    def manage_metadata(self, lyrics: Lyrics, settings: Settings):
        lyrics_metadata = {
            song_id: " ".join(sequence) for song_id, sequence in lyrics.items()
        }
        lyrics_metadata_path = f"{self._output_basepath}_lyrics.json"
        with open(lyrics_metadata_path, "w") as f:
            json.dump(lyrics_metadata, f, indent=4)

        settings_metadata_path = f"{self._output_basepath}_settings.json"
        with open(settings_metadata_path, "w") as f:
            json.dump(settings.model_dump(), f, indent=4)


class CsvOutput(FileOutput):
    """
    Save out put as a CSV table with epoch, seed, diversity, and result
    """

    def manage_output(self, df: pd.DataFrame):
        df.to_csv(f"{self._results_basepath}.csv", sep="\t", header=True, index=False)


class TxtOutput(MonoOutput, FileOutput):
    def manage_output(self, df: pd.DataFrame):
        lines = self._get_output_lines(df)

        with open(f"{self._results_basepath}.txt", "w") as f:
            f.writelines(lines)


class PrintOutput(MonoOutput, OutputManager):
    def manage_output(self, df: pd.DataFrame):
        lines = self._get_output_lines(df)
        for l in lines:
            log.info(l)

    def manage_metadata(self, lyrics: Lyrics, settings: Settings):
        log.info("Warning: print output does not save metadata")


class ResultOutput(enum.Enum):
    print = PrintOutput
    save_txt = TxtOutput
    save_csv = CsvOutput


class OutputBuilder:
    def build_output(
        self, output_type: OutputType, identifier: str, *args
    ) -> OutputManager:
        output_class = ResultOutput[output_type].value
        return output_class(identifier, *args)
