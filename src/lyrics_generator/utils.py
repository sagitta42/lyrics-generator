import numpy as np
import string

from lyrics_generator.schemas import WordSequence, Text


# TODO: treat punctuaton as words when drop_punctuation is False
# add drop punctuation as input setting
# (rename to punctuation_is_word or similar)
def clean_text(text: str, drop_punctuation: bool = True) -> str:
    """
    Clean and uniformize text.

    Convert all words to lowercase.

    drop_punctuation [bool]: If true, remove punctuation (commas, periods, question marks)
    """
    translator_args = ["", ""]
    if drop_punctuation:
        translator_args.append(string.punctuation)
    translator = str.maketrans(*translator_args)
    ret = " \n ".join(
        [
            l.lower().strip().translate(translator)
            for l in text.splitlines()
            if len(l) > 0
        ]
    )
    return ret


# TODO: optionally consider punctuation words
def extract_words(text: Text) -> WordSequence:
    """
    Extract words from text.

    Newline character is considered a word (from POV of lyrics generation)
    """
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
