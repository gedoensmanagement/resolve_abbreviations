# Resolving abbreviations in 16th century Latin texts

(Tested with Python 3.8 on Linux and Windows.)

## Installation
* Create a new environment with Python 3.8 using [venv](https://docs.python-guide.org/dev/virtualenvs/) or [conda](https://docs.anaconda.com/), e.g. `conda create --name dh_blog python=3.8`.
* Activate the new environment, e.g. `conda activate dh_blog`.
* Clone this repository.
* Use pip to install the required Python packages: `pip install -r requirements.txt`.
* Download [`hunspell-la.zip`](https://latin-dict.github.io/docs/hunspell-la.zip), the Latin Hunspell dictionary by Karl Zeiler and Jean-Pierre Sutto, and unzip it to the project folder (“resolve_abbreviations”).

## Usage
* Read the documentation on https://dhlab.hypotheses.org/2154.
* Execute `python normalizer.py` and follow the command line instructions.

## Description
* `simple_regex.py` and `simple_hunspell.py`: Short examples explaining the basic approach of resolving abbreviations in 16th century Latin texts (cf. https://dhlab.hypotheses.org/2154). 
* `transkribus_web.py`: A client communicating with the Transkribus REST API (described [here](https://dhlab.hypotheses.org/2114) and [here](https://github.com/gedoensmanagement/transkribus_rest_api_client).).
* `dictionary.py`: A wrapper class providing a Latin Hunspell dictionary. 
* `cleaner.py`: Class containing all the functions necessary to resolve abbreviations, tokenize the text, and resolve hyphenations/line breaks/macrons. 
* `replacement_table.tsv`: A table defining regex patterns to search and replace abbreviations in 16th century Latin texts. (This is work in progress, thus a bit chaotic!)
* `tools.py`: The `IO_Tools` class provides functions to load a csv table from disk or from Google Sheets into a Python dictionary.
* `cli.py`: Provides `Transkribus_CLI`, a rudimentary command line interface which connects all these parts.
* `normalizer.py`: This is the main script which uses `Transkribus_CLI` to operate the whole machine.