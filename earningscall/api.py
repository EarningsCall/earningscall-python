import logging
import os
from typing import Optional

import requests

import earningscall

log = logging.getLogger(__file__)

DOMAIN = os.environ.get("ECALL_DOMAIN", "earningscall.biz")
API_BASE = f"https://v2.api.{DOMAIN}"


def get_api_key():
    api_key = earningscall.api_key
    if not api_key:
        return os.environ.get("ECALL_API_KEY", "demo")
    return api_key


def api_key_param():
    return {"apikey": get_api_key()}


def is_demo_account():
    return get_api_key() == "demo"


def get_events(exchange: str,
               symbol: str):

    log.debug(f"get_events exchange: {exchange} symbol: {symbol}")
    params = {
        **api_key_param(),
        "exchange": exchange,
        "symbol": symbol,
    }
    response = requests.get(f"{API_BASE}/events", params=params)
    if response.status_code != 200:
        return None
    return response.json()


def get_transcript(exchange: str,
                   symbol: str,
                   year: int,
                   quarter: int) -> Optional[str]:

    log.debug(f"get_transcript year: {year} quarter: {quarter}")
    params = {
        **api_key_param(),
        "exchange": exchange,
        "symbol": symbol,
        "year": str(year),
        "quarter": str(quarter),
    }
    response = requests.get(f"{API_BASE}/transcript", params=params)
    if response.status_code != 200:
        return None
    return response.json()


def get_symbols_v1():
    response = requests.get(f"{API_BASE}/symbols.txt")
    if response.status_code != 200:
        return None
    return response.text


def get_symbols_v2():
    response = requests.get(f"{API_BASE}/symbols-v2.txt", params=api_key_param())
    if response.status_code != 200:
        return None
    return response.text


def get_sp500_companies_txt_file():
    response = requests.get(f"{API_BASE}/symbols/sp500.txt", params=api_key_param())
    if response.status_code != 200:
        return None
    return response.text
