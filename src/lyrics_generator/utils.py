import logging
import numpy as np
from dotenv import dotenv_values


class Logger:
    def __init__(self, log_level=logging.INFO):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        self._logger.addHandler(handler)

    @property
    def info(self):
        return self._logger.info

    @property
    def error(self):
        return self._logger.error

    @property
    def debug(self):
        return self._logger.debug


env_config = dotenv_values()
is_debug = env_config.get("DEBUG", "").lower() in ("true", "1")
log = Logger(log_level=logging.DEBUG if is_debug else logging.INFO)


def extract_words(text: str):
    words = [w for w in text.split(" ") if w.strip() != "" or w == "\n"]
    return words


def sample(preds, temperature: float):
    """helper function to sample an index from a probability array"""

    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)

    return np.argmax(probas)


# TODO: generalize filename inputs
def get_keras_filepath(
    input_dim: int, min_valid_sequence: int, min_frequency: int
) -> str:
    ret = (
        "./checkpoints/LSTM_LYintRICS-epoch{epoch:03d}-words%d-sequence%d-minfreq%d-"
        "loss{loss:.4f}-acc{acc:.4f}-val_loss{val_loss:.4f}-val_acc{val_acc:.4f}"
        % (input_dim, min_valid_sequence, min_frequency)
    )
    ret += ".keras"
    return ret
