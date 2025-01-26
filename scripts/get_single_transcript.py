import earningscall  # noqa: F401

from earningscall import get_company


# TODO: Set your API key here:
# earningscall.api_key = "YOUR API KEY HERE"

company = get_company("AAPL")

transcript = company.get_transcript(year=2021, quarter=3, level=2)

speaker = transcript.speakers[1]
speaker_label = speaker.speaker_info.name
text = speaker.text
print("Speaker:")
print(f"  Name: {speaker.speaker_info.name}")
print(f"  Title: {speaker.speaker_info.title}")
print()
print(f"Text: {text}")
