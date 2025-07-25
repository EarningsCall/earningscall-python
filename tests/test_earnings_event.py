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


def test_date_field_deserialization_with_z_suffix():
    """Test that the 'Z' UTC suffix is properly handled."""
    earnings_event = EarningsEvent.from_dict(
        {
            "year": 2021,
            "quarter": 1,
            "conference_date": "2021-01-25T13:30:00.000Z",
        }
    )
    assert earnings_event.year == 2021
    assert earnings_event.quarter == 1
    # Verify the date was parsed correctly as UTC
    expected_date = datetime.datetime.fromisoformat("2021-01-25T13:30:00.000+00:00")
    assert earnings_event.conference_date == expected_date
    assert earnings_event.conference_date.tzinfo is not None  # Should have timezone info
