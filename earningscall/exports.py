from earningscall.symbols import get_symbols

from earningscall.company import Company


def get_company(symbol: str) -> Company:
    return Company(company_info=get_symbols().lookup_company(symbol))


def get_all_companies() -> [Company]:
    for company_info in get_symbols().get_all():
        yield Company(company_info=company_info)


def get_sp500_companies() -> [Company]:
    for company_info in get_symbols().get_all():
        yield Company(company_info=company_info)
