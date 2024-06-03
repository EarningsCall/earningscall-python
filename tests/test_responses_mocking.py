import requests
import responses


# NOTE: this test is only testing the behavior of the responses library, and therefore it is not testing any
#       code in earningscall at all.


@responses.activate
def test_load_sp500_tickers():
    ##
    responses.add(
        responses.GET,
        "http://www.example.com",
        body="first response",
        status=200,
    )
    responses.add(
        responses.GET,
        "http://www.example.com",
        body="second response",
        status=200,
    )
    ##
    first_response = requests.get("http://www.example.com").text
    assert first_response == "first response"
    second_response = requests.get("http://www.example.com").text
    assert second_response == "second response"
    # It just returns last response over and over again.
    second_response = requests.get("http://www.example.com").text
    assert second_response == "second response"
    second_response = requests.get("http://www.example.com").text
    assert second_response == "second response"
    ##
