from typing import Optional

from earningscall.symbols import get_symbols

from earningscall.company import Company


def get_company(symbol: str) -> Optional[Company]:
    company_info = get_symbols().lookup_company(symbol)
    if company_info:
        return Company(company_info=company_info)
    return None


def get_all_companies() -> [Company]:
    for company_info in get_symbols().get_all():
        yield Company(company_info=company_info)


def get_sp500_companies() -> [Company]:
    for company_info in get_symbols().get_all():
        yield Company(company_info=company_info)
