import importlib
import logging
import os
import platform
import time
import urllib.parse
from importlib.metadata import PackageNotFoundError
from typing import Dict, Optional, Union

import requests
from requests_cache import CachedSession

import earningscall
from earningscall.errors import InvalidApiKeyError

log = logging.getLogger(__file__)

DOMAIN = os.environ.get("EARNINGSCALL_DOMAIN", "earningscall.biz")
API_BASE = f"https://v2.api.{DOMAIN}"
DEFAULT_RETRY_STRATEGY: Dict[str, Union[str, int, float]] = {
    "strategy": "exponential",
    "base_delay": 1,
    "max_attempts": 10,
}


def get_api_key():
    if earningscall.api_key:
        return earningscall.api_key
    e_call_key = os.environ.get("ECALL_API_KEY")
    earnings_call_key = os.environ.get("EARNINGSCALL_API_KEY")
    if e_call_key:
        return e_call_key
    if earnings_call_key:
        return earnings_call_key
    return "demo"


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


def get_earnings_call_version():
    try:
        return importlib.metadata.version("earningscall")
    except PackageNotFoundError:
        return None


def get_user_agent():
    sdk_name = "EarningsCallPython"
    sdk_version = get_earnings_call_version()
    python_version = platform.python_version()
    os_info = f"{platform.system()} {platform.release()}"
    arch = platform.machine()
    requests_version = requests.__version__
    user_agent = f"{sdk_name}/{sdk_version} (Python/{python_version}; {os_info}; {arch}) Requests/{requests_version}"
    return user_agent


def get_headers():
    earnings_call_version = get_earnings_call_version()
    return {
        "User-Agent": get_user_agent(),
        "X-EarningsCall-Version": earnings_call_version,
    }


def can_retry(response: requests.Response) -> bool:
    if response.status_code == 429:
        return True
    # Check for 5XX errors
    if response.status_code >= 500 and response.status_code < 600:
        return True
    return False


def is_success(response: requests.Response) -> bool:
    # TODO: Do we need to check for 2xx status codes?
    return response.status_code == 200


def do_get(
    path: str,
    use_cache: bool = False,
    **kwargs,
) -> requests.Response:
    """
    Do a GET request to the API with exponential backoff retry for rate limits.

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
    if log.isEnabledFor(logging.DEBUG):
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        log.debug(f"GET: {full_url}")

    retry_strategy = earningscall.retry_strategy or DEFAULT_RETRY_STRATEGY
    delay = retry_strategy["base_delay"]
    max_attempts = int(retry_strategy["max_attempts"])

    for attempt in range(max_attempts):
        if use_cache and earningscall.enable_requests_cache:
            response = cache_session().get(url, params=params)
        else:
            response = requests.get(
                url,
                params=params,
                headers=get_headers(),
                stream=kwargs.get("stream"),
            )

        if is_success(response):
            return response

        if response.status_code == 401:
            raise InvalidApiKeyError(
                "Your API key is invalid. You can get your API key at: https://earningscall.biz/api-key"
            )

        if not can_retry(response):
            return response

        if attempt < max_attempts - 1:  # Don't sleep after the last attempt
            if retry_strategy["strategy"] == "exponential":
                wait_time = delay * (2**attempt)  # Exponential backoff: 1s -> 2s -> 4s -> 8s -> 16s -> 32s -> 64s
            elif retry_strategy["strategy"] == "linear":
                wait_time = delay * (attempt + 1)  # Linear backoff: 1s -> 2s -> 3s -> 4s -> 5s -> 6s -> 7s
            else:
                raise ValueError("Invalid retry strategy. Must be one of: 'exponential', 'linear'")
            # TODO: Should we log a warning here?  Does the customer want to see this log?
            log.warning(
                f"Rate limited (429). Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_attempts})"
            )
            time.sleep(wait_time)

    return response  # Return the last response if all retries failed


def get_calendar_api_operation(year: int, month: int, day: int) -> dict:
    params = {
        "year": str(year),
        "month": str(month),
        "day": str(day),
    }
    response = do_get("calendar", params=params)
    response.raise_for_status()
    return response.json()


def get_events(exchange: str, symbol: str) -> Optional[dict]:
    params = {
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
) -> Optional[dict]:
    """
    Get the transcript for a given exchange, symbol, year, and quarter.

    :param str exchange: The exchange to get the transcript for.
    :param str symbol: The symbol to get the transcript for.
    :param int year: The year to get the transcript for.
    :param int quarter: The quarter to get the transcript for.
    :param Optional[int] level: The level to get the transcript for.

    :return: The transcript for the given exchange, symbol, year, and quarter.
    """
    params = {
        "exchange": exchange,
        "symbol": symbol,
        "year": str(year),
        "quarter": str(quarter),
        "level": str(level or 1),
    }
    response = do_get("transcript", params=params)
    response.raise_for_status()
    return response.json()


def get_symbols_v2():
    response = do_get("symbols-v2.txt", use_cache=True)
    if response.status_code != 200:
        return None
    return response.text


def get_sp500_companies_txt_file():
    response = do_get("symbols/sp500.txt", use_cache=True)
    if response.status_code != 200:
        return None
    return response.text


def download_audio_file(
    exchange: str,
    symbol: str,
    year: int,
    quarter: int,
    file_name: Optional[str] = None,
) -> Optional[str]:
    """
    Get the audio for a given exchange, symbol, year, and quarter.

    :param str exchange: The exchange to get the audio for.
    :param str symbol: The symbol to get the audio for.
    :param int year: The 4-digit year to get the audio for.
    :param int quarter: The quarter to get the audio for (1, 2, 3, or 4).
    :param file_name: Optionally specify the filename to save the audio to.
    :return: The filename of the downloaded audio file.
    :rtype Optional[str]: The filename of the downloaded audio file.
    """
    params = {
        "exchange": exchange,
        "symbol": symbol,
        "year": str(year),
        "quarter": str(quarter),
    }
    local_filename = file_name or f"{exchange}_{symbol}_{year}_{quarter}.mp3"
    with do_get("audio", params=params, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename
