import logging
from typing import Optional, List

import requests

from earningscall import api
from earningscall.errors import InsufficientApiAccessError
from earningscall.event import EarningsEvent
from earningscall.symbols import CompanyInfo
from earningscall.transcript import Transcript

log = logging.getLogger(__file__)


class Company:
    """
    A class representing a company.
    """

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
        level: Optional[int] = None,
    ) -> Optional[Transcript]:
        """
        Get the transcript for a given year and quarter.

        :param Optional[int] year: The year to get the transcript for.
        :param Optional[int] quarter: The quarter to get the transcript for.
        :param Optional[EarningsEvent] event: The event to get the transcript for.
        :param Optional[int] level: The transcript level to retrieve.  Default: 1

        :return: The transcript for the given year and quarter.
        """
        if not self.company_info.exchange or not self.company_info.symbol:
            return None
        if (not year or not quarter) and event:
            year = event.year
            quarter = event.quarter
        if not year or not quarter:
            raise ValueError("Must specify either event or year and quarter")
        if level is None:
            level = 1
        if 1 > level > 4:
            raise ValueError("Invalid level. Must be between 1-4.")
        if type(level) != int or level <= 0 or level > 4:
            raise ValueError(f"Invalid level: {level}.  Must be between 1-4.")
        response_payload = api.get_transcript(
            self.company_info.exchange,
            self.company_info.symbol,
            year,  # type: ignore
            quarter,  # type: ignore
            level=level,
        )
        if not response_payload:
            return None
        transcript = Transcript.from_dict(response_payload)
        if level == 3:
            for speaker in transcript.speakers:
                speaker.text = " ".join(speaker.words)
        if 2 <= level <= 3:
            transcript.text = " ".join(map(lambda spk: spk.text, transcript.speakers))
        elif level == 4:
            transcript.text = " ".join([transcript.prepared_remarks, transcript.questions_and_answers])
        return transcript


    def download_audio_file(
        self,
        year: Optional[int] = None,
        quarter: Optional[int] = None,
        event: Optional[EarningsEvent] = None,
        file_name: Optional[str] = None,
    ) -> Optional[str]:
        """
        Download the audio file for a given year and quarter.

        :param Optional[int] year: The year to get the audio for.
        :param Optional[int] quarter: The quarter to get the audio for.
        :param Optional[EarningsEvent] event: The event to get the audio for.
        :param Optional[str] file_name: The file name to save the audio to.

        :return: The audio for the given year and quarter.
        """
        log.info(f"Downloading audio file for {self.company_info.symbol} {event}")
        if not self.company_info.exchange or not self.company_info.symbol:
            return None
        if (not year or not quarter) and event:
            year = event.year
            quarter = event.quarter
        if (not year or not quarter) and not event:
            raise ValueError("Must specify either event or year and quarter")
        try:
            resp = api.download_audio_file(
                exchange=self.company_info.exchange,
                symbol=self.company_info.symbol,
                year=year,  # type: ignore
                quarter=quarter,  # type: ignore
                file_name=file_name,
            )
            return resp
        except requests.exceptions.HTTPError as error:
            log.error(f"Error downloading audio file: {error}")
            if error.response.status_code == 404:
                return None
            if error.response.status_code == 403:
                raise InsufficientApiAccessError(f"Insufficient API access for {self.company_info.symbol}")
            raise error
