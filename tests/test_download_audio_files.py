import os

import pytest
import responses

from earningscall import get_company
from earningscall.api import purge_cache
from earningscall.event import EarningsEvent
from earningscall.symbols import clear_symbols
from earningscall.utils import data_path


# Uncomment and run following code to generate msft-transcript-response.yaml file
#
# @_recorder.record(file_path="msft-q1-2024-audio-file.yaml")
# def test_save_symbols_v1():
#     # requests.get("https://v2.api.earningscall.biz/audio?apikey=demo&exchange=NASDAQ&symbol=MSFT&year=2024&quarter=1")
#     # requests.get("https://cca-test-webcasts.s3.amazonaws.com/assets/2020-q4-sgh-cut-with-music.mp3")
#     # requests.get("https://cdn.pixabay.com/download/audio/2024/03/16/audio_9a81feecdc.mp3?filename=short-1-slow-196420.mp3")
#     requests.get("https://cdn.pixabay.com/download/audio/2023/04/04/audio_7f705b3235.mp3?filename=teddy-short-comedy-audio-logo-happy-cartoony-intro-outro-music-145155.mp3")


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
