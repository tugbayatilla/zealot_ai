# test_timed_decorator.py

import pytest
from unittest.mock import patch
import re
from ally_ai_core.Decorators import timed
import logging

# Sample functions to be decorated
@timed
def add(a, b):
    """Adds two numbers."""
    return a + b

@timed
def greet(name="World"):
    """Greets a person."""
    return f"Hello, {name}!"

@timed
def sleep_func(duration):
    """Sleeps for a specified duration."""
    from time import sleep
    sleep(duration)
    return "Slept"

# Test Cases

def test_timed_add(caplog):
    with caplog.at_level(logging.INFO):
        result = add(2, 3)
        assert result == 5

        # Check that a log message was emitted
        assert any("add took" in record.message for record in caplog.records)

        # Optionally, verify the log message format using regex
        pattern = r"add took \d+\.\d{6} seconds to finish"
        assert any(re.match(pattern, record.message) for record in caplog.records), \
            "No log message matches the expected pattern."

def test_timed_greet(caplog):
    with caplog.at_level(logging.INFO):
        greeting = greet(name="Alice")
        assert greeting == "Hello, Alice!"

        # Check that a log message was emitted
        assert any("greet took" in record.message for record in caplog.records)

        # Verify the log message format using regex
        pattern = r"greet took \d+\.\d{6} seconds to finish"
        assert any(re.match(pattern, record.message) for record in caplog.records), \
            "No log message matches the expected pattern."

def test_timed_sleep_func(caplog):
    with patch('time.time') as mock_time:
        mock_time.side_effect = [100.0, 105.0]  # Simulate 5 seconds elapsed

        with patch('time.sleep', return_value=None):
            with caplog.at_level(logging.INFO):
                result = sleep_func(5)
                assert result == "Slept"

                # Check that a log message was emitted
                assert any("sleep_func took" in record.message for record in caplog.records)

                # Verify the log message format using regex
                pattern = r"sleep_func took \d+\.\d{6} seconds to finish"
                assert any(re.match(pattern, record.message) for record in caplog.records), \
                    "No log message matches the expected pattern."

def test_preserve_metadata():
    assert add.__name__ == "add"
    assert greet.__name__ == "greet"
    assert sleep_func.__name__ == "sleep_func"

    assert add.__doc__ == "Adds two numbers."
    assert greet.__doc__ == "Greets a person."
    assert sleep_func.__doc__ == "Sleeps for a specified duration."

def test_handle_no_arguments(caplog):
    @timed
    def say_hi():
        """Says hi."""
        return "Hi!"

    with patch('time.time') as mock_time:
        mock_time.side_effect = [200.0, 200.0]  # Simulate 0 seconds elapsed

        with caplog.at_level(logging.INFO):
            result = say_hi()
            assert result == "Hi!"

            # Check that a log message was emitted
            assert any("say_hi took" in record.message for record in caplog.records)

            # Verify the log message format using regex
            pattern = r"say_hi took \d+\.\d{6} seconds to finish"
            assert any(re.match(pattern, record.message) for record in caplog.records), \
                "No log message matches the expected pattern."

def test_handle_various_arguments(caplog):
    @timed
    def concatenate(*args, **kwargs):
        """Concatenates arguments with a separator."""
        sep = kwargs.get('sep', ' ')
        return sep.join(args)

    with patch('time.time') as mock_time:
        mock_time.side_effect = [300.0, 300.0]  # Simulate 0 seconds elapsed

        with caplog.at_level(logging.INFO):
            result = concatenate("Hello", "World", sep=", ")
            assert result == "Hello, World"

            # Check that a log message was emitted
            assert any("concatenate took" in record.message for record in caplog.records)

            # Verify the log message format using regex
            pattern = r"concatenate took \d+\.\d{6} seconds to finish"
            assert any(re.match(pattern, record.message) for record in caplog.records), \
                "No log message matches the expected pattern."