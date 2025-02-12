from datetime import datetime, date, timedelta

import pytest
import requests
import responses

import earningscall
from earningscall import get_calendar
from earningscall.api import purge_cache
from earningscall.errors import InsufficientApiAccessError
from earningscall.utils import data_path


# Uncomment and run following code to generate data/get-calendar-not-found-response.yaml file
#

# import earningscall
# @_recorder.record(file_path="data/get-calendar-not-found-response.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.earningscall.biz/calendar?apikey=demo&year=1980&month=1&day=1")


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run"""
    # Setup
    earningscall.api_key = None
    earningscall.retry_strategy = {
        "strategy": "exponential",
        "base_delay": 0.01,
        "max_attempts": 3,
    }
    purge_cache()
    yield  # this is where the testing happens
    # Teardown
    earningscall.api_key = None


@responses.activate
def test_get_calendar_invalid_inputs():
    with pytest.raises(ValueError):
        get_calendar(None)
    with pytest.raises(ValueError):
        get_calendar("2025-02-10")
    with pytest.raises(ValueError):
        get_calendar(123456)
    with pytest.raises(ValueError):
        get_calendar(date(2017, 12, 31))
    with pytest.raises(ValueError):
        get_calendar(datetime.now() + timedelta(days=31))


@responses.activate
def test_get_non_demo_date():
    with pytest.raises(InsufficientApiAccessError):
        get_calendar(date(2020, 1, 1))


@responses.activate
def test_get_calendar_success():
    earningscall.api_key = "XXXXXXXXXXX"
    responses._add_from_file(file_path=data_path("get-calendar-successful-response.yaml"))
    calendar = get_calendar(date(2025, 2, 10))
    assert len(calendar) == 20
    assert calendar[0].exchange == "NASDAQ"
    assert calendar[0].symbol == "MPAA"
    assert calendar[0].year == 2025
    assert calendar[0].quarter == 3
    assert calendar[0].conference_date.year == 2025
    assert calendar[0].conference_date.month == 2
    assert calendar[0].conference_date.day == 10
    assert calendar[0].transcript_ready
    assert calendar[0].company_name == "Motorcar Parts of America, Inc."


@responses.activate
def test_get_calendar_success_with_datetime():
    earningscall.api_key = "XXXXXXXXXXX"
    responses._add_from_file(file_path=data_path("get-calendar-successful-response.yaml"))
    calendar = get_calendar(datetime(2025, 2, 10))
    assert len(calendar) == 20
    assert calendar[0].exchange == "NASDAQ"
    assert calendar[0].symbol == "MPAA"
    assert calendar[0].year == 2025
    assert calendar[0].quarter == 3
    assert calendar[0].conference_date.year == 2025
    assert calendar[0].conference_date.month == 2
    assert calendar[0].conference_date.day == 10
    assert calendar[0].transcript_ready
    assert calendar[0].company_name == "Motorcar Parts of America, Inc."


@responses.activate
def test_get_calendar_server_error():
    earningscall.api_key = "XXXXXXXXXXX"
    responses._add_from_file(file_path=data_path("get-calendar-500-error.yaml"))
    with pytest.raises(requests.exceptions.HTTPError):
        get_calendar(date(2020, 1, 1))


@responses.activate
def test_get_calendar_not_found():
    earningscall.api_key = "XXXXXXXXXXX"
    responses._add_from_file(file_path=data_path("get-calendar-not-found-response.yaml"))
    calendar = get_calendar(date(2018, 1, 1))
    assert len(calendar) == 0
