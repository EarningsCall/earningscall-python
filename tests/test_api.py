import importlib.metadata

import pytest
import requests
import responses

import earningscall
from earningscall.api import (
    API_BASE,
    DOMAIN,
    get_api_key,
    get_earnings_call_version,
    get_events,
    get_exchanges_json,
    get_sp500_companies_txt_file,
    get_symbols_v2,
    get_user_agent,
    purge_cache,
)


def test_get_api_key_returns_earningscall_api_key_when_set(monkeypatch):
    """Test that get_api_key returns earningscall.api_key when it's set."""
    # Given earningscall.api_key is set
    monkeypatch.setattr(earningscall, "api_key", "test-api-key")
    # And environment variables are cleared
    monkeypatch.delenv("ECALL_API_KEY", raising=False)
    monkeypatch.delenv("EARNINGSCALL_API_KEY", raising=False)

    # When get_api_key is called
    result = get_api_key()

    # Then it returns the earningscall.api_key value
    assert result == "test-api-key"


def test_get_api_key_returns_ecall_api_key_when_earningscall_api_key_none(monkeypatch):
    """Test that get_api_key returns ECALL_API_KEY when earningscall.api_key is None."""
    # Given earningscall.api_key is None
    monkeypatch.setattr(earningscall, "api_key", None)
    # And ECALL_API_KEY is set
    monkeypatch.setenv("ECALL_API_KEY", "ecall-key")
    # And EARNINGSCALL_API_KEY is cleared
    monkeypatch.delenv("EARNINGSCALL_API_KEY", raising=False)

    # When get_api_key is called
    result = get_api_key()

    # Then it returns the ECALL_API_KEY value
    assert result == "ecall-key"


def test_get_api_key_returns_earningscall_api_key_env_when_ecall_none(monkeypatch):
    """Test that get_api_key returns EARNINGSCALL_API_KEY when ECALL_API_KEY is None."""
    # Given earningscall.api_key is None
    monkeypatch.setattr(earningscall, "api_key", None)
    # And ECALL_API_KEY is not set
    monkeypatch.delenv("ECALL_API_KEY", raising=False)
    # And EARNINGSCALL_API_KEY is set
    monkeypatch.setenv("EARNINGSCALL_API_KEY", "earningscall-key")

    # When get_api_key is called
    result = get_api_key()

    # Then it returns the EARNINGSCALL_API_KEY value
    assert result == "earningscall-key"


def test_get_api_key_prefers_ecall_over_earningscall_env(monkeypatch):
    """Test that get_api_key prefers ECALL_API_KEY over EARNINGSCALL_API_KEY when both are set."""
    # Given earningscall.api_key is None
    monkeypatch.setattr(earningscall, "api_key", None)
    # And both environment variables are set
    monkeypatch.setenv("ECALL_API_KEY", "ecall-key")
    monkeypatch.setenv("EARNINGSCALL_API_KEY", "earningscall-key")

    # When get_api_key is called
    result = get_api_key()

    # Then it returns the ECALL_API_KEY value (preferred)
    assert result == "ecall-key"


def test_get_api_key_returns_demo_when_no_keys_set(monkeypatch):
    """Test that get_api_key returns 'demo' when no API keys are set."""
    # Given earningscall.api_key is None
    monkeypatch.setattr(earningscall, "api_key", None)
    # And no environment variables are set
    monkeypatch.delenv("ECALL_API_KEY", raising=False)
    monkeypatch.delenv("EARNINGSCALL_API_KEY", raising=False)

    # When get_api_key is called
    result = get_api_key()

    # Then it returns "demo"
    assert result == "demo"


def test_get_earnings_call_version_returns_version_when_package_found(monkeypatch):
    """Test that get_earnings_call_version returns version when package is found."""
    # Given importlib.metadata.version returns a version string
    monkeypatch.setattr(importlib.metadata, "version", lambda package: "2.0.0" if package == "earningscall" else None)

    # When get_earnings_call_version is called
    result = get_earnings_call_version()

    # Then it returns the version
    assert result == "2.0.0"


def test_get_earnings_call_version_returns_none_when_package_not_found(monkeypatch):
    """Test that get_earnings_call_version returns None when PackageNotFoundError is raised."""

    # Given importlib.metadata.version raises PackageNotFoundError
    def mock_version(package):
        raise importlib.metadata.PackageNotFoundError(f"Package {package} not found")

    monkeypatch.setattr(importlib.metadata, "version", mock_version)

    # When get_earnings_call_version is called
    result = get_earnings_call_version()

    # Then it returns None
    assert result is None


def test_get_user_agent():
    user_agent = get_user_agent()
    assert user_agent is not None
    assert "EarningsCallPython/" in user_agent
    assert "Python" in user_agent
    assert "Requests" in user_agent


@pytest.fixture()
def setup_api():
    earningscall.api_key = "foobar"
    earningscall.retry_strategy = {
        "strategy": "exponential",
        "base_delay": 0.01,
        "max_attempts": 1,
    }
    purge_cache()
    yield
    earningscall.api_key = None
    earningscall.retry_strategy = None


@responses.activate
def test_get_symbols_v2_raises_on_500(setup_api):
    responses.add(responses.GET, f"{API_BASE}/symbols-v2.txt", status=500)
    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        get_symbols_v2()


@responses.activate
def test_get_symbols_v2_raises_on_404(setup_api):
    responses.add(responses.GET, f"{API_BASE}/symbols-v2.txt", status=404)
    with pytest.raises(requests.HTTPError, match="404 Client Error"):
        get_symbols_v2()


@responses.activate
def test_get_sp500_companies_txt_file_raises_on_500(setup_api):
    responses.add(responses.GET, f"{API_BASE}/symbols/sp500.txt", status=500)
    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        get_sp500_companies_txt_file()


@responses.activate
def test_get_sp500_companies_txt_file_raises_on_404(setup_api):
    responses.add(responses.GET, f"{API_BASE}/symbols/sp500.txt", status=404)
    with pytest.raises(requests.HTTPError, match="404 Client Error"):
        get_sp500_companies_txt_file()


@responses.activate
def test_get_events_raises_on_500(setup_api):
    responses.add(responses.GET, f"{API_BASE}/events", status=500)
    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        get_events("NASDAQ", "AAPL")


@responses.activate
def test_get_events_raises_on_404(setup_api):
    responses.add(responses.GET, f"{API_BASE}/events", status=404)
    with pytest.raises(requests.HTTPError, match="404 Client Error"):
        get_events("NASDAQ", "AAPL")


@responses.activate
def test_get_exchanges_json_raises_on_500(setup_api):
    responses.add(responses.GET, f"https://{DOMAIN}/exchanges.json", status=500)
    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        get_exchanges_json()


@responses.activate
def test_get_exchanges_json_raises_on_404(setup_api):
    responses.add(responses.GET, f"https://{DOMAIN}/exchanges.json", status=404)
    with pytest.raises(requests.HTTPError, match="404 Client Error"):
        get_exchanges_json()
