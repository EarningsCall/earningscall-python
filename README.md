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
from earningscall import get_company

company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

print(f"Getting all transcripts for: {company}..")
# Retrieve all earnings conference call events for a company, and iterate through each one
for event in company.events():
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
