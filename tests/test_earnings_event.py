import datetime

from earningscall.event import EarningsEvent


def test_basic_object_creation():
    event = EarningsEvent(
        year=2024,
        quarter=1,
        conference_date=datetime.datetime.fromisoformat("2024-04-28T15:00:00.000-05:00"),
    )
    event.to_json()


def test_basic_without_conference_date():
    event = EarningsEvent(
        year=2024,
        quarter=1,
    )
    raw_json = event.to_json()
    event_after = EarningsEvent.from_json(raw_json)
    assert event_after.conference_date is None
    assert event_after.year == 2024
    assert event_after.quarter == 1


def test_date_field_deserialization():
    #
    earnings_event = EarningsEvent.from_dict(
        {
            "year": 2024,
            "quarter": 1,
            "conference_date": "2024-04-28T15:00:00.000-05:00",
        }
    )
    #
    assert earnings_event.year == 2024
    assert earnings_event.quarter == 1
    assert earnings_event.conference_date == datetime.datetime.fromisoformat("2024-04-28T15:00:00.000-05:00")
    assert earnings_event.conference_date.isoformat() == "2024-04-28T15:00:00-05:00"
