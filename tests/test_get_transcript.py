import json

import pytest
import responses
from requests import HTTPError

import earningscall
from earningscall import get_company
from earningscall.api import purge_cache
from earningscall.company import Company
from earningscall.errors import InsufficientApiAccessError, InvalidApiKeyError
from earningscall.event import EarningsEvent
from earningscall.symbols import clear_symbols, CompanyInfo
from earningscall.transcript import Transcript, normalize_transcript_payload
from earningscall.utils import data_path

# Uncomment and run following code to generate msft-transcript-response.yaml file
#
# from responses import _recorder
# @_recorder.record(file_path="msft-transcript-response.yaml")
# def test_save_symbols_v1():
#     requests.get("https://api.earningscall.dev/transcript?apikey=demo&exchange=NASDAQ&symbol=MSFT&year=2023&quarter=1")


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    earningscall.api_key = None
    earningscall.retry_strategy = {
        "strategy": "exponential",
        "base_delay": 0.01,
        "max_attempts": 3,
    }
    purge_cache()
    clear_symbols()
    yield  # this is where the testing happens
    # Teardown : fill with any logic you want
    earningscall.api_key = None


@responses.activate
def test_get_transcript_invalid_inputs():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
    ##
    company = get_company("msft")
    ##
    with pytest.raises(ValueError):
        company.get_transcript(year=2023)
    with pytest.raises(ValueError):
        company.get_transcript(quarter=1)
    with pytest.raises(ValueError):
        company.get_transcript(quarter=0)
    with pytest.raises(ValueError):
        company.get_transcript(year=2023, quarter=5)
    with pytest.raises(ValueError):
        company.get_transcript(year=2023, quarter=1, level=0)
    with pytest.raises(ValueError):
        company.get_transcript(year=2023, quarter=1, level=5)
    ##
    invalid_company = Company(company_info=CompanyInfo())
    transcript = invalid_company.get_transcript(year=2023, quarter=1)
    ##
    assert transcript is None


@responses.activate
def test_get_demo_company():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
    ##
    company = get_company("msft")
    ##
    transcript = company.get_transcript(year=2023, quarter=1)
    assert transcript.text[:100] == (
        'Greetings, and welcome to the Microsoft Fiscal Year 2023 First Quarter Earnings ' 'Conference Call. At '
    )


@responses.activate
def test_get_demo_company_with_event_populated():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("demo-symbols-v2-alpha.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(event=EarningsEvent(year=2022, quarter=1))
    assert transcript.event.year == 2022
    assert transcript.event.quarter == 1
    assert transcript.event.conference_date.isoformat() == "2022-01-19T00:00:00-08:00"
    assert transcript.text[:100] == (
        "Good day and welcome to the Apple Q1 Fiscal Year 2021 earnings conference " "call. Today's call is bein"
    )


@responses.activate
def test_get_demo_company_with_advanced_transcript_data():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2022-advanced-data-level-2.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2022, quarter=1, level=2)
    ##
    assert transcript.event.year == 2022
    assert transcript.event.quarter == 1
    assert transcript.event.conference_date.isoformat() == "2022-01-27T14:00:00-08:00"
    assert transcript.text[:100] == (
        "Good day and welcome to the Apple Q1 FY 2022 earnings conference call. Today's call is being recorde"
    )
    assert transcript.speakers[0].speaker == "spk03"
    assert transcript.speakers[0].words is None
    assert transcript.speakers[0].start_times is None


@responses.activate
def test_get_demo_company_with_speaker_name_map_v2():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2022-speaker-name-map-v2.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2023, quarter=1, level=2)
    ##
    assert transcript.event.year == 2023
    assert transcript.event.quarter == 1
    assert transcript.event.conference_date.isoformat() == "2023-02-02T17:00:00-05:00"
    assert transcript.text[:100] == (
        "Good day, everyone, and welcome to the Apple Q1 Fiscal Year 2023 Earnings Conference Call. Today's c"
    )
    assert transcript.speakers[0].speaker == "spk12"
    assert transcript.speakers[0].speaker_info.name == "Teja Skala"
    assert transcript.speakers[0].speaker_info.title == "Director of Investor Relations and Corporate Finance"
    assert transcript.speakers[0].words is None
    assert transcript.speakers[0].start_times is None
    assert transcript.speakers[1].speaker == "spk07"
    assert transcript.speakers[1].speaker_info.name == "Operator"
    assert transcript.speakers[1].speaker_info.title is None
    assert transcript.speakers[1].words is None
    assert transcript.speakers[1].start_times is None
    assert transcript.speaker_name_map_v2["spk01"].name == "Tim Cook"
    assert transcript.speaker_name_map_v2["spk01"].title == "CEO"


