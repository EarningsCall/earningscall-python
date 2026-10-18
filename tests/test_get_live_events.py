import pytest
import requests
import responses

import earningscall
from earningscall import get_live_events
from earningscall.api import API_BASE, purge_cache
from earningscall.live import LiveEvent, LiveTranscriptLinks
from earningscall.utils import data_path

# Uncomment and run following code to generate data/live-events-demo-schema-v4.yaml file
#
# import requests
# from responses import _recorder
#
#
# @_recorder.record(file_path="data/live-events-demo-schema-v4.yaml")
# def test_save_live_events():
#     requests.get("https://api.earningscall.dev/live?apikey=demo", headers={"X-API-Version-Schema": "v4"})


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run"""
    # Setup
    earningscall.api_key = None
    earningscall.retry_strategy = {
        "strategy": "exponential",
        "base_delay": 0.01,
        "max_attempts": 1,
    }
    purge_cache()
    yield  # this is where the testing happens
    # Teardown
    earningscall.api_key = None
    earningscall.retry_strategy = None


@responses.activate
def test_get_live_events_demo():
    responses._add_from_file(file_path=data_path("live-events-demo-schema-v4.yaml"))
    ##
    events = get_live_events()
    ##
    assert responses.calls[0].request.headers["X-API-Version-Schema"] == "v4"
    assert len(events) == 1
    assert events[0].exchange == "NASDAQ"
    assert events[0].symbol == "AAPL"
    assert events[0].year == 2024
    assert events[0].quarter == 4
    assert events[0].company_name == "Apple Inc."
    assert events[0].event_date.isoformat() == "2024-11-01T17:00:00+00:00"
    assert events[0].streaming_url == "https://earningscall.biz/live-demo/dynamic-playlist/playlist.m3u8"
    assert events[0].live_transcript is None


@responses.activate
def test_get_live_events_with_live_transcript():
    earningscall.api_key = "XXXXXXXXXXX"
    responses.add(
        responses.GET,
        f"{API_BASE}/live",
        json={
            "events": [
                {
                    "exchange": "NYSE",
                    "symbol": "JPM",
                    "year": 2026,
                    "quarter": 3,
                    "company_name": "JP Morgan Chase & Co.",
                    "event_date": "2026-10-14T07:00:00-04:00",
                    "streaming_url": "https://earningscall.biz/live/abc123/playlist.m3u8",
                    "live_transcript": {
                        "experimental": True,
                        "note": "The live transcript feature is experimental. It may change. Do not rely on it.",
                        "token": "abc123",
                        "poll_url": "https://earningscall.biz/live/abc123/transcript",
                        "websocket_url": "wss://ws.earningscall.biz",
                        "websocket_action": "live-transcript",
                    },
                }
            ]
        },
    )
    ##
    events = get_live_events()
    ##
    assert len(events) == 1
    assert events[0].symbol == "JPM"
    assert events[0].event_date.isoformat() == "2026-10-14T07:00:00-04:00"
    assert events[0].live_transcript == LiveTranscriptLinks(
        experimental=True,
        note="The live transcript feature is experimental. It may change. Do not rely on it.",
        token="abc123",
        poll_url="https://earningscall.biz/live/abc123/transcript",
        websocket_url="wss://ws.earningscall.biz",
        websocket_action="live-transcript",
    )


def test_live_transcript_tolerates_changed_fields():
    # The live transcript links are experimental, so added or removed fields must not break parsing.
    event = LiveEvent.from_dict(
        {
            "exchange": "NASDAQ",
            "symbol": "MSFT",
            "year": 2026,
            "quarter": 1,
            "company_name": "Microsoft Corporation",
            "event_date": "2026-10-28T17:30:00-04:00",
            "streaming_url": "https://earningscall.biz/live/def456/playlist.m3u8",
            "live_transcript": {"experimental": True, "some_future_field": "value"},
        }
    )
    assert event.live_transcript == LiveTranscriptLinks(experimental=True)


@pytest.mark.parametrize("live_transcript", [None, [{"poll_url": "x"}], "https://example.com/transcript", True])
@responses.activate
def test_get_live_events_drops_live_transcript_that_is_not_an_object(live_transcript):
    # If the experimental links change from an object to something else, the events still parse.
    earningscall.api_key = "XXXXXXXXXXX"
    event = {
        "exchange": "NASDAQ",
        "symbol": "MSFT",
        "year": 2026,
        "quarter": 1,
        "company_name": "Microsoft Corporation",
        "event_date": "2026-10-28T17:30:00-04:00",
        "streaming_url": "https://earningscall.biz/live/def456/playlist.m3u8",
        "live_transcript": live_transcript,
    }
    responses.add(responses.GET, f"{API_BASE}/live", json={"events": [event]})
    ##
    events = get_live_events()
    ##
    assert len(events) == 1
    assert events[0].symbol == "MSFT"
    assert events[0].live_transcript is None


@responses.activate
def test_get_live_events_none_live():
    earningscall.api_key = "XXXXXXXXXXX"
    responses.add(responses.GET, f"{API_BASE}/live", json={"events": []})
    assert get_live_events() == []


@responses.activate
def test_get_live_events_raises_on_500():
    earningscall.api_key = "XXXXXXXXXXX"
    responses.add(responses.GET, f"{API_BASE}/live", status=500)
    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        get_live_events()
