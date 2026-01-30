from ._version import __version__

# FIXME: inconvenient, means any time lyrics_generator itself is imported
# get warnings for CUDA etc.
from .core import generate_lyrics
