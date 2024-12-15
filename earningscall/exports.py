from typing import Optional, Iterator

from earningscall.api import get_sp500_companies_txt_file
from earningscall.company import Company
from earningscall.symbols import get_symbols


def get_company(symbol: str, exchange: Optional[str] = None) -> Optional[Company]:
    """
    Get a company by symbol and optionally an exchange.

    :param str symbol: The symbol to get the company for.
    :param Optional[str] exchange: The exchange to get the company for.

    :return: The company for the given symbol and exchange.
    """
    company_info = get_symbols().lookup_company(symbol=symbol, exchange=exchange)
    if company_info:
        return Company(company_info=company_info)
    return None


def get_all_companies() -> Iterator[Company]:
    """
    Get all companies.

    :return: An iterator of all companies that is available to the current API plan.
    """
    for company_info in get_symbols().get_all():
        yield Company(company_info=company_info)


def get_sp500_companies() -> Iterator[Company]:
    """
    Get all S&P 500 companies.

    :return: An iterator of all S&P 500 companies that is available to the current API plan.
    """
    resp = get_sp500_companies_txt_file()
    if not resp:
        return
    for ticker_symbol in resp.split("\n"):
        company_info = get_symbols().lookup_company(ticker_symbol)
        if company_info:
            yield Company(company_info=company_info)
