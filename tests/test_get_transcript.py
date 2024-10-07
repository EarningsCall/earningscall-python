import earningscall
import pytest
import responses

from earningscall import get_company
from earningscall.api import purge_cache
from earningscall.company import Company
from earningscall.errors import InsufficientApiAccessError
from earningscall.event import EarningsEvent
from earningscall.symbols import clear_symbols, CompanyInfo
from earningscall.utils import data_path


# Uncomment and run following code to generate msft-transcript-response.yaml file
#
# from responses import _recorder
# @_recorder.record(file_path="msft-transcript-response.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.earningscall.biz/transcript?apikey=demo&exchange=NASDAQ&symbol=MSFT&year=2023&quarter=1")


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    earningscall.api_key = None
    purge_cache()
    clear_symbols()
    yield  # this is where the testing happens
    # Teardown : fill with any logic you want
    earningscall.api_key = None


@responses.activate
def test_get_transcript_invalid_inputs():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
    ##
    company = get_company("msft")
    ##
    with pytest.raises(ValueError):
        company.get_transcript(year=2023)
    with pytest.raises(ValueError):
        company.get_transcript(quarter=1)
    with pytest.raises(ValueError):
        company.get_transcript(quarter=0)
    with pytest.raises(ValueError):
        company.get_transcript(year=2023, quarter=5)
    with pytest.raises(ValueError):
        company.get_transcript(year=2023, quarter=1, level=0)
    with pytest.raises(ValueError):
        company.get_transcript(year=2023, quarter=1, level=5)
    ##
    invalid_company = Company(company_info=CompanyInfo())
    transcript = invalid_company.get_transcript(year=2023, quarter=1)
    ##
    assert transcript is None

    # assert transcript.text[:100] == (
    #     'Greetings, and welcome to the Microsoft Fiscal Year 2023 First Quarter Earnings ' 'Conference Call. At '
    # )


@responses.activate
def test_get_demo_company():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
    ##
    company = get_company("msft")
    ##
    transcript = company.get_transcript(year=2023, quarter=1)
    assert transcript.text[:100] == (
        'Greetings, and welcome to the Microsoft Fiscal Year 2023 First Quarter Earnings ' 'Conference Call. At '
    )


@responses.activate
def test_get_demo_company_with_event_populated():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("demo-symbols-v2-alpha.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(event=EarningsEvent(year=2022, quarter=1))
    assert transcript.event.year == 2022
    assert transcript.event.quarter == 1
    assert transcript.event.conference_date.isoformat() == "2022-01-19T00:00:00-08:00"
    assert transcript.text[:100] == (
        "Good day and welcome to the Apple Q1 Fiscal Year 2021 earnings conference " "call. Today's call is bein"
    )


@responses.activate
def test_get_demo_company_with_advanced_transcript_data():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2022-advanced-data-level-2.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2022, quarter=1, level=2)
    assert transcript.event.year == 2022
    assert transcript.event.quarter == 1
    assert transcript.event.conference_date.isoformat() == "2022-01-27T14:00:00-08:00"
    assert transcript.text[:100] == (
        "Good day and welcome to the Apple Q1 FY 2022 earnings conference call. Today's call is being recorde"
    )
    assert transcript.speakers[0].speaker == "spk03"
    assert transcript.speakers[0].words is None
    assert transcript.speakers[0].start_times is None

# Uncomment and run following code to generate demo-symbols-v2.yaml file
#
# import requests
#
# from responses import _recorder
#
#
# @_recorder.record(file_path="demo-symbols-v2.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.earningscall.biz/symbols-v2.txt?apikey=demo")

# Uncomment and run following code to generate demo-symbols-v2.yaml file
#
import requests

from responses import _recorder


@_recorder.record(file_path="aapl-q1-2022-advanced-data-level-2.yaml")
def test_save_symbols_v1():
    requests.get("https://v2.api.earningscall.biz/transcript?apikey=demo&exchange=NASDAQ&symbol=AAPL&year=2022&quarter=q1&level=2")



@responses.activate
def test_get_non_demo_company():
    ##
    responses._add_from_file(file_path=data_path("demo-symbols-v2.yaml"))
    ##
    with pytest.raises(InsufficientApiAccessError):
        get_company("nvda")
