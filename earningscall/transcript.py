import logging
from dataclasses import dataclass

from dataclasses_json import dataclass_json

log = logging.getLogger(__file__)


@dataclass_json
@dataclass
class Transcript:

    text: str

