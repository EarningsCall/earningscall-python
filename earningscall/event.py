import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import config
from dataclasses_json import dataclass_json
from marshmallow import fields

log = logging.getLogger(__file__)


@dataclass_json
@dataclass
class EarningsEvent:
    """
    EarningsEvent
    """

    year: int
    quarter: int
    conference_date: Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda date: date.isoformat() if date else None,
            decoder=lambda date: datetime.fromisoformat(date) if date else None,
            mm_field=fields.DateTime(format="iso"),
        ),
    )
