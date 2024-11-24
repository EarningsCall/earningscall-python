## Release `0.0.23` - 2024-11-24

* Allow `None` for optional fields in SpeakerInfo data structure.
* Update logging format for API calls.
* Update logging level to DEBUG in unit tests.

## Release `0.0.22` - 2024-10-07

* Add **experimental feature**: Speaker Names and Titles

## Release `0.0.21` - 2024-10-07

* Bump version for PyPI release: updated README docs.

## Release `0.0.20` - 2024-10-07

* Bugfix: Fix importlib error.

## Release `0.0.19` - 2024-10-07

* Add Advanced Transcript Data structures (Beta: and subject to change in the future).
* Add additional client-side verification and parameter checking.
* Don't throw an exception when audio file is missing, just return `None`.
* Throw useful error in the case of not authorized to download Audio Files.
* Add additional unit test coverage.

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
