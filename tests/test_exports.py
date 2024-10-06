import pytest
import responses

import earningscall
from earningscall import get_all_companies, get_company, get_sp500_companies
from earningscall.api import purge_cache
from earningscall.symbols import clear_symbols
from earningscall.utils import data_path


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
def test_get_company_not_found():
    ##
    earningscall.api_key = "foobar"  # Bogus key to avoid check for "demo"
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    ##
    company = get_company("blah blah blah")
    ##
    assert company is None


@responses.activate
def test_get_all_companies():
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    ##
    companies = [company for company in get_all_companies()]
    ##
    # for company in get_all_companies():
    #     print(company)
    assert len(companies) == 5807
    assert str(companies[0]) == "Agilent Technologies, Inc."
    assert str(companies[1]) == "Alcoa Corporation"
    assert str(companies[-1]) == "Zynex, Inc."


@responses.activate
def test_get_sp_500_companies():
    responses._add_from_file(file_path=data_path("sp500-company-list.yaml"))
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    ##
    earningscall.api_key = "foobar"  # Bogus key to avoid check for "demo"
    companies = [company for company in get_sp500_companies()]
    ##
    assert len(companies) == 493
    assert str(companies[0]) == "Apple Inc."
    assert str(companies[1]) == "Microsoft Corporation"
    assert str(companies[-1]) == "News Corporation"


@responses.activate
def test_get_sp_500_companies_failed_request():
    responses._add_from_file(file_path=data_path("sp500-company-list-failed.yaml"))
    ##
    earningscall.api_key = "foobar"  # Bogus key to avoid check for "demo"
    companies = [company for company in get_sp500_companies()]
    ##
    assert len(companies) == 0
