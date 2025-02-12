from datetime import datetime
import earningscall  # noqa: F401

from earningscall import get_calendar


# TODO: Set your API key here:
# earningscall.api_key = "YOUR API KEY HERE"

date = datetime(2025, 1, 10)

events = get_calendar(date)

for event in events:
    print(f"{event.company_name} - Q{event.quarter} {event.year} on: {event.conference_date.astimezone().isoformat()} Transcript Ready: {event.transcript_ready}")
