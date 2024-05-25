import logging
import os
from typing import Optional

import requests


log = logging.getLogger(__file__)

DOMAIN = os.environ.get("ECALL_DOMAIN", "earningscall.biz")
API_BASE = f"https://v2.api.{DOMAIN}"


def get_events(exchange: str,
               symbol: str):

    log.debug(f"get_events exchange: {exchange} symbol: {symbol}")
    params = {
        "apikey": "demo",
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
        "apikey": "demo",
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
    response = requests.get(f"https://{DOMAIN}/symbols.txt")
    if response.status_code != 200:
        return None
    return response.text


def get_symbols_v2():
    response = requests.get(f"https://{DOMAIN}/symbols-v2.txt")
    if response.status_code != 200:
        return None
    return response.text
