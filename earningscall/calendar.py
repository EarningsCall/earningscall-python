from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import config
from dataclasses_json import dataclass_json
from marshmallow import fields


@dataclass_json
@dataclass
class CalendarEvent:
    """
    CalendarEvent
    """

    company_name: str
    exchange: str
    symbol: str
    year: int
    quarter: int
    transcript_ready: bool
    conference_date: Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda date: date.isoformat() if date else None,
            decoder=lambda date: datetime.fromisoformat(date) if date else None,
            mm_field=fields.DateTime(format="iso"),
        ),
    )
