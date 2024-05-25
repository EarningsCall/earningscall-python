from earningscall import get_company


company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

print(f"Getting all transcripts for: {company}..")

for event in company.events():
    print(f"* Q{event.quarter} {event.year}")
    transcript = company.get_transcript(event=event)
    if transcript:
        print(f"  Transcript Text: \"{transcript.text[:100]}...\"")
    else:
        print(f"  No transcript found.")
