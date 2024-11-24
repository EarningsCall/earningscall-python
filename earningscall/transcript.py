from dataclasses import dataclass, field
from typing import List, Optional, Dict

from dataclasses_json import dataclass_json

from earningscall.event import EarningsEvent


@dataclass_json
@dataclass
class SpeakerInfo:
    name: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)


@dataclass_json
@dataclass
class Speaker:
    speaker: str
    speaker_info: Optional[SpeakerInfo] = field(default=None)
    text: Optional[str] = field(default=None)
    words: Optional[List[str]] = field(default=None)
    start_times: Optional[List[float]] = field(default=None)


@dataclass_json
@dataclass
class Transcript:
    text: Optional[str] = field(default=None)
    event: Optional[EarningsEvent] = field(default=None)
    speakers: Optional[List[Speaker]] = field(default=None)
    prepared_remarks: Optional[str] = field(default=None)
    questions_and_answers: Optional[str] = field(default=None)
    speaker_name_map_v2: Optional[Dict[str, SpeakerInfo]] = field(default=None)
