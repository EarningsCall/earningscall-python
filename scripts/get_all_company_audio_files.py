from earningscall import get_company


company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

print(f"Downloading all audio files for: {company}..")

for event in company.events():
    print(f"* Q{event.quarter} {event.year}")
    audio_file = company.download_audio_file(event=event)
    if audio_file:
        print(f" Downloaded audio file: \"{audio_file}\"")
    else:
        print("  No audio file found.")
