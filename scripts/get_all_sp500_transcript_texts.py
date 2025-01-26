from datetime import datetime
import os

import earningscall  # noqa: F401
from earningscall import get_sp500_companies
from earningscall.company import Company

# TODO: Set your API key here:
# earningscall.api_key = "YOUR SECRET API KEY GOES HERE"

directory = "data/transcript_texts"
os.makedirs(directory, exist_ok=True)


def download_transcript_texts(company: Company):
    print(f"Downloading all transcript texts for: {company}..")
    for event in company.events():
        if datetime.now().timestamp() < event.conference_date.timestamp():
            print(
                f"* {company.company_info.symbol} Q{event.quarter} {event.year} -- skipping, conference date in the future"
            )
            continue
        file_name = os.path.join(
            directory,
            f"{company.company_info.exchange}_{company.company_info.symbol}_{event.year}_Q{event.quarter}.text",
        )
        if os.path.exists(file_name):
            print(f"* {company.company_info.symbol} Q{event.quarter} {event.year} -- already downloaded")
        else:
            print(f"* Downloading transcript text for {company.company_info.symbol} Q{event.quarter} {event.year}...")
            transcript = company.get_transcript(event=event)
            if transcript:
                # Save transcript text to file
                with open(file_name, "w") as fd:
                    fd.write(transcript.text)
                print(
                    f" Downloaded transcript text for {company.company_info.symbol} Q{event.quarter} {event.year} to: {file_name}"
                )
            else:
                print(f" No transcript text found for {company.company_info.symbol} Q{event.quarter} {event.year}")


for company in get_sp500_companies():
    download_transcript_texts(company)
