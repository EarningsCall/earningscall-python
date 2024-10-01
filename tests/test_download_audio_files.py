import os

import pytest
import responses

from earningscall import get_company
from earningscall.api import purge_cache
from earningscall.event import EarningsEvent
from earningscall.symbols import clear_symbols
from earningscall.utils import data_path


@responses.activate
def test_download_audio_file():
    ##
    purge_cache()
    clear_symbols()
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-q1-2022-audio-file-short-clip.yaml"))
    responses._add_from_file(file_path=data_path("msft-company-events.yaml"))
    ##
    company = get_company("msft")
    file_name = company.download_audio_file(year=2022, quarter=1)
    #
    assert os.path.exists(file_name)
    assert os.path.getsize(file_name) > 0


@responses.activate
def test_download_audio_file_event():
    ##
    purge_cache()
    clear_symbols()
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-q1-2022-audio-file-short-clip.yaml"))
    responses._add_from_file(file_path=data_path("msft-company-events.yaml"))
    ##
    company = get_company("msft")
    file_name = company.download_audio_file(event=EarningsEvent(year=2022, quarter=1))
    #
    assert os.path.exists(file_name)
    assert os.path.getsize(file_name) > 0


def test_download_audio_file_missing_params_raises_value_error():
    ##
    purge_cache()
    clear_symbols()
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    ##
    company = get_company("msft")
    with pytest.raises(ValueError):
        company.download_audio_file()
