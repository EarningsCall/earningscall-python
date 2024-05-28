import logging
import os
import pathlib
import sys

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


LOG_FORMAT = "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)"


def configure_sane_logging(level=logging.DEBUG):
    # Manually set the following loggers to "INFO", since they tend to be VERY noisy, and when we are
    # debugging our own application, we only care about DEBUG logs from OUR application, not these libs.
    for name in ['urllib3']:
        logging.getLogger(name).setLevel(logging.INFO)
    logging.getLogger("filelock").setLevel(logging.WARNING)
    logging.basicConfig(level=level, stream=sys.stdout, format=LOG_FORMAT)
