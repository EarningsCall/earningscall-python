from typing import Optional, Iterator

from earningscall.api import get_sp500_companies_txt_file
from earningscall.company import Company
from earningscall.symbols import get_symbols


def get_company(symbol: str) -> Optional[Company]:
    company_info = get_symbols().lookup_company(symbol)
    if company_info:
        return Company(company_info=company_info)
    return None


def get_all_companies() -> Iterator[Company]:
    for company_info in get_symbols().get_all():
        yield Company(company_info=company_info)


def get_sp500_companies() -> Iterator[Company]:
    resp = get_sp500_companies_txt_file()
    if not resp:
        return
    for ticker_symbol in resp.split("\n"):
        company_info = get_symbols().lookup_company(ticker_symbol)
        if company_info:
            yield Company(company_info=company_info)
