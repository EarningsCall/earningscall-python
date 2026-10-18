import json

import pytest
import requests

from earningscall.company import Company, _plan_name
from earningscall.symbols import CompanyInfo


def test_company_constructor_checks():
    with pytest.raises(ValueError):
        Company(company_info=None)


def test_company_to_string():
    company_info = CompanyInfo(
        name="Test Company",
        symbol="TEST",
        exchange="TEST",
        sector="TEST",
        industry="TEST",
    )
    company = Company(company_info=company_info)
    assert str(company) == "Test Company"
    assert str(company.company_info) == "(TEST: TEST - Test Company)"
    assert company.company_info == company_info
    assert json.loads(company_info.to_json()) == {
        "name": "Test Company",
        "symbol": "TEST",
        "exchange": "TEST",
        "sector": "TEST",
        "industry": "TEST",
    }
    assert company_info.exchange_symbol() == "TEST_TEST"
    assert company_info.to_txt_row() == ["-1", "TEST", "Test Company"]


def _response_with_headers(headers: dict) -> requests.Response:
    response = requests.Response()
    response.headers.update(headers)
    return response


@pytest.mark.parametrize(
    "headers, expected",
    [
        ({"X-Plan-Name": "basic", "X-Plan-Type": "starter"}, "basic"),
        ({"X-Plan-Type": "starter"}, "starter"),
        ({}, "unknown"),
    ],
)
def test_plan_name(headers, expected):
    assert _plan_name(_response_with_headers(headers)) == expected


def test_plan_name_without_response():
    assert _plan_name(None) == "unknown"
