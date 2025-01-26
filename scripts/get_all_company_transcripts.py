import earningscall  # noqa: F401
from earningscall import get_company

# earningscall.api_key = "YOUR API KEY HERE"


company = get_company("AAPL")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

print(f"Getting all transcripts for: {company}..")

for event in company.events():
    print(f"* Q{event.quarter} {event.year}")
    transcript = company.get_transcript(event=event)
    if transcript:
        print(f"  Transcript Text: \"{transcript.text[:100]}...\"")
    else:
        print("  No transcript found.")
