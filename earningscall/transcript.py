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


def normalize_transcript_payload(payload: dict) -> dict:
    """
    Convert schema v4 speakers to the shape the Transcript model exposes.

    Schema v4 inlines each speaker as {"id", "name", "title"}, while the model keeps the
    speaker id in Speaker.speaker and names/titles in speaker_name_map_v2.  Payloads that
    are already in that shape are returned unchanged.
    """
    speakers = payload.get("speakers")
    if not speakers or not any(isinstance(speaker.get("speaker"), dict) for speaker in speakers):
        return payload
    speaker_name_map = dict(payload.get("speaker_name_map_v2") or {})
    normalized_speakers = []
    for speaker in speakers:
        speaker_info = speaker.get("speaker")
        if isinstance(speaker_info, dict):
            speaker_id = speaker_info.get("id")
            speaker_name_map.setdefault(
                speaker_id, {"name": speaker_info.get("name"), "title": speaker_info.get("title")}
            )
            speaker = {**speaker, "speaker": speaker_id}
        normalized_speakers.append(speaker)
    return {**payload, "speakers": normalized_speakers, "speaker_name_map_v2": speaker_name_map}