@responses.activate
def test_get_transcript_schema_v4_level_2():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2023-level-2-schema-v4.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2023, quarter=1, level=2)
    ##
    assert responses.calls[-1].request.headers["X-API-Version-Schema"] == "v4"
    assert transcript.event.year == 2023
    assert transcript.event.quarter == 1
    assert transcript.event.conference_date.isoformat() == "2023-02-02T17:00:00-05:00"
    assert transcript.text[:100] == (
        "Good day, everyone, and welcome to the Apple Q1 Fiscal Year 2023 Earnings Conference Call. Today's c"
    )
    assert transcript.speakers[0].speaker == "spk12"
    assert transcript.speakers[0].speaker_info.name == "Teja Skala"
    assert transcript.speakers[0].speaker_info.title == "Director of Investor Relations and Corporate Finance"
    assert transcript.speakers[0].words is None
    assert transcript.speaker_name_map_v2["spk01"].name == "Tim Cook"
    assert transcript.speaker_name_map_v2["spk01"].title == "CEO"


@responses.activate
def test_get_transcript_schema_v4_level_3():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2023-level-3-schema-v4.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2023, quarter=1, level=3)
    ##
    speaker = transcript.speakers[0]
    assert speaker.speaker == "spk12"
    assert speaker.speaker_info.name == "Teja Skala"
    assert len(speaker.words) == len(speaker.start_times)
    assert speaker.text == " ".join(speaker.words)
    assert transcript.text.startswith("Good day, everyone, and welcome to the Apple Q1 Fiscal Year 2023")


def _get_aapl_q1_2023_level_2_transcript(fixture_file_name: str) -> Transcript:
    with responses.RequestsMock(assert_all_requests_are_fired=False) as mock:
        mock._add_from_file(file_path=data_path("symbols-v2.yaml"))
        mock._add_from_file(file_path=data_path(fixture_file_name))
        clear_symbols()
        company = get_company("aapl")
        assert company
        transcript = company.get_transcript(year=2023, quarter=1, level=2)
        assert transcript
        return transcript


def test_get_transcript_schema_v4_matches_v2():
    v2_transcript = _get_aapl_q1_2023_level_2_transcript("aapl-q1-2022-speaker-name-map-v2.yaml")
    v4_transcript = _get_aapl_q1_2023_level_2_transcript("aapl-q1-2023-level-2-schema-v4.yaml")
    ##
    assert v4_transcript.text == v2_transcript.text
    assert v4_transcript.event == v2_transcript.event
    assert v4_transcript.speakers == v2_transcript.speakers
    assert v4_transcript.speaker_name_map_v2 == v2_transcript.speaker_name_map_v2


def test_normalize_transcript_payload_leaves_v2_payload_unchanged():
    payload = {
        "speakers": [{"speaker": "spk01", "text": "Hello."}],
        "speaker_name_map_v2": {"spk01": {"name": "Tim Cook", "title": "CEO"}},
    }
    assert normalize_transcript_payload(payload) is payload


def test_normalize_transcript_payload_leaves_payload_without_speakers_unchanged():
    payload = {"text": "Hello."}
    assert normalize_transcript_payload(payload) is payload


def test_normalize_transcript_payload_converts_v4_speakers():
    payload = {
        "speakers": [
            {"speaker": {"id": "spk01", "name": "Tim Cook", "title": "CEO"}, "text": "Hello."},
            {"speaker": {"id": "spk02", "name": "Operator"}, "text": "First question."},
            {"speaker": {"id": "spk01", "name": "Tim Cook", "title": "CEO"}, "text": "Thanks."},
        ],
    }
    ##
    normalized = normalize_transcript_payload(payload)
    ##
    assert [speaker["speaker"] for speaker in normalized["speakers"]] == ["spk01", "spk02", "spk01"]
    assert [speaker["text"] for speaker in normalized["speakers"]] == ["Hello.", "First question.", "Thanks."]
    assert normalized["speaker_name_map_v2"] == {
        "spk01": {"name": "Tim Cook", "title": "CEO"},
        "spk02": {"name": "Operator", "title": None},
    }
    # The input payload is not mutated
    assert payload["speakers"][0]["speaker"] == {"id": "spk01", "name": "Tim Cook", "title": "CEO"}
    assert "speaker_name_map_v2" not in payload


