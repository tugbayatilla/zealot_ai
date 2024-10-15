import pytest
import logging
from unittest.mock import patch
import asyncio
import re

from ally_ai_core.decorators import logged


@logged("Test sync function", level=logging.INFO)
def sample_sync_func(x, y):
    return x + y


@logged("Test sync function with exception", level=logging.INFO)
def sample_sync_func_with_exception(x, y):
    raise ValueError("Test sync exception")


@pytest.mark.asyncio
@logged("Test async function", level=logging.INFO)
async def sample_async_func(x, y):
    await asyncio.sleep(0.1)  # Simulating async work
    return x + y


@pytest.mark.asyncio
@logged("Test async function with exception", level=logging.INFO)
async def sample_async_func_with_exception(x, y):
    await asyncio.sleep(0.1)
    raise ValueError("Test async exception")


# Helper function to assert log messages with dynamic ID
def assert_log_contains(mock_log, expected_message_part):
    log_message = " ".join([call[0][1] for call in mock_log.call_args_list])
    assert re.search(expected_message_part, log_message)


def assert_ex_info_contains(ex_info, expected_message_part):
    log_message = " ".join([call for call in ex_info.value.args])
    assert re.search(expected_message_part, log_message)


# Test case for sync function
def test_logged_sync_func():
    with patch("logging.log") as mock_log:
        result = sample_sync_func(2, 3)
        assert result == 5

        # Ensure logging for start and finish (ignore dynamic ID)
        assert_log_contains(
            mock_log,
            r"Test sync function - Starting\(\d+\) \*sample_sync_func\* with args: \(2, 3\), kwargs: {}",
        )
        assert_log_contains(
            mock_log,
            r"Test sync function - Finished\(\d+\) \*sample_sync_func\* with result: 5",
        )


# Test case for sync function raising exception
def test_logged_sync_func_with_exception():
    with patch("logging.log") as mock_log:
        with pytest.raises(ValueError, match="Test sync exception"):
            sample_sync_func_with_exception(2, 3)

        # Ensure logging for start and exception (ignore dynamic ID)
        assert_log_contains(
            mock_log,
            r"Test sync function with exception - Starting\(\d+\) \*sample_sync_func_with_exception\* with args: \(2, 3\), kwargs: {}",
        )


# Test case for async function
@pytest.mark.asyncio
async def test_logged_async_func():
    with patch("logging.log") as mock_log:
        result = await sample_async_func(4, 5)
        assert result == 9

        # Ensure logging for start and finish (ignore dynamic ID)
        assert_log_contains(
            mock_log,
            r"Test async function - Starting\(\d+\) \*sample_async_func\* with args: \(4, 5\), kwargs: {}",
        )
        assert_log_contains(
            mock_log,
            r"Test async function - Finished\(\d+\) \*sample_async_func\* with result: 9",
        )


# Test case for async function raising exception
@pytest.mark.asyncio
async def test_logged_async_func_with_exception():
    with patch("logging.log") as mock_log:
        with pytest.raises(ValueError, match="Test async exception") as exc_info:
            await sample_async_func_with_exception(4, 5)

        # Ensure logging for start and exception (ignore dynamic ID)
        assert_log_contains(
            mock_log,
            r"Test async function with exception - Starting\(\d+\) \*sample_async_func_with_exception\* with args: \(4, 5\), kwargs: {}",
        )
