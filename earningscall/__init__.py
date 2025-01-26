from typing import Optional

from earningscall.exports import get_company, get_all_companies, get_sp500_companies
from earningscall.symbols import Symbols, load_symbols

api_key: Optional[str] = None
enable_requests_cache: bool = True
retry_strategy = {
    "strategy": "exponential",
    "base_delay": 3,
    "max_attempts": 5,
}

__all__ = ["get_company", "get_all_companies", "get_sp500_companies", "Symbols", "load_symbols"]