@responses.activate
def test_get_demo_company_with_advanced_transcript_data_level_3():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2022-advanced-data-level-3.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2022, quarter=1, level=3)
    ##
    assert transcript.event.year == 2022
    assert transcript.event.quarter == 1
    assert transcript.event.conference_date.isoformat() == "2022-01-27T14:00:00-08:00"
    assert transcript.text[:100] == (
        "Good day and welcome to the Apple Q1 FY 2022 earnings conference call. Today's call is being recorde"
    )
    assert transcript.speakers[0].speaker == "spk03"
    assert " ".join(transcript.speakers[0].words)[:100] == (
        "Good day and welcome to the Apple Q1 FY 2022 earnings conference call. Today's call is being recorde"
    )
    assert transcript.speakers[0].start_times[:7] == [
        0.029,
        0.189,
        0.429,
        0.57,
        0.91,
        1.03,
        1.27,
    ]


@responses.activate
def test_get_demo_company_with_advanced_transcript_data_level_4():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2022-advanced-data-level-4.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2022, quarter=1, level=4)
    ##
    assert transcript.event.year == 2022
    assert transcript.event.quarter == 1
    assert transcript.event.conference_date.isoformat() == "2022-01-27T14:00:00-08:00"
    assert transcript.text[:100] == (
        "Good day and welcome to the Apple Q1 FY 2022 earnings conference call. Today's call is being recorde"
    )
    assert transcript.prepared_remarks[:100] == (
        "Good day and welcome to the Apple Q1 FY 2022 earnings conference call. Today's call is being recorde"
    )
    assert transcript.questions_and_answers[:100] == (
        "We'll take our first question from Katie Huberty with Morgan Stanley. Caller, please check your mute"
    )

    assert transcript.speakers is None


@responses.activate
def test_get_demo_company_with_advanced_transcript_data_level_4_q_and_a_is_missing():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("nvda-q2-2025-level-4-data-missing.yaml"))
    ##
    company = get_company("nvda")
    ##
    transcript = company.get_transcript(year=2025, quarter=2, level=4)
    ##
    assert transcript.event.year == 2025
    assert transcript.event.quarter == 2
    assert transcript.event.conference_date.isoformat() == "2024-08-28T17:00:00-04:00"
    assert transcript.text[:100] == (
        "Good afternoon, everyone, and welcome to NVIDIA's conference call for the second quarter of fiscal 2"
    )
    assert transcript.prepared_remarks[:100] == (
        "Good afternoon, everyone, and welcome to NVIDIA's conference call for the second quarter of fiscal 2"
    )
    assert transcript.questions_and_answers is None
    assert transcript.speakers is None


@responses.activate
def test_get_non_demo_company():
    ##
    responses._add_from_file(file_path=data_path("demo-symbols-v2.yaml"))
    ##
    with pytest.raises(InsufficientApiAccessError):
        get_company("nvda")


@responses.activate
def test_get_transcript_not_found():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2030-not-found.yaml"))
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2030, quarter=1)
    ##
    assert transcript is None


@responses.activate
def test_get_transcript_not_authorized_level_1():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2030-not-authorized.yaml"))
    ##
    company = get_company("aapl")
    ##
    with pytest.raises(InsufficientApiAccessError):
        company.get_transcript(year=2030, quarter=1)


@responses.activate
def test_get_transcript_not_authorized_level_2():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2030-not-authorized-l2.yaml"))
    ##
    company = get_company("aapl")
    ##
    with pytest.raises(InsufficientApiAccessError):
        company.get_transcript(year=2030, quarter=1, level=2)


@responses.activate
def test_get_transcript_server_error():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("aapl-q1-2030-server-error.yaml"))
    ##
    company = get_company("aapl")
    ##
    with pytest.raises(HTTPError):
        company.get_transcript(year=2030, quarter=1)


