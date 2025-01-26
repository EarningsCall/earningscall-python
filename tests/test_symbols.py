import pytest
import responses

import earningscall
from earningscall.api import API_BASE, purge_cache
from earningscall.symbols import Symbols, CompanyInfo
from earningscall.utils import data_path


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    earningscall.api_key = None
    purge_cache()
    yield  # this is where the testing happens
    # Teardown : fill with any logic you want
    earningscall.api_key = None


@responses.activate
def test_load_symbols_txt_v2():
    ##
    responses.patch(API_BASE)
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
    assert responses.calls[0].request.url == "https://v2.api.earningscall.biz/symbols-v2.txt?apikey=demo"
    ##
    symbols.remove_exchange_symbol("NASDAQ_AAPL")
    with pytest.raises(KeyError):
        symbols.get_exchange_symbol("NASDAQ_AAPL")


@responses.activate
def test_load_symbols_txt_v2_missing_edge_cases():
    ##
    responses.patch(API_BASE)
    responses._add_from_file(file_path=data_path("symbols-v2-missing-edge-cases.yaml"))
    ##
    symbols = Symbols.load_txt_v2()
    ##
    assert len(symbols) == 4
    _symbol = symbols.get_exchange_symbol("UNKNOWN_A")
    assert _symbol.name == "Agilent Technologies, Inc."
    assert _symbol.exchange == "UNKNOWN"
    assert _symbol.sector == "Unknown"
    assert _symbol.industry == "Unknown"
    _symbol = symbols.get_exchange_symbol("NASDAQ_AACG")
    assert _symbol.name == "ATA Creativity Global"
    assert _symbol.exchange == "NASDAQ"
    assert _symbol.sector == "Consumer Defensive"
    assert _symbol.industry == "Education & Training Services"
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://v2.api.earningscall.biz/symbols-v2.txt?apikey=demo"


def test_symbols_serialization_to_text_v2():
    ##
    _symbols = Symbols()
    _symbols.add(
        CompanyInfo(
            exchange="TSX",
            symbol="TLRY",
            name="Tilray, Inc",
            sector="Energy",
            industry="Electronic Gaming & Multimedia",
        )
    )
    _symbols.add(
        CompanyInfo(
            exchange="TSX",
            symbol="ACB",
            name="Aurora Cannabis Inc.",
            sector="Technology",
            industry="Electronic Gaming & Multimedia",
        )
    )
    _symbols.add(
        CompanyInfo(
            exchange="NASDAQ",
            symbol="HITI",
            name="High Tide Inc.",
            sector="Consumer Cyclical",
            industry="Electronic Gaming & Multimedia",
        )
    )
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


def test_symbols_serialization_v1():
    _symbols = Symbols()
    _symbols.add(CompanyInfo(exchange="TSX", symbol="TLRY", name="Tilray, Inc", sector="Energy", industry="Uranium"))
    _symbols.add(
        CompanyInfo(exchange="TSX", symbol="ACB", name="Aurora Cannabis Inc.", sector="Energy", industry="Uranium")
    )
    _symbols.add(
        CompanyInfo(exchange="NASDAQ", symbol="HITI", name="High Tide Inc.", sector="Energy", industry="Uranium")
    )
    ##
    result = _symbols.to_json()
    ##
    _deserialized_symbols = Symbols.from_json(result)
    assert len(_deserialized_symbols) == 3
    assert _deserialized_symbols.get_exchange_symbol("TSX_TLRY").name == "Tilray, Inc"
    assert _deserialized_symbols.get_exchange_symbol("TSX_TLRY").sector == "Energy"
    assert _deserialized_symbols.get_exchange_symbol("TSX_TLRY").industry == "Uranium"
    assert _deserialized_symbols.get_exchange_symbol("TSX_ACB").name == "Aurora Cannabis Inc."
    assert _deserialized_symbols.get_exchange_symbol("NASDAQ_HITI").name == "High Tide Inc."


def test_exchanges_in_order():
    assert earningscall.symbols.EXCHANGES_IN_ORDER == [
        "NYSE",
        "NASDAQ",
        "AMEX",
        "TSX",
        "TSXV",
        "OTC",
        "LSE",
        "CBOE",
        "STO",
    ]
