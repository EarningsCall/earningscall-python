# Development

TODO: Add hatch installation instructions.


### Saving Server-Side Responses for a Mocked Unit test

You can use the following test code to save responses from the server as a .YAML file:

```python
import requests

from responses import _recorder

@_recorder.record(file_path="symbols.yaml")
def test_save_symbols_v1():
    requests.get("https://earningscall.biz/symbols.txt")


@_recorder.record(file_path="symbols-v2.yaml")
def test_save_symbols_v1():
    requests.get("https://earningscall.biz/symbols-v2.txt")
```



### Publishing a new Version to PyPI

Assuming you want to publish version 0.0.7, first, make your changes, then run the commands:

```sh
git commit -a
git tag v0.0.7
git push --atomic origin master v0.0.7
```



### Manually Running Scripts

Use the library to get a single transcript from the API:

```shell
python -m scripts.get_single_transcript
```

Get all transcripts for a company:

```shell
python -m scripts.get_all_company_transcripts
```

List all companies:

```shell
python -m scripts.list_companies
```
