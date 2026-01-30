from abc import abstractmethod
from datetime import datetime
import enum
import os
from pathlib import Path
import pandas as pd

from lyrics_generator.logger import log
from lyrics_generator.schemas import OutputType


class OutputManager:
    def __init__(self, identifier: str) -> None:
        self._output_id = (
            identifier + "_" + datetime.now().strftime("%Y%m%d") + "_results"
        )

    @property
    def output_id(self):
        return self._output_id

    @abstractmethod
    def produce_output(self, df: pd.DataFrame):
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

        self._file_basename: Path = self._output_folder / self._output_id


class CsvOutput(FileOutput):
    """
    Save out put as a CSV table with epoch, seed, diversity, and result
    """

    def produce_output(self, df: pd.DataFrame):
        df.to_csv(f"{self._file_basename}.csv", sep="\t", header=True, index=False)


class TxtOutput(MonoOutput, FileOutput):
    def produce_output(self, df: pd.DataFrame):
        lines = self._get_output_lines(df)

        with open(f"{self._file_basename}.txt", "w") as f:
            f.writelines(lines)


class SeparateEpochTxtOutput(TxtOutput):
    # TODO: each epoch in a separate file
    def produce_output(self, df: pd.DataFrame):
        pass


class PrintOutput(MonoOutput, OutputManager):
    def produce_output(self, df: pd.DataFrame):
        lines = self._get_output_lines(df)
        for l in lines:
            log.info(l)


class ResultOutput(enum.Enum):
    print = PrintOutput
    save_txt = TxtOutput
    save_csv = CsvOutput


class OutputBuilder:
    def build_output(self, output_type: str, identifier: str, *args) -> OutputManager:
        output_type = OutputType[output_type]
        output_class = ResultOutput[output_type].value
        return output_class(identifier, *args)
