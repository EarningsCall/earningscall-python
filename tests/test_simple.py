import responses
import requests
# from responses import _recorder


@responses.activate
def test_simple():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  json={'error': 'not found'}, status=404)

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.text == '{"error": "not found"}'


# @_recorder.record(file_path="symbols.yaml")
# def test_save_symbols_v1():
#     requests.get("https://earningscall.biz/symbols.txt")
#
#
# @_recorder.record(file_path="symbols-v2.yaml")
# def test_save_symbols_v1():
#     requests.get("https://earningscall.biz/symbols-v2.txt")
