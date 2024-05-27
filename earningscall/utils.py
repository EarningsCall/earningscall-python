import logging
import os
import pathlib

import earningscall


def project_file_path(base_dir, file_name):
    result = os.path.join(pathlib.Path(earningscall.__file__).resolve().parent.parent, base_dir)
    if file_name is None:
        return result
    return os.path.join(result, file_name)


def data_path(file_name=None):
    return project_file_path("tests/data", file_name)


def enable_debug_logs():
    logging.basicConfig(level=logging.DEBUG)
