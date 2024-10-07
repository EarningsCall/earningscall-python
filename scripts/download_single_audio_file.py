import argparse
import os

import earningscall  # noqa: F401
from earningscall import get_company
from earningscall.utils import configure_sane_logging

# TODO: Set your API key here:
# earningscall.api_key = "YOUR SECRET API KEY GOES HERE"


parser = argparse.ArgumentParser(description='')
parser.add_argument('--debug', action='store_true', help='Enable debug logs')
parser.add_argument('--sp-500', action='store_true', help='Show S&P500 Companies')

args = parser.parse_args()
configure_sane_logging()


directory = "audio_files"
os.makedirs(directory, exist_ok=True)


file_name = os.path.join(
    directory,
    "NASDAQ_META_2024_Q3.mp3",
)
company = get_company("meta")  # Lookup Meta, Inc by its ticker symbol, "META"
company.download_audio_file(year=2024, quarter=3, file_name=file_name)
