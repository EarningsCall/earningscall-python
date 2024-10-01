import logging
import os
from typing import Optional

import requests
from requests_cache import CachedSession

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


def cache_session() -> CachedSession:
    return CachedSession(
        ".earningscall_cache",
        backend="sqlite",
        cache_control=True,
        use_temp=True,
        ignored_parameters=[],
    )


def cached_urls():
    return cache_session().cache.urls()


def purge_cache():
    return cache_session().cache.clear()


def do_get(
    path: str,
    use_cache: bool = False,
    **kwargs,
):
    """
    Do a GET request to the API.

    Args:
        path (str): The path to request.
        use_cache (bool): Whether to use the cache.
        **kwargs: Additional arguments to pass to the request.

    Returns:
        requests.Response: The response from the API.
    """
    params = {
        **api_key_param(),
        **kwargs.get("params", {}),
    }
    url = f"{API_BASE}/{path}"
    log.debug(f"do_get url: {url} params: {params}")
    if use_cache and earningscall.enable_requests_cache:
        return cache_session().get(url, params=params)
    else:
        return requests.get(url, params=params)


def get_events(exchange: str, symbol: str):
    log.debug(f"get_events exchange: {exchange} symbol: {symbol}")
    params = {
        **api_key_param(),
        "exchange": exchange,
        "symbol": symbol,
    }
    response = do_get("events", params=params)
    if response.status_code != 200:
        return None
    return response.json()


def get_transcript(
    exchange: str,
    symbol: str,
    year: int,
    quarter: int,
    level: Optional[int] = None,
) -> Optional[str]:
    """
    Get the transcript for a given exchange, symbol, year, and quarter.

    Args:
        exchange (str): The exchange to get the transcript for.
        symbol (str): The symbol to get the transcript for.
        year (int): The year to get the transcript for.
        quarter (int): The quarter to get the transcript for.

    Returns:
        Optional[str]: The transcript for the given exchange, symbol, year, and quarter.
    """
    log.debug(f"get_transcript year: {year} quarter: {quarter}")
    params = {
        **api_key_param(),
        "exchange": exchange,
        "symbol": symbol,
        "year": str(year),
        "quarter": str(quarter),
        "level": str(level or 1),
    }
    response = do_get("transcript", params=params)
    if response.status_code != 200:
        return None
    return response.json()


def get_symbols_v2():
    log.debug("get_symbols_v2")
    response = do_get("symbols-v2.txt", use_cache=True)
    if response.status_code != 200:
        return None
    return response.text


def get_sp500_companies_txt_file():
    log.debug("get_sp500_companies_txt_file")
    response = do_get("symbols/sp500.txt", use_cache=True)
    if response.status_code != 200:
        return None
    return response.text


def download_audio_file(
    exchange: str,
    symbol: str,
    year: int,
    quarter: int,
) -> Optional[str]:
    """
    Get the audio for a given exchange, symbol, year, and quarter.

    Args:
        exchange (str): The exchange to get the audio for.
        symbol (str): The symbol to get the audio for.
        year (int): The year to get the audio for.
        quarter (int): The quarter to get the audio for.
    """
    params = {
        **api_key_param(),
        "exchange": exchange,
        "symbol": symbol,
        "year": str(year),
        "quarter": str(quarter),
    }
    local_filename = f"{exchange}_{symbol}_{year}_{quarter}.mp3"
    with do_get("audio", params=params, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename
