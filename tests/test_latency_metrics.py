import responses

import earningscall
from earningscall.api import (
    API_BASE,
    clear_latency_metrics,
    do_get,
    get_exchanges_json,
    get_latency_metrics,
    get_latency_metrics_summary,
    pop_latency_metrics,
)

import pytest


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    earningscall.api_key = None
    earningscall.retry_strategy = {
        "strategy": "exponential",
        "base_delay": 0,
        "max_attempts": 3,
    }
    earningscall.enable_requests_cache = False
    earningscall.enable_telemetry = True
    earningscall.telemetry_max_entries = 1000
    clear_latency_metrics()
    yield
    clear_latency_metrics()
    earningscall.api_key = None
    earningscall.retry_strategy = None
    earningscall.enable_requests_cache = True
    earningscall.enable_telemetry = True
    earningscall.telemetry_max_entries = 1000


@responses.activate
def test_do_get_collects_latency_metrics():
    responses.add(
        responses.GET,
        f"{API_BASE}/symbols-v2.txt?apikey=demo",
        body="AAPL\nMSFT",
        status=200,
    )

    response = do_get("symbols-v2.txt")

    assert response.status_code == 200
    metrics = get_latency_metrics()
    assert len(metrics) == 1
    metric = metrics[0]
    assert metric["method"] == "GET"
    assert metric["target"] == "symbols-v2.txt"
    assert metric["status_code"] == 200
    assert metric["attempts"] == 1
    assert metric["error_type"] is None
    assert metric["duration_ms"] >= 0


@responses.activate
def test_do_get_latency_metrics_include_retry_attempts():
    earningscall.retry_strategy = {
        "strategy": "linear",
        "base_delay": 0,
        "max_attempts": 3,
    }
    url = f"{API_BASE}/transcript?apikey=demo&exchange=NASDAQ&symbol=AAPL&year=2023&quarter=1&level=1"
    responses.add(
        responses.GET,
        url,
        json={"error": "Rate limit exceeded"},
        status=429,
    )
    responses.add(
        responses.GET,
        url,
        json={"text": "hello"},
        status=200,
    )

    response = do_get(
        "transcript",
        params={
            "exchange": "NASDAQ",
            "symbol": "AAPL",
            "year": "2023",
            "quarter": "1",
            "level": "1",
        },
    )

    assert response.status_code == 200
    metrics = get_latency_metrics()
    assert len(metrics) == 1
    metric = metrics[0]
    assert metric["attempts"] == 2
    assert metric["status_code"] == 200


@responses.activate
def test_latency_metrics_summary_and_drain():
    url = f"{API_BASE}/symbols-v2.txt?apikey=demo"
    responses.add(responses.GET, url, body="AAPL", status=200)
    responses.add(responses.GET, url, body="MSFT", status=200)

    do_get("symbols-v2.txt")
    do_get("symbols-v2.txt")

    summary = get_latency_metrics_summary()
    assert len(summary) == 1
    assert summary[0]["target"] == "symbols-v2.txt"
    assert summary[0]["count"] == 2
    assert summary[0]["retry_count"] == 0
    assert summary[0]["p95_duration_ms"] >= summary[0]["min_duration_ms"]

    drained_metrics = pop_latency_metrics()
    assert len(drained_metrics) == 2
    assert get_latency_metrics() == []


@responses.activate
def test_latency_metrics_respect_max_entries():
    earningscall.telemetry_max_entries = 1
    responses.add(
        responses.GET,
        f"{API_BASE}/symbols-v2.txt?apikey=demo",
        body="AAPL",
        status=200,
    )
    responses.add(
        responses.GET,
        f"{API_BASE}/symbols/sp500.txt?apikey=demo",
        body="AAPL\nMSFT",
        status=200,
    )

    do_get("symbols-v2.txt")
    do_get("symbols/sp500.txt")

    metrics = get_latency_metrics()
    assert len(metrics) == 1
    assert metrics[0]["target"] == "symbols/sp500.txt"


@responses.activate
def test_latency_metrics_can_be_disabled():
    earningscall.enable_telemetry = False
    responses.add(
        responses.GET,
        f"{API_BASE}/symbols-v2.txt?apikey=demo",
        body="AAPL",
        status=200,
    )

    do_get("symbols-v2.txt")

    assert get_latency_metrics() == []


@responses.activate
def test_telemetry_max_entries_zero_disables_collection():
    earningscall.telemetry_max_entries = 0
    responses.add(
        responses.GET,
        f"{API_BASE}/symbols-v2.txt?apikey=demo",
        body="AAPL",
        status=200,
    )

    do_get("symbols-v2.txt")

    assert get_latency_metrics() == []


@responses.activate
def test_latency_metrics_summary_with_reset():
    url = f"{API_BASE}/symbols-v2.txt?apikey=demo"
    responses.add(responses.GET, url, body="AAPL", status=200)

    do_get("symbols-v2.txt")

    summary = get_latency_metrics_summary(reset=True)
    assert len(summary) == 1
    assert summary[0]["count"] == 1
    # Buffer should be drained after reset=True
    assert get_latency_metrics() == []


@responses.activate
def test_get_exchanges_json_collects_absolute_url_metrics():
    responses.add(
        responses.GET,
        "https://earningscall.biz/exchanges.json",
        json={"exchanges": []},
        status=200,
    )

    exchanges_payload = get_exchanges_json()

    assert exchanges_payload == {"exchanges": []}
    metrics = get_latency_metrics()
    assert len(metrics) == 1
    assert metrics[0]["target"] == "https://earningscall.biz/exchanges.json"
