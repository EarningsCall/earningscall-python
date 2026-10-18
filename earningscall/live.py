from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import config
from dataclasses_json import dataclass_json
from marshmallow import fields


@dataclass_json
@dataclass
class LiveTranscriptLinks:
    """
    Links to the provisional transcript of a call that is in progress.

    Experimental: the API may change or remove these fields, so every field is optional.
    """

    experimental: Optional[bool] = field(default=None)
    note: Optional[str] = field(default=None)
    token: Optional[str] = field(default=None)
    poll_url: Optional[str] = field(default=None)
    websocket_url: Optional[str] = field(default=None)
    websocket_action: Optional[str] = field(default=None)


@dataclass_json
@dataclass
class LiveEvent:
    """
    LiveEvent
    """

    exchange: str
    symbol: str
    year: int
    quarter: int
    company_name: str
    streaming_url: str
    event_date: Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda date: date.isoformat() if date else None,
            decoder=lambda date: datetime.fromisoformat(date) if date else None,
            mm_field=fields.DateTime(format="iso"),
        ),
    )
    live_transcript: Optional[LiveTranscriptLinks] = field(default=None)
