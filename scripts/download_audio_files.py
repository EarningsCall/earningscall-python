import os
from earningscall import get_company


directory = "audio_files"
os.makedirs(directory, exist_ok=True)


def download_audio_files(company):
    print(f"Downloading all audio files for: {company}..")
    for event in company.events():
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
