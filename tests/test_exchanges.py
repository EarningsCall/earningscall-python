import pytest

import earningscall.api as api
import earningscall.exchanges as exchanges


@pytest.fixture(autouse=True)
def reset_exchange_cache():
    # Ensure cache doesn't leak across tests
    exchanges._exchanges_in_order = None
    yield
    exchanges._exchanges_in_order = None


def test_load_exchanges_in_order_fallback_when_payload_none(monkeypatch):
    # Given the API returns None
    monkeypatch.setattr(exchanges, "get_exchanges_json", lambda: None)

    # When we load exchanges
    result = exchanges.load_exchanges_in_order()

    # Then we fall back to the static list
    assert result == exchanges.FALLBACK_EXCHANGES_IN_ORDER


def test_load_exchanges_in_order_fallback_when_missing_key(monkeypatch):
    # Given the API returns an unexpected payload without 'exchanges'
    monkeypatch.setattr(exchanges, "get_exchanges_json", lambda: {"unexpected": []})

    # When we load exchanges
    result = exchanges.load_exchanges_in_order()

    # Then we fall back to the static list
    assert result == exchanges.FALLBACK_EXCHANGES_IN_ORDER


def test_exchange_to_index_when_none_returns_minus_one(monkeypatch):
    # Given a known order to avoid any external calls
    monkeypatch.setattr(exchanges, "get_exchanges_in_order", lambda: ["NYSE", "NASDAQ"]) 

    # When exchange is None
    assert exchanges.exchange_to_index(None) == -1


def test_exchange_to_index_when_empty_string_returns_minus_one(monkeypatch):
    # Given a known order to avoid any external calls
    monkeypatch.setattr(exchanges, "get_exchanges_in_order", lambda: ["NYSE", "NASDAQ"]) 

    # When exchange is empty
    assert exchanges.exchange_to_index("") == -1


def test_exchange_to_index_when_unknown_exchange_returns_minus_one(monkeypatch):
    # Given a known order to avoid any external calls
    monkeypatch.setattr(exchanges, "get_exchanges_in_order", lambda: ["NYSE", "NASDAQ"]) 

    # When exchange is not in the list
    assert exchanges.exchange_to_index("UNKNOWN") == -1


