from typing import Dict, Optional, Union

from earningscall.api import (
    clear_latency_metrics,
    get_latency_metrics,
    get_latency_metrics_summary,
    pop_latency_metrics,
)
from earningscall.exports import get_company, get_all_companies, get_sp500_companies, get_calendar
import earningscall.exchanges as exchanges
from earningscall.symbols import Symbols, load_symbols

api_key: Optional[str] = None
enable_requests_cache: bool = True
retry_strategy: Optional[Dict[str, Union[str, int, float]]] = None
enable_telemetry: bool = True
telemetry_max_entries: int = 1000

__all__ = [
    "get_company",
    "get_all_companies",
    "get_sp500_companies",
    "Symbols",
    "load_symbols",
    "get_calendar",
    "get_latency_metrics",
    "get_latency_metrics_summary",
    "clear_latency_metrics",
    "pop_latency_metrics",
    "exchanges",
]
