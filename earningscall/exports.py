import datetime
from datetime import date, timedelta
from typing import List, Optional, Iterator

import requests

from earningscall import api
from earningscall.api import get_sp500_companies_txt_file, is_demo_account
from earningscall.calendar import CalendarEvent
from earningscall.company import Company
from earningscall.errors import InsufficientApiAccessError
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


def get_calendar(input_date: date) -> List[CalendarEvent]:
    """
    Get the earnings event calendar for a given input date.

    :param date input_date: The date to get the calendar for.

    :return: A list of CalendarEvent objects.
    """
    if not input_date:
        raise ValueError("Date is required")
    if isinstance(input_date, datetime.datetime):
        input_date = input_date.date()
    if not isinstance(input_date, date):
        raise ValueError("Date must be a date object")
    if input_date < date(2018, 1, 1):
        raise ValueError("input_date must be greater than or equal to 2018-01-01")
    # Check if input_date is greater than 30 days from today
    if input_date > datetime.datetime.now().date() + timedelta(days=30):
        raise ValueError("input_date must be less than 30 days from today")
    if is_demo_account() and input_date != date(2025, 1, 10):
        raise InsufficientApiAccessError(
            f"\"{input_date}\" requires an API Key for access.  To get your API Key,"
            f" see: https://earningscall.biz/api-pricing"
        )
    try:
        json_data = api.get_calendar_api_operation(input_date.year, input_date.month, input_date.day)
        return [CalendarEvent.from_dict(event) for event in json_data]  # type: ignore
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            # Calendar Date not found, simply return an empty list
            return []
        raise error