def test_data_class_for_transcript():
    ##
    transcript = Transcript.from_dict(
        {
            "speakers": [],
            "speaker_name_map_v2": {
                "spk01": {
                    "name": "John Doe",
                    "title": "CEO",
                }
            },
        }
    )
    ##
    assert transcript.speaker_name_map_v2["spk01"].name == "John Doe"
    assert transcript.speaker_name_map_v2["spk01"].title == "CEO"


@responses.activate
def test_get_transcript_with_rate_limit_backoff_and_retry():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    # First response
    responses.add(
        responses.GET,
        "https://api.earningscall.dev/transcript?apikey=demo&exchange=NASDAQ&symbol=AAPL&year=2023&quarter=1&level=1",
        body=json.dumps({"error": "Rate limit exceeded"}),
        status=429,
    )
    # Second response
    responses.add(
        responses.GET,
        "https://api.earningscall.dev/transcript?apikey=demo&exchange=NASDAQ&symbol=AAPL&year=2023&quarter=1&level=1",
        body=json.dumps({"text": "Hello, world!"}),
        status=200,
    )
    ##
    company = get_company("aapl")
    ##
    transcript = company.get_transcript(year=2023, quarter=1, level=1)
    # ##
    assert transcript.text == "Hello, world!"


@responses.activate
def test_get_transcript_fails_all_attempts():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    # Always throttle the caller
    responses.add(
        responses.GET,
        "https://api.earningscall.dev/transcript?apikey=demo&exchange=NASDAQ&symbol=AAPL&year=2023&quarter=1&level=1",
        body=json.dumps({"error": "Rate limit exceeded"}),
        status=429,
    )
    ##
    company = get_company("aapl")
    ##
    with pytest.raises(HTTPError):
        company.get_transcript(year=2023, quarter=1, level=1)


@responses.activate
def test_get_transcript_fails_all_attempts_linear_retry_strategy():
    earningscall.retry_strategy = {
        "strategy": "linear",
        "base_delay": 0.01,
        "max_attempts": 3,
    }
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    # Always throttle the caller
    responses.add(
        responses.GET,
        "https://api.earningscall.dev/transcript?apikey=demo&exchange=NASDAQ&symbol=AAPL&year=2023&quarter=1&level=1",
        body=json.dumps({"error": "Rate limit exceeded"}),
        status=429,
    )
    ##
    company = get_company("aapl")
    ##
    with pytest.raises(HTTPError):
        company.get_transcript(year=2023, quarter=1, level=1)


@responses.activate
def test_get_transcript_fails_all_attempts_invalid_retry_strategy():
    earningscall.retry_strategy = {
        "strategy": "invalid",
        "base_delay": 0.01,
        "max_attempts": 3,
    }
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    # Always throttle the caller
    responses.add(
        responses.GET,
        "https://api.earningscall.dev/transcript?apikey=demo&exchange=NASDAQ&symbol=AAPL&year=2023&quarter=1&level=1",
        body=json.dumps({"error": "Rate limit exceeded"}),
        status=429,
    )
    ##
    company = get_company("aapl")
    ##
    with pytest.raises(ValueError):
        company.get_transcript(year=2023, quarter=1, level=1)


@responses.activate
def test_get_company_fails_not_authorized():
    # Always throttle the caller
    responses.add(
        responses.GET,
        "https://api.earningscall.dev/symbols-v2.txt",
        body=json.dumps({"error": "Not authorized"}),
        status=401,
    )
    ##
    with pytest.raises(InvalidApiKeyError):
        get_company("aapl")


# Uncomment and run following code to generate demo-symbols-v2.yaml file
#
# import requests
#
# from responses import _recorder
#
#
# @_recorder.record(file_path="data/nvda-q2-2025-level-4-data-missing.yaml")
# def test_save_symbols_v1_first():
#     requests.get("https://api.earningscall.dev/transcript?apikey=demo&exchange=NASDAQ&symbol=NVDA&year=2025&quarter=2&level=4")

# Uncomment and run following code to generate demo-symbols-v2.yaml file

# import requests
#
# from responses import _recorder
#
#
# @_recorder.record(file_path="data/aapl-q1-2030-not-found.yaml")
# def test_save_symbols_v1_second():
#     requests.get(
#         "https://api.earningscall.dev/transcript?apikey=demo&exchange=NASDAQ&symbol=AAPL&year=2030&quarter=1&level=1"
#     )
