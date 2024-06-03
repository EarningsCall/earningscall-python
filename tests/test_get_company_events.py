import responses

from earningscall import get_company
from earningscall.api import purge_cache
from earningscall.symbols import clear_symbols
from earningscall.utils import data_path


# Uncomment and run following code to generate msft-transcript-response.yaml file
#
# from responses import _recorder
# @_recorder.record(file_path="msft-company-events.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.earningscall.biz/events?apikey=demo&exchange=NASDAQ&symbol=MSFT")
#


@responses.activate
def test_get_demo_company():
    ##
    purge_cache()
    clear_symbols()
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
    responses._add_from_file(file_path=data_path("msft-company-events.yaml"))
    ##
    company = get_company("msft")
    events = company.events()
    ##
    assert len(events) == 20
    assert events[0].year == 2024
    assert events[0].quarter == 3
