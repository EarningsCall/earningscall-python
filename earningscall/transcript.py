from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from earningscall.event import EarningsEvent


@dataclass_json
@dataclass
class Speaker:
    speaker: str
    text: Optional[str] = field(default=None)
    words: Optional[list[str]] = field(default=None)
    start_times: Optional[list[float]] = field(default=None)


@dataclass_json
@dataclass
class Transcript:
    text: Optional[str] = field(default=None)
    event: Optional[EarningsEvent] = field(default=None)
    speakers: list[Speaker] = field(default=None)
    prepared_remarks: Optional[str] = field(default=None)
    questions_and_answers: Optional[str] = field(default=None)
