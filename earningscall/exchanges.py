import logging

from earningscall.api import get_exchanges_json


log = logging.getLogger(__file__)


FALLBACK_EXCHANGES_IN_ORDER = [
    "NYSE",
    "NASDAQ",
    "AMEX",
    "TSX",
    "TSXV",
    "OTC",
    "LSE",
    "CBOE",
    "STO",
]


_exchanges_in_order = None


def load_exchanges_in_order() -> list:
    """Load exchanges from the website JSON with a safe fallback.

    Returns a list of exchange codes in order.
    """
    try:
        payload = get_exchanges_json()
        if not payload or "exchanges" not in payload:
            return FALLBACK_EXCHANGES_IN_ORDER
        codes = [item.get("code") for item in payload["exchanges"] if item.get("code")]
        return codes
    except Exception:
        return FALLBACK_EXCHANGES_IN_ORDER


def get_exchanges_in_order() -> list:
    global _exchanges_in_order
    if _exchanges_in_order is None:
        _exchanges_in_order = load_exchanges_in_order()
    return _exchanges_in_order


