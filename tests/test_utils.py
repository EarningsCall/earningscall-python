from earningscall.utils import configure_sane_logging, enable_debug_logs, project_file_path


def test_project_file_path_tests_dir():
    project_file_path("tests", None)


def test_enable_debug_logs():
    enable_debug_logs()


def test_configure_sane_logging():
    configure_sane_logging()
