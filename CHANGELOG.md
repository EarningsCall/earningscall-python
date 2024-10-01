## Release `0.0.18` - 2024-10-01

* Add Download Audio File Feature: add `download_audio_file` function to the `Company` class.
* Add "LSE" to the list of exchanges.

## Release `0.0.17` - 2024-08-04

* Remove apikey from the ignored parameters list.

When `apikey=demo`, the API will return different results.  If we change
apikey to some other value, then the old result from when `apikey=demo`
would be returned.  This is incorrect.

## Release `0.0.16` - 2024-06-12
* Bump version number.

## Release `0.0.15` - 2024-06-12
* Remove `dataclasses` as a project dependency.  It is built directly into Python.

## Release `0.0.14` - 2024-06-08
* Add caching to improve client performance.
* Add `company_info` attribute in `Company` class.
