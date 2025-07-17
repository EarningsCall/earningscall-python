import os

import pytest
import responses
from requests import HTTPError

import earningscall
from earningscall import get_company
from earningscall.api import purge_cache
from earningscall.company import Company
from earningscall.errors import InsufficientApiAccessError
from earningscall.event import EarningsEvent
from earningscall.symbols import CompanyInfo, clear_symbols
from earningscall.utils import data_path


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    earningscall.api_key = None
    earningscall.retry_strategy = {
        "strategy": "exponential",
        "base_delay": 0.001,
        "max_attempts": 3,
    }
    purge_cache()
    clear_symbols()
    yield  # this is where the testing happens
    # Teardown : fill with any logic you want
    earningscall.api_key = None


@responses.activate
def test_download_slide_deck():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-q1-2022-slide-deck-short-clip.yaml"))
    responses._add_from_file(file_path=data_path("msft-company-events.yaml"))
    ##
    company = get_company("msft")
    file_name = company.download_slide_deck(year=2022, quarter=1)
    #
    assert os.path.exists(file_name)
    assert os.path.getsize(file_name) > 0
    # Check that it's a PDF file (starts with %PDF)
    with open(file_name, 'rb') as f:
        assert f.read(4) == b'%PDF'
    os.unlink(file_name)


@responses.activate
def test_download_slide_deck_event():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-q1-2022-slide-deck-short-clip.yaml"))
    responses._add_from_file(file_path=data_path("msft-company-events.yaml"))
    ##
    company = get_company("msft")
    file_name = company.download_slide_deck(event=EarningsEvent(year=2022, quarter=1))
    #
    assert os.path.exists(file_name)
    assert os.path.getsize(file_name) > 0
    # Check that it's a PDF file (starts with %PDF)
    with open(file_name, 'rb') as f:
        assert f.read(4) == b'%PDF'
    os.unlink(file_name)


@responses.activate
def test_download_slide_deck_missing_params_raises_value_error():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    ##
    company = get_company("msft")
    with pytest.raises(ValueError):
        company.download_slide_deck()
    with pytest.raises(ValueError):
        company.download_slide_deck(year=2023)
    with pytest.raises(ValueError):
        company.download_slide_deck(quarter=1)
    with pytest.raises(ValueError):
        company.download_slide_deck(quarter=0)
    with pytest.raises(ValueError):
        company.download_slide_deck(year=2023, quarter=5)
    ##
    invalid_company = Company(company_info=CompanyInfo())
    slide_deck = invalid_company.download_slide_deck(year=2023, quarter=1)
    ##
    assert slide_deck is None


@responses.activate
def test_download_slide_deck_missing_from_server():
    ##
    earningscall.api_key = "foobar"  # Set to a bogus API Key.
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("meta-q3-2024-slides-not-found.yaml"))
    ##
    company = get_company("meta")
    output_file = company.download_slide_deck(year=2024, quarter=3)
    ##
    assert output_file is None


@responses.activate
def test_download_slide_deck_not_authorized():
    ##
    earningscall.api_key = "foobar"  # Set to a bogus API Key.
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("meta-q3-2024-slides-not-authorized.yaml"))
    ##
    company = get_company("meta")
    with pytest.raises(InsufficientApiAccessError):
        company.download_slide_deck(year=2024, quarter=3)


@responses.activate
def test_download_slide_deck_500_error():
    ##
    earningscall.api_key = "foobar"  # Set to a bogus API Key.
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("meta-q3-2024-slides-other-error.yaml"))
    ##
    company = get_company("meta")
    with pytest.raises(HTTPError):
        company.download_slide_deck(year=2024, quarter=3)


@responses.activate
def test_download_slide_deck_custom_filename():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-q1-2022-slide-deck-short-clip.yaml"))
    responses._add_from_file(file_path=data_path("msft-company-events.yaml"))
    ##
    company = get_company("msft")
    custom_filename = "test_custom_slides.pdf"
    file_name = company.download_slide_deck(year=2022, quarter=1, file_name=custom_filename)
    #
    assert file_name == custom_filename
    assert os.path.exists(file_name)
    assert os.path.getsize(file_name) > 0
    # Check that it's a PDF file (starts with %PDF)
    with open(file_name, 'rb') as f:
        assert f.read(4) == b'%PDF'
    os.unlink(file_name)
