# EarningsCall Python Library

[![pypi](https://img.shields.io/pypi/v/earningscall.svg)](https://pypi.org/project/earningscall/)
[![Build Status](https://github.com/EarningsCall/earningscall-python/actions/workflows/release.yml/badge.svg?branch=master)](https://github.com/EarningsCall/earningscall-python/actions?query=branch%3Amaster)
[![Coverage Status](https://coveralls.io/repos/github/EarningsCall/earningscall-python/badge.svg?branch=master)](https://coveralls.io/github/EarningsCall/earningscall-python?branch=master)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/earningscall?color=blue)](https://pypi.org/project/earningscall/)

The EarningsCall Python library provides convenient access to the [EarningsCall API](https://earningscall.biz/api-guide) from
applications written in the Python language. It includes a pre-defined set of
classes for API resources that initialize themselves dynamically from API
responses.

# Requirements

* Python 3.8+

# Installation

You don't need this source code unless you want to modify the package. If you just want to use the package, just run:

```sh
pip install --upgrade earningscall
```

## Get Transcript for a Single Quarter

```python
from earningscall import get_company

company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

transcript = company.get_transcript(year=2021, quarter=3)
print(f"{company} Q3 2021 Transcript Text: \"{transcript.text[:100]}...\"")
```

Output

```text
Apple Inc. Q3 2021 Transcript Text: "Good day, and welcome to the Apple Q3 FY 2021 Earnings Conference Call. Today's call is being record..."
```


## Get All Transcripts for a company


```python
from datetime import datetime

from earningscall import get_company

company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

print(f"Getting all transcripts for: {company}..")
# Retrieve all earnings conference call events for a company, and iterate through each one
for event in company.events():
    if datetime.now().timestamp() < event.conference_date.timestamp():
        print(f"* {company.company_info.symbol} Q{event.quarter} {event.year} -- skipping, conference date in the future")
        continue
    transcript = company.get_transcript(event=event)  # Fetch the earnings call transcript for this event
    print(f"* Q{event.quarter} {event.year}")
    if transcript:
        print(f"  Transcript Text: \"{transcript.text[:100]}...\"")
    else:
        print(f"  No transcript found.")

```

Output

```text
Getting all transcripts for: Apple Inc...
* Q4 2023
  Transcript Text: "Good day and welcome to the Apple Q4 Fiscal Year 2023 earnings conference call. Today's call is bein..."
* Q3 2023
  Transcript Text: "Good day and welcome to the Apple Q3 Fiscal Year 2023 earnings conference call. Today's call is bein..."
* Q2 2023
  Transcript Text: "At this time for opening remarks and introductions, I would like to turn the call over to Suhasini T..."
* Q1 2023

  ...
```


## Get Text by Speaker

If you want to get the text by speaker, you can do so by setting the `level` parameter to `2`.

NOTE: Level `2` data is provided in any plan that includes Enhanced Transcript Data.

```python
from earningscall import get_company

company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

transcript = company.get_transcript(year=2021, quarter=3, level=2)

first_speaker = transcript.speakers[0]
speaker_label = first_speaker.speaker
text = first_speaker.text
print(f"Speaker: {speaker_label}\nText: {text}")
```

Output

```text
Speaker: spk11
Text: Good day, and welcome to the Apple Q3 FY 2021 Earnings Conference Call. Today's call is being recorded. At this time, for opening remarks and introductions, I would like to turn the call over to Tejas Ghala, Director, Investor Relations and Corporate Finance. Please go ahead.
```


## Get Text by Speaker with Speaker Name and Title

NOTE: This is a new experimental feature.  It includes Speaker Names and Titles.

```python
from earningscall import get_company

company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

transcript = company.get_transcript(year=2021, quarter=3, level=2)

speaker = transcript.speakers[1]  # Get second speaker
speaker_label = speaker.speaker_info.name
text = speaker.text
print("Speaker:")
print(f"  Name: {speaker.speaker_info.name}")
print(f"  Title: {speaker.speaker_info.title}")
print()
print(f"Text: {text}")
```

Output

```text
Speaker:
  Name: Tejas Ghala
  Title: Director, Investor Relations and Corporate Finance

Text: Thank you. Good afternoon, and thank you for joining us. Speaking first today is Apple CEO Tim Cook, and he'll be followed by CFO Luca Maestri. After that, we'll open the call to questions from analysts. Please note that some of the information you'll hear during our discussion today will consist of forward-looking statements, including without limitation, those regarding revenue, gross margin, operating expenses, other income and expenses, taxes, capital allocation, and future business outlook, including the potential impact of COVID-19 on the company's business and results of operations. These statements involve risks and uncertainties that may cause actual results or trends to differ materially from our forecast. For more information, please refer to the risk factors discussed in Apple's most recently filed annual report on Form 10-K and the Form 8-K filed with the SEC today, along with the associated press release. Apple assumes no obligation to update any forward-looking statements or information which speak as of their respective dates. I'd like to now turn the call over to Tim for introductory remarks.
```

## Get Word-Level Timestamps

If you want to get the word-level timestamps, you can do so by setting the `level` parameter to `3`.

Each timestamp is the number of seconds since the start of the transcript.

NOTE: Level `3` data is provided in any plan that includes Enhanced Transcript Data.


```python
from earningscall import get_company

company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

transcript = company.get_transcript(year=2021, quarter=3, level=3)

first_speaker = transcript.speakers[0]
words_and_start_times = list(zip(first_speaker.words, first_speaker.start_times))
print(f"Speaker: {first_speaker.speaker}")
print(f"Words with start times: {words_and_start_times}")
```

Output

```text
Speaker: spk11
Words with start times: [('Good', 0.049), ('day,', 0.229), ('and', 0.489), ('welcome', 0.609), ('to', 0.929), ('the', 1.029), ('Apple', 1.229), ('Q3', 1.629), ('FY', 2.65), ('2021', 2.6599999999999997), ('Earnings', 3.81), ('Conference', 4.17), ('Call.', 4.55), ("Today's", 5.411), ('call', 5.811), ('is', 6.111), ('being', 6.271), ('recorded.', 6.471), ('At', 7.571), ('this', 7.671), ('time,', 7.871), ('for', 8.111), ('opening', 8.351), ('remarks', 8.631), ('and', 9.092), ('introductions,', 9.232), ('I', 9.832), ('would', 9.912), ('like', 10.052), ('to', 10.192), ('turn', 10.292), ('the', 10.492), ('call', 10.592), ('over', 10.872), ('to', 11.052), ('Tejas', 11.152), ('Ghala,', 11.532), ('Director,', 12.112), ('Investor', 12.533), ('Relations', 12.873), ('and', 13.353), ('Corporate', 13.473), ('Finance.', 13.773), ('Please', 14.413), ('go', 14.653), ('ahead.', 14.793)]
```

## Get Prepared Remarks and Q&A for a Single Quarter

If you want to get the prepared remarks and Q&A for a single quarter, you can do so by setting the `level` parameter to `4`.

NOTE: Level `4` data is provided in any plan that includes Enhanced Transcript Data.

```python
from earningscall import get_company

company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

transcript = company.get_transcript(year=2021, quarter=3, level=4)
print(f"{company} Q3 2021 Prepared Remarks: \"{transcript.prepared_remarks[:100]}...\"")
print(f"{company} Q3 2021 Q&A: \"{transcript.questions_and_answers[:100]}...\"")
```

Output

```text
Apple Inc. Q3 2021 Prepared Remarks: "Good day, and welcome to the Apple Q3 FY 2021 Earnings Conference Call. Today's call is being record..."
Apple Inc. Q3 2021 Q&A: "Our first question comes from Katie Huberty from Morgan Stanley. Please go ahead. Hello, Katie. Your..."
```

## Download Audio File

If you want to download the audio file for a single quarter, you can call the `download_audio_file` function.

```python
from earningscall import get_company

company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

print("Downloading audio file for Apple Inc. Q3 2021...")
audio_file = company.download_audio_file(year=2021, quarter=3, file_name="Apple Q3 2021.mp3")
```

## List All Companies

```python
from earningscall import get_all_companies

for company in get_all_companies():
    print(f"{company.company_info} -- {company.company_info.sector} -- {company.company_info.industry}")
```

By default, this library grants you access to only two companies, Apple Inc. and Microsoft, Inc.

To gain access to 5,000+ companies please [signup here](https://earningscall.biz/api-pricing) to get your API key.

Once you have access to your API key, you can set the API Key like this:

```python
import earningscall

earningscall.api_key = "YOUR SECRET API KEY GOES HERE"
```

Alternatively, you can pass in your API key as an environment variable:

```sh
export ECALL_API_KEY="YOUR SECRET API KEY GOES HERE"
python your-python-script.py
```

## List S&P 500 Companies

```python
from earningscall import get_sp500_companies

for company in get_sp500_companies():
    print(f"{company.company_info} -- {company.company_info.sector} -- {company.company_info.industry}")
```


## Advanced

### Disable Caching

When you call `get_company("aapl")` to retrieve a company, internally the library retrieves metadata
from the EarningsCall API.  By default, it caches this metadata on disk in order to speed up subsequent requests.

If you prefer to disable this local caching behavior, you can do so with this code:

```python
import earningscall

earningscall.enable_requests_cache = False
```
