import responses

from earningscall import get_company
from earningscall.utils import data_path


# Uncomment following code to generate msft-transcript-response.yaml file
#
# from responses import _recorder
# @_recorder.record(file_path="msft-transcript-response.yaml")
# def test_save_symbols_v1():
#     requests.get("https://v2.api.earningscall.biz/transcript?apikey=demo&exchange=NASDAQ&symbol=MSFT&year=2023&quarter=1")


@responses.activate
def test_get_demo_company():
    ##
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
    ##
    company = get_company("msft")
    ##
    transcript = company.get_transcript(year=2023, quarter=1)
    assert transcript.text[:100] == ('Greetings, and welcome to the Microsoft Fiscal Year 2023 First Quarter Earnings '
                                     'Conference Call. At ')


# @responses.activate
# def test_get_non_demo_company():
#     ##
#     responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
#     # responses._add_from_file(file_path=data_path("msft-transcript-response.yaml"))
#     ##
#     company = get_company("nvda")
#     ##
#     transcript = company.get_transcript(year=2023, quarter=1)
#     assert transcript.text[:100] == ('Greetings, and welcome to the Microsoft Fiscal Year 2023 First Quarter Earnings '
#                                      'Conference Call. At ')
