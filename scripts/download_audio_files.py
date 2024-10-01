import os
from earningscall import get_company


company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"
directory = "audio_files"
os.makedirs(directory, exist_ok=True)

print(f"Downloading all audio files for: {company}..")

for event in company.events():
    file_name = os.path.join(
        directory, f"{company.company_info.exchange}_{company.company_info.symbol}_{event.year}_{event.quarter}.mp3"
    )
    print(f"* {company.company_info.symbol} Q{event.quarter} {event.year}")
    audio_file = company.download_audio_file(event=event, file_name=file_name)
    if audio_file:
        print(f" Downloaded audio file: \"{audio_file}\"")
    else:
        print("  No audio file found.")
