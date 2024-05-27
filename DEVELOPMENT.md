# Development

TODO: Add rye installation instructions.

This project uses Rye: https://rye.astral.sh/


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
