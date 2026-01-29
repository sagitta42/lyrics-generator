# Lyrics Generator

Generate song lyrics to parody your favourite band (with love).

Procedure learned from
https://www.activestate.com/blog/how-to-build-a-lyrics-generator-with-python-recurrent-neural-networks/

## Install

Install via

```bash
pip install git+https://github.com/sagitta42/lyrics-generator.git@v0.1.0
```

to get the first working version

or

```bash
pip install git+https://github.com/sagitta42/lyrics-generator.git
```

to get latest.

Then you can use `import lyrics_generator` in the environment you installed it in.

## Example

Generate lyrics based on Into Glory Ride (1983) album by Manowar.

Download `into_glory_ride.txt` and `settings_2022.json` from `examples/`

Run

```python
from lyrics_generator import generate_lyrics

generate_lyrics(
    lyrics_path="into_glory_ride.txt",
    settings_path="settings_2022.json",
    output_type="save_txt"
)
```

Result:
Will create a folder `results/` with a file `results.txt`.
The file contains lyrics generated at end of every epoch with the diversities as specified in the settings.

Example: epoch 10 diversity 0.98

> ridin ridin ridin aint never never world 
> ride im the warlord of the road 
> know know i aint never warlord the of road 
> gloves metal metal rule tonight yea 
> a ride 
> im the warlord of the road 
> he know i aint children leather from


## How to prepare input

Following the [Dark Lyrics](http://www.darklyrics.com/lyrics/manowar/intogloryride.html) format, create a `.txt` file copy-pasting the album lyrics:

```
N. Song title

Lyrics
lyrics lyrics lyrics

M. Song title

Lyrics
More lyrics
```

The format has to be `N. Song title` to correctly parse songs.
The amount of spaces between song titles and lyrics is not important.

## Settings

Check out the settings under `examples/` to make your own following the template.

More detailed explanation of the meanings of the parameters will be updated.
