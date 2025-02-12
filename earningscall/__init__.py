from typing import Dict, Optional, Union

from earningscall.exports import get_company, get_all_companies, get_sp500_companies, get_calendar
from earningscall.symbols import Symbols, load_symbols

api_key: Optional[str] = None
enable_requests_cache: bool = True
retry_strategy: Optional[Dict[str, Union[str, int, float]]] = None

__all__ = [
    "get_company",
    "get_all_companies",
    "get_sp500_companies",
    "Symbols",
    "load_symbols",
    "get_calendar",
]
