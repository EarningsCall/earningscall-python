import argparse
from datetime import datetime
import os

import earningscall  # noqa: F401
from earningscall import get_company
from earningscall.company import Company
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


def download_audio_files(company: Company):
    print(f"Downloading all audio files for: {company}..")
    for event in company.events():
        if datetime.now().timestamp() < event.conference_date.timestamp():
            print(
                f"* {company.company_info.symbol} Q{event.quarter} {event.year} -- skipping, conference date in the future"
            )
            continue
        file_name = os.path.join(
            directory,
            f"{company.company_info.exchange}_{company.company_info.symbol}_{event.year}_Q{event.quarter}.mp3",
        )
        if os.path.exists(file_name):
            print(f"* {company.company_info.symbol} Q{event.quarter} {event.year} -- already downloaded")
        else:
            print(f"* Downloading audio file for {company.company_info.symbol} Q{event.quarter} {event.year}...")
            audio_file = company.download_audio_file(event=event, file_name=file_name)
            if audio_file:
                print(f" Downloaded audio file: \"{audio_file}\"")
            else:
                print(f" No audio file found for {company.company_info.symbol} Q{event.quarter} {event.year}")


company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"
download_audio_files(company)
