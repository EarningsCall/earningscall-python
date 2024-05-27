import pytest
import responses

from earningscall import get_company
from earningscall.errors import InsufficientApiAccessError
from earningscall.symbols import clear_symbols
from earningscall.utils import data_path


# Uncomment and run following code to generate msft-transcript-response.yaml file
#
# from responses import _recorder
# @_recorder.record(file_path="msft-transcript-response.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.earningscall.biz/transcript?apikey=demo&exchange=NASDAQ&symbol=MSFT&year=2023&quarter=1")


@responses.activate
def test_get_demo_company():
    ##
    clear_symbols()
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
    ##
    company = get_company("msft")
    ##
    transcript = company.get_transcript(year=2023, quarter=1)
    assert transcript.text[:100] == ('Greetings, and welcome to the Microsoft Fiscal Year 2023 First Quarter Earnings '
                                     'Conference Call. At ')


# Uncomment and run following code to generate demo-symbols-v2.yaml file
#
# import requests
#
# from responses import _recorder
#
#
# @_recorder.record(file_path="demo-symbols-v2.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.earningscall.biz/symbols-v2.txt?apikey=demo")


@responses.activate
def test_get_non_demo_company():
    ##
    clear_symbols()
    responses._add_from_file(file_path=data_path("demo-symbols-v2.yaml"))
    ##
    with pytest.raises(InsufficientApiAccessError):
        get_company("nvda")
