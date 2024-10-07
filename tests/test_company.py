import json

import pytest

from earningscall.company import Company
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
