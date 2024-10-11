import logging
import os
import sys


def get_value_or_default(key: str, default: any, **kwargs):
    """
    returns kwargs value or default
        if key is in kwargs
    or
        default value
    """
    return kwargs[key] if key in kwargs else default


def load_test_logger(level=logging.INFO):
    test_logger = logging.getLogger()
    test_logger.setLevel(level=level)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.formatter = logging.Formatter(
        "::> %(name)s - %(levelname)s - %(message)s"
    )
    test_logger.handlers.clear()
    test_logger.addHandler(console_handler)


def register_modules(file: str, *paths):
    """
    Register modules in sys path.
    If it is already registered, it will be skipped

    Args:
        file: __file__
        paths: 'src', 'tools', 'module1'
    """
    src_dir = os.path.dirname(os.path.abspath(file))
    if not src_dir in sys.path:
        sys.path.insert(0, src_dir)

    for name in paths:
        tools_dir = os.path.join(src_dir, name)
        if not tools_dir in sys.path:
            sys.path.insert(0, tools_dir)
