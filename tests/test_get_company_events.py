import pytest
import requests
import responses

import earningscall
from earningscall import get_company
from earningscall.api import API_BASE, purge_cache
from earningscall.symbols import clear_symbols
from earningscall.utils import data_path

# Uncomment and run following code to generate msft-transcript-response.yaml file
#
# from responses import _recorder
# @_recorder.record(file_path="msft-company-events.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.earningscall.biz/events?apikey=demo&exchange=NASDAQ&symbol=MSFT")
#


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    earningscall.api_key = None
    earningscall.retry_strategy = {
        "strategy": "exponential",
        "base_delay": 0.001,
        "max_attempts": 1,
    }
    purge_cache()
    clear_symbols()
    yield
    earningscall.api_key = None
    earningscall.retry_strategy = None


@responses.activate
def test_get_demo_company():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
    responses._add_from_file(file_path=data_path("msft-company-events.yaml"))
    ##
    company = get_company("msft")
    events = company.events()
    ##
    assert len(events) == 20
    assert events[0].year == 2024
    assert events[0].quarter == 3


@responses.activate
def test_get_company_events_returns_empty_on_404():
    earningscall.api_key = "foobar"
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses.add(responses.GET, f"{API_BASE}/events", status=404)
    ##
    company = get_company("msft")
    events = company.events()
    ##
    assert events == []


@responses.activate
def test_get_company_events_raises_on_500():
    earningscall.api_key = "foobar"
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses.add(responses.GET, f"{API_BASE}/events", status=500)
    ##
    company = get_company("msft")
    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        company.events()
