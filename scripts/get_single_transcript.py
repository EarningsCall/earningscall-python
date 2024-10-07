import earningscall  # noqa: F401

from earningscall import get_company


# TODO: Set your API key here:
# earningscall.api_key = "YOUR SECRET API KEY GOES HERE"


company = get_company("aapl")

transcript = company.get_transcript(year=2021, quarter=3, level=4)
print(f"{company} Q3 2021 Transcript Text: \"{transcript.text[:100]}...\"")
