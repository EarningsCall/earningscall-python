from earningscall import get_company


company = get_company("msft")

transcript = company.get_transcript(year=2021, quarter=3)
print(f"{company} Q3 2021 Transcript Text: \"{transcript.text[:100]}...\"")
