import importlib.metadata
import logging
import math
import os
import platform
import threading
import time
import urllib.parse
from typing import Dict, List, Optional, Union

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
DEFAULT_TELEMETRY_MAX_ENTRIES = 1000
_latency_metrics: List[dict] = []
_latency_metrics_lock = threading.Lock()


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


def _get_telemetry_max_entries() -> int:
    return max(earningscall.telemetry_max_entries, 0)


def _record_latency_metric(
    *,
    method: str,
    target: str,
    duration_ms: float,
    attempts: int,
    status_code: Optional[int] = None,
    from_cache: bool = False,
    error_type: Optional[str] = None,
) -> None:
    if not earningscall.enable_telemetry:
        return

    max_entries = _get_telemetry_max_entries()
    if max_entries == 0:
        return

    metric = {
        "timestamp": time.time(),
        "method": method,
        "target": target,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 3),
        "attempts": attempts,
        "from_cache": from_cache,
        "error_type": error_type,
    }
    with _latency_metrics_lock:
        _latency_metrics.append(metric)
        overflow = len(_latency_metrics) - max_entries
        if overflow > 0:
            del _latency_metrics[:overflow]


def get_latency_metrics() -> List[dict]:
    with _latency_metrics_lock:
        return [metric.copy() for metric in _latency_metrics]


def pop_latency_metrics() -> List[dict]:
    with _latency_metrics_lock:
        snapshot = [metric.copy() for metric in _latency_metrics]
        _latency_metrics.clear()
        return snapshot


def clear_latency_metrics() -> None:
    with _latency_metrics_lock:
        _latency_metrics.clear()


def _calculate_percentile(values: List[float], percentile: float) -> float:
    sorted_values = sorted(values)
    index = max(math.ceil(percentile * len(sorted_values)) - 1, 0)
    return sorted_values[index]


def get_latency_metrics_summary(reset: bool = False) -> List[dict]:
    metrics = pop_latency_metrics() if reset else get_latency_metrics()
    groups: Dict[tuple, dict] = {}
    for metric in metrics:
        key = (
            metric["method"],
            metric["target"],
            metric["status_code"],
            metric["error_type"],
        )
        group = groups.setdefault(
            key,
            {
                "method": metric["method"],
                "target": metric["target"],
                "status_code": metric["status_code"],
                "error_type": metric["error_type"],
                "count": 0,
                "from_cache_count": 0,
                "retry_count": 0,
                "durations_ms": [],
            },
        )
        group["count"] += 1
        group["from_cache_count"] += int(bool(metric["from_cache"]))
        group["retry_count"] += max(int(metric["attempts"]) - 1, 0)
        group["durations_ms"].append(float(metric["duration_ms"]))

    summaries: List[dict] = []
    for group in groups.values():
        durations = group["durations_ms"]
        count = group["count"]
        total_duration = sum(durations)
        summaries.append(
            {
                "method": group["method"],
                "target": group["target"],
                "status_code": group["status_code"],
                "error_type": group["error_type"],
                "count": count,
                "from_cache_count": group["from_cache_count"],
                "retry_count": group["retry_count"],
                "min_duration_ms": round(min(durations), 3),
                "max_duration_ms": round(max(durations), 3),
                "avg_duration_ms": round(total_duration / count, 3),
                "p95_duration_ms": round(_calculate_percentile(durations, 0.95), 3),
            }
        )

    return sorted(
        summaries,
        key=lambda item: (
            item["target"],
            item["method"],
            str(item["status_code"]),
            str(item["error_type"]),
        ),
    )


def get_earnings_call_version():
    try:
        return importlib.metadata.version("earningscall")
    except importlib.metadata.PackageNotFoundError:
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
        "x-client-build-version": earnings_call_version,
    }


def _get_with_optional_cache(url: str, *, params: Optional[dict] = None, stream: Optional[bool] = None):
    """
    Internal helper to GET an absolute URL, using the shared requests cache when enabled.
    """
    request_start_time = time.perf_counter()
    response: Optional[requests.Response] = None
    error_type: Optional[str] = None
    try:
        if earningscall.enable_requests_cache:
            response = cache_session().get(url, params=params, headers=get_headers(), stream=stream)
        else:
            response = requests.get(url, params=params, headers=get_headers(), stream=stream)
        return response
    except Exception as exc:
        error_type = type(exc).__name__
        raise
    finally:
        _record_latency_metric(
            method="GET",
            target=url,
            status_code=response.status_code if response is not None else None,
            duration_ms=(time.perf_counter() - request_start_time) * 1000,
            attempts=1,
            from_cache=bool(getattr(response, "from_cache", False)) if response is not None else False,
            error_type=error_type,
        )


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

    request_start_time = time.perf_counter()
    response: Optional[requests.Response] = None
    attempts = 0
    error_type: Optional[str] = None

    try:
        for attempt in range(max_attempts):
            attempts = attempt + 1
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
                    "Your API key is invalid. You can get your API key at: https://{DOMAIN}/api-key"
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
                time.sleep(float(wait_time))
    except Exception as exc:
        error_type = type(exc).__name__
        raise
    finally:
        _record_latency_metric(
            method="GET",
            target=path,
            status_code=response.status_code if response is not None else None,
            duration_ms=(time.perf_counter() - request_start_time) * 1000,
            attempts=attempts,
            from_cache=bool(getattr(response, "from_cache", False)) if response is not None else False,
            error_type=error_type,
        )

    assert response is not None  # Always set when max_attempts >= 1
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


def download_slide_deck(
    exchange: str,
    symbol: str,
    year: int,
    quarter: int,
    file_name: Optional[str] = None,
) -> Optional[str]:
    """
    Get the slide deck for a given exchange, symbol, year, and quarter.

    :param str exchange: The exchange to get the slide deck for.
    :param str symbol: The symbol to get the slide deck for.
    :param int year: The 4-digit year to get the slide deck for.
    :param int quarter: The quarter to get the slide deck for (1, 2, 3, or 4).
    :param file_name: Optionally specify the filename to save the slide deck to.
    :return: The filename of the downloaded slide deck file.
    :rtype Optional[str]: The filename of the downloaded slide deck file.
    """
    params = {
        "exchange": exchange,
        "symbol": symbol,
        "year": str(year),
        "quarter": str(quarter),
    }
    local_filename = file_name or f"{exchange}_{symbol}_{year}_{quarter}_slides.pdf"
    with do_get("slides", params=params, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def get_exchanges_json():
    """Fetch the public exchanges JSON from the website domain.

    Uses the shared cache to avoid frequent network requests.
    """
    url = f"https://{DOMAIN}/exchanges.json"
    response = _get_with_optional_cache(url)
    if response.status_code != 200:
        return None
    return response.json()
