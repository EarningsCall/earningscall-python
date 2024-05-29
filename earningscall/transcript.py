import logging
from typing import Optional

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from earningscall.event import EarningsEvent

log = logging.getLogger(__file__)


@dataclass_json
@dataclass
class Transcript:

    text: str
    event: Optional[EarningsEvent] = field(default=None)
