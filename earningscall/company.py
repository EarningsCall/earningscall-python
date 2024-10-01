import logging
from typing import Optional, List

from earningscall import api
from earningscall.event import EarningsEvent
from earningscall.symbols import CompanyInfo
from earningscall.transcript import Transcript

log = logging.getLogger(__file__)


class Company:

    company_info: CompanyInfo
    name: Optional[str]
    _events: Optional[List[EarningsEvent]]

    def __init__(self, company_info: CompanyInfo):
        if not company_info:
            raise ValueError("company_info must be present.")
        self.company_info = company_info
        self.name = company_info.name
        self._events = None

    def __str__(self):
        return str(self.name)

    def _get_events(self) -> List[EarningsEvent]:
        if not self.company_info.exchange or not self.company_info.symbol:
            return []
        raw_response = api.get_events(self.company_info.exchange, self.company_info.symbol)
        if not raw_response:
            return []
        return [EarningsEvent.from_dict(event) for event in raw_response["events"]]  # type: ignore

    def events(self) -> List[EarningsEvent]:
        if not self._events:
            self._events = self._get_events()
        return self._events

    def get_transcript(
        self,
        year: Optional[int] = None,
        quarter: Optional[int] = None,
        event: Optional[EarningsEvent] = None,
    ) -> Optional[Transcript]:
        """
        Get the transcript for a given year and quarter.

        Args:
            year (Optional[int]): The year to get the transcript for.
            quarter (Optional[int]): The quarter to get the transcript for.
            event (Optional[EarningsEvent]): The event to get the transcript for.

        Returns:
            Optional[Transcript]: The transcript for the given year and quarter.
        """
        if not self.company_info.exchange or not self.company_info.symbol:
            return None
        if (not year or not quarter) and event:
            year = event.year
            quarter = event.quarter
        if (not year or not quarter) and not event:
            raise ValueError("Must specify either event or year and quarter")
        resp = api.get_transcript(
            self.company_info.exchange,
            self.company_info.symbol,
            year,  # type: ignore
            quarter,  # type: ignore
            level=None,  # TODO: Pass level to API
        )
        # TODO: Parse Advanced transcript data
        if not resp:
            return None
        return Transcript.from_dict(resp)  # type: ignore

    def download_audio_file(
        self,
        year: Optional[int] = None,
        quarter: Optional[int] = None,
        event: Optional[EarningsEvent] = None,
        file_name: Optional[str] = None,
    ) -> Optional[str]:
        """
        Download the audio file for a given year and quarter.

        Args:
            year (Optional[int]): The year to get the audio for.
            quarter (Optional[int]): The quarter to get the audio for.
            event (Optional[EarningsEvent]): The event to get the audio for.
            file_name (Optional[str]): The file name to save the audio to.

        Returns:
            Optional[str]: The audio for the given year and quarter.
        """
        if not self.company_info.exchange or not self.company_info.symbol:
            return None
        if (not year or not quarter) and event:
            year = event.year
            quarter = event.quarter
        if (not year or not quarter) and not event:
            raise ValueError("Must specify either event or year and quarter")
        resp = api.download_audio_file(
            exchange=self.company_info.exchange,
            symbol=self.company_info.symbol,
            year=year,  # type: ignore
            quarter=quarter,  # type: ignore
            file_name=file_name,
        )
        return resp
