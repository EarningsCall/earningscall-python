# Changelog

## Release `1.2.1` - 2025-04-04

* Bugfix: handle case where Q&A section is missing from the transcript for level 4 transcription.

## Release `1.2.0` - 2025-02-12

* Add `get_calendar` function to get the calendar for a given date.

## Release `1.1.1` - 2025-01-26

* Modify default retry strategy to use 1s base delay and 10 max attempts (necessary for starter plan).
* Check for HTTP 401 Unauthorized status code from server and raise a helpful error message to the user.
* Update documentation and example scripts to reflect new retry configuration

## Release `1.1.0` - 2025-01-26

* Add backoff and retry logic to all API calls.
* Add tests for rate limiting.

## Release `1.0.2` - 2024-12-24

* Add STO exchange to the list of exchanges.

## Release `1.0.1` - 2024-12-20

* Update User-Agent string to standardized format used in the industry.

## Release `1.0.0` - 2024-12-16

* Release the first major version of EarningsCall.

## Release `0.0.26` - 2024-12-15

* Bump gh-action-sigstore-python to version 3.0.0.

## Release `0.0.25` - 2024-12-15

* Bump version for PyPI release (no changes to the code).

## Release `0.0.24` - 2024-12-15

* Remove extraneous debug logging.
* Add CBOE exchange to the list of exchanges.
* Support env variable "EARNINGSCALL_API_KEY" for key.

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
