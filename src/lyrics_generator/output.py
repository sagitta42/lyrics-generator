from abc import abstractmethod
import enum
import os
from pathlib import Path
import pandas as pd

from .logger import log


class OutputManager:
    @abstractmethod
    # TODO: improve (validation/format) (seed/epoch/...)
    def produce_output(self, df: pd.DataFrame):
        pass


class FileOutput(OutputManager):
    def __init__(self, output_folder: Path = Path("results")) -> None:
        self._output_folder = output_folder

        if not os.path.exists(self._output_folder):
            os.makedirs(self._output_folder)

        # TODO: customize
        self._filename = self._output_folder / "result"


class CsvOutput(FileOutput):
    """
    Save out put as a CSV table with epoch, seed, diversity, and result
    """

    def produce_output(self, df: pd.DataFrame):
        df.to_csv(f"{self._filename}.csv", sep="\t", header=True, index=False)


class TxtOutput(FileOutput):
    # TODO: all epochs in the same file
    def produce_output(self, df: pd.DataFrame):
        pass


class SeparateEpochTxtOutput(TxtOutput):
    # TODO: each epoch in a separate file
    def produce_output(self, df: pd.DataFrame):
        pass


class PrintOutput(OutputManager):
    def produce_output(self, df: pd.DataFrame):
        df_output = df.copy()
        df_output = df_output.reset_index()
        df_output["diversity_result"] = (
            "Diversity "
            + df_output["diversity"].astype(str)
            + "->\n"
            + df_output["text"].astype(str)
            + "\n"
        )

        for epoch in df_output["epoch"].unique():
            df_epoch = df_output[df_output["epoch"] == epoch]

            seed = df_epoch["seed"].unique()[0]
            header = []
            header.append("=" * 10)
            header.append(f"@ Epoch {int(epoch)} - Seed: {seed}")
            header.append("-" * 10)
            log.info("\n".join(header))
            log.info("\n".join(df_epoch["diversity_result"]))


class OutputType(str, enum.Enum):
    print = "print"
    save_txt = "save_txt"
    save_csv = "save_csv"
    save_txt_separate = "save_txt_separate"


class ResultOutput(enum.Enum):
    print = PrintOutput
    save_txt = TxtOutput
    save_csv = CsvOutput


class OutputBuilder:
    def build_output(self, output_type: str, *args) -> OutputManager:
        output_type = OutputType[output_type]
        output_class = ResultOutput[output_type].value
        return output_class(*args)
