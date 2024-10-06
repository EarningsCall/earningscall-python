import os

import earningscall
import pytest
import responses

from earningscall import get_company
from earningscall.api import purge_cache
from earningscall.event import EarningsEvent
from earningscall.symbols import clear_symbols
from earningscall.utils import data_path


# Uncomment and run following code to generate msft-transcript-response.yaml file
#
# from responses import _recorder
# @_recorder.record(file_path="meta-q3-2024-not-found.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.alpha.earningscall.biz/audio?apikey=brocktest&exchange=NASDAQ&symbol=META&year=2024&quarter=3")


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    earningscall.api_key = None
    yield # this is where the testing happens
    # Teardown : fill with any logic you want
    earningscall.api_key = None


@responses.activate
def test_download_audio_file():
    ##
    earningscall.api_key = None
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
    earningscall.api_key = None
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
    earningscall.api_key = None
    purge_cache()
    clear_symbols()
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    ##
    company = get_company("msft")
    with pytest.raises(ValueError):
        company.download_audio_file()


# @responses.activate
# def test_download_audio_file_missing_from_server():
#     ##
#     earningscall.api_key = "foobar"
#     purge_cache()
#     clear_symbols()
#     responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
#     responses._add_from_file(file_path=data_path("meta-q3-2024-not-found.yaml"))
#     ##
#     company = get_company("meta")
#     output_file = company.download_audio_file(year=2024, quarter=3)
#     ##
#     assert output_file is None
