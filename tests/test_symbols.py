import responses

from earningscall.api import API_BASE
from earningscall.symbols import Symbols, CompanyInfo
from earningscall.utils import data_path


@responses.activate
def test_load_symbols_txt_v2():
    ##
    responses.patch(API_BASE)
    print("symbols path")
    print(data_path("symbols-v2.yaml"))
    responses._add_from_file(file_path=data_path("symbols-v2.yaml"))
    ##
    symbols = Symbols.load_txt_v2()
    ##
    assert len(symbols) == 5807
    _symbol = symbols.get_exchange_symbol("NASDAQ_AAPL")
    assert _symbol.name == "Apple Inc."
    assert _symbol.exchange == "NASDAQ"
    assert _symbol.sector == "Technology"
    assert _symbol.industry == "Consumer Electronics"
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://v2.api.earningscall.biz/symbols-v2.txt"


def test_symbols_serialization_to_text_v2():
    ##
    _symbols = Symbols()
    _symbols.add(CompanyInfo(exchange="TSX", symbol="TLRY", name="Tilray, Inc", sector="Energy",
                             industry="Electronic Gaming & Multimedia"))
    _symbols.add(CompanyInfo(exchange="TSX", symbol="ACB", name="Aurora Cannabis Inc.", sector="Technology",
                             industry="Electronic Gaming & Multimedia"))
    _symbols.add(CompanyInfo(exchange="NASDAQ", symbol="HITI", name="High Tide Inc.", sector="Consumer Cyclical",
                             industry="Electronic Gaming & Multimedia"))
    ##
    result = _symbols.to_txt_v2()
    ##
    _deserialized_symbols = Symbols.from_txt_v2(result)
    assert len(_deserialized_symbols) == 3
    assert _deserialized_symbols.get_exchange_symbol("TSX_TLRY").name == "Tilray, Inc"
    assert _deserialized_symbols.get_exchange_symbol("TSX_TLRY").exchange == "TSX"
    assert _deserialized_symbols.get_exchange_symbol("TSX_TLRY").sector == "Energy"
    assert _deserialized_symbols.get_exchange_symbol("TSX_TLRY").industry == "Electronic Gaming & Multimedia"
    assert _deserialized_symbols.get_exchange_symbol("TSX_ACB").name == "Aurora Cannabis Inc."
    assert _deserialized_symbols.get_exchange_symbol("TSX_ACB").sector == "Technology"
    assert _deserialized_symbols.get_exchange_symbol("TSX_ACB").industry == "Electronic Gaming & Multimedia"
    assert _deserialized_symbols.get_exchange_symbol("NASDAQ_HITI").name == "High Tide Inc."
