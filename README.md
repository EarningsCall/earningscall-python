# EarningsCall Python Library

The EarningsCall Python library provides convenient access to the EarningsCall API from
applications written in the Python language. It includes a pre-defined set of
classes for API resources that initialize themselves dynamically from API
responses.

# Installation

You don't need this source code unless you want to modify the package. If you just want to use the package, just run:

```sh
pip install --upgrade earningscall
```

# Requirements

* Python 3.7+ (PyPI supported)


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
    transcript = company.get_transcript(event)  # Fetch the earnings call transcript for this event
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
