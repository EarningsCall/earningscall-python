import time

import responses

from earningscall.api import get_sp500_companies_txt_file, cached_urls, purge_cache


@responses.activate
def test_load_sp500_tickers():
    purge_cache()
    assert len(cached_urls()) == 0
    ##
    responses.add(
        responses.GET,
        "https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo",
        body="AAPL\nMSFT\nTSLA",
        status=200,
        adding_headers={
            "Cache-Control": "public, max-age=3",  # Allow client to cache for 3 seconds
        },
    )
    responses.add(
        responses.GET,
        "https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo",
        body="AAPL\nMSFT\nTSLA\nNEWCOMPANY",
        status=200,
        adding_headers={
            "cache-control": "public, max-age=30",  # Allow client to cache for 30 seconds
        },
    )
    ##
    sp500_raw_text = get_sp500_companies_txt_file()
    ##
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo"
    assert cached_urls() == ["https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo"]
    tickers = [ticker_symbol for ticker_symbol in sp500_raw_text.split("\n")]
    assert tickers == ["AAPL", "MSFT", "TSLA"]
    ##
    # Request a second time, should serve out of cache
    ##
    sp500_raw_text = get_sp500_companies_txt_file()
    ##
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo"
    urls = cached_urls()
    assert urls == ["https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo"]
    tickers = [ticker_symbol for ticker_symbol in sp500_raw_text.split("\n")]
    assert tickers == ["AAPL", "MSFT", "TSLA"]
    ##
    # Wait enough time for cache entry to expire
    ##
    time.sleep(4)
    ##
    sp500_raw_text = get_sp500_companies_txt_file()
    ##
    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == "https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo"
    assert responses.calls[1].request.url == "https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo"
    assert cached_urls() == ["https://v2.api.earningscall.biz/symbols/sp500.txt?apikey=demo"]
    tickers = [ticker_symbol for ticker_symbol in sp500_raw_text.split("\n")]
    assert tickers == ["AAPL", "MSFT", "TSLA", "NEWCOMPANY"]
