# tests/test_log_step.py

import pytest
import logging
import re
import asyncio
from ally_ai_core.context_managers import logged_step, alogged_step

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------
# Helper Functions for Testing
# ---------------------------


# Sample synchronous function
def process_data(data):
    with logged_step("Process Data"):
        # Simulate data processing
        processed = data.upper()
        return processed


def process_data_custom(data):
    with logged_step("Custom Process", level=logging.DEBUG, raise_exception=False):
        # Simulate data processing
        processed = data.lower()
        return processed


def faulty_process():
    with logged_step("Faulty Process"):
        raise ValueError("An error occurred during processing")


# Sample asynchronous function
async def async_reverse(data):
    async with alogged_step("Async Process Data"):
        # Simulate async data processing
        await asyncio.sleep(0.1)
        return data[::-1]


async def async_faulty_process():
    async with alogged_step("Async Faulty Process"):
        await asyncio.sleep(0.1)
        raise RuntimeError("Async error occurred")


# Function with no return
def void_function():
    with logged_step("Void Function"):
        pass


# ---------------------------
# Test Cases
# ---------------------------


# 1. Test synchronous function without exceptions
def test_log_step_process_data(caplog):
    with caplog.at_level(logging.INFO):
        result = process_data("Test Data")
        assert result == "TEST DATA", "process_data should convert data to uppercase"

        # Check start and finish logs
        assert any(
            "Step(Process Data): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the step"
        assert any(
            "Step(Process Data): Executed." in record.message
            for record in caplog.records
        ), "No log message for finishing the step"


# 2. Test synchronous function with custom logging level and raise_exception=False
def test_log_step_process_data_custom(caplog):
    with caplog.at_level(logging.DEBUG):
        result = process_data_custom("Test Data")
        assert (
            result == "test data"
        ), "process_data_custom should convert data to lowercase"

        # Check start and finish logs at DEBUG level
        assert any(
            "Step(Custom Process): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the custom step"
        assert any(
            "Step(Custom Process): Executed." in record.message
            for record in caplog.records
        ), "No log message for finishing the custom step"


# 3. Test synchronous function that raises an exception
def test_log_step_faulty_process(caplog):
    with caplog.at_level(logging.INFO):
        with pytest.raises(ValueError, match="An error occurred during processing"):
            faulty_process()

        # Check start and error logs
        assert any(
            "Step(Faulty Process): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the faulty step"
        assert any(
            "Step(Faulty Process): Failed! Reason: An error occurred during processing"
            in record.message
            for record in caplog.records
        ), "No log message for failed step"


# 4. Test asynchronous function without exceptions
@pytest.mark.asyncio
async def test_async_log_step_process_data(caplog):
    with caplog.at_level(logging.INFO):
        result = await async_reverse("Async Data")
        assert result == "ataD cnysA", "async_process_data should reverse the data"

        # Check start and finish logs
        assert any(
            "Step(Async Process Data): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the async step"
        assert any(
            "Step(Async Process Data): Executed." in record.message
            for record in caplog.records
        ), "No log message for finishing the async step"


# 5. Test asynchronous function that raises an exception
@pytest.mark.asyncio
async def test_async_log_step_faulty_process(caplog):
    with caplog.at_level(logging.INFO):
        with pytest.raises(RuntimeError, match="Async error occurred"):
            await async_faulty_process()

        # Check start and error logs
        assert any(
            "Step(Async Faulty Process): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the async faulty step"
        assert any(
            "Step(Async Faulty Process): Failed! Reason: Async error occurred"
            in record.message
            for record in caplog.records
        ), "No log message for failed async step"


# 6. Test context manager on a function that returns None
def test_log_step_void_function(caplog):
    with caplog.at_level(logging.INFO):
        result = void_function()
        assert result is None, "void_function should return None"

        # Check start and finish logs
        assert any(
            "Step(Void Function): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the void step"
        assert any(
            "Step(Void Function): Executed." in record.message
            for record in caplog.records
        ), "No log message for finishing the void step"


# 7. Test context manager with raise_exception=False
def test_log_step_no_raise_exception(caplog):
    with caplog.at_level(logging.INFO):
        # Attempt to raise an exception without re-raising
        try:
            with logged_step("Faulty Process", raise_exception=False):
                raise ValueError("An error occurred during processing")
        except ValueError:
            # Exception should not be raised since raise_exception=False
            pytest.fail("Exception was raised despite raise_exception=False")

        # Check start and error logs
        assert any(
            "Step(Faulty Process): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the faulty step"
        assert any(
            "Step(Faulty Process): Failed! Reason: An error occurred during processing"
            in record.message
            for record in caplog.records
        ), "No log message for failed step"


# 8. Test context manager with nested context managers
def test_log_step_nested(caplog):
    with caplog.at_level(logging.INFO):
        with logged_step("Outer Step"):
            with logged_step("Inner Step"):
                pass

        # Check logs for both steps
        assert any(
            "Step(Outer Step): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the outer step"
        assert any(
            "Step(Outer Step): Executed." in record.message for record in caplog.records
        ), "No log message for finishing the outer step"

        assert any(
            "Step(Inner Step): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the inner step"
        assert any(
            "Step(Inner Step): Executed." in record.message for record in caplog.records
        ), "No log message for finishing the inner step"


# 9. Test context manager with empty name
def test_log_step_empty_name(caplog):
    with caplog.at_level(logging.INFO):
        with logged_step(""):
            pass

        # Check logs with empty step name
        assert any(
            "Step(): Executing..." in record.message for record in caplog.records
        ), "No log message for starting the step with empty name"
        assert any(
            "Step(): Executed." in record.message for record in caplog.records
        ), "No log message for finishing the step with empty name"


# 10. Test context manager with complex name containing special characters
def test_log_step_complex_name(caplog):
    with caplog.at_level(logging.INFO):
        with logged_step("Complex-Step_123!"):
            pass

        # Check logs with complex step name
        assert any(
            "Step(Complex-Step_123!): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the complex step"
        assert any(
            "Step(Complex-Step_123!): Executed." in record.message
            for record in caplog.records
        ), "No log message for finishing the complex step"


# 11. Test asynchronous context manager with exceptions
@pytest.mark.asyncio
async def test_async_log_step_with_exception(caplog):
    with caplog.at_level(logging.INFO):
        try:
            async with alogged_step("Async Faulty Step"):
                raise RuntimeError("Async runtime error")
        except RuntimeError:
            pass

        # Check logs
        assert any(
            "Step(Async Faulty Step): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the async faulty step"
        assert any(
            "Step(Async Faulty Step): Failed! Reason: Async runtime error"
            in record.message
            for record in caplog.records
        ), "No log message for failed async step"


# 12. Test asynchronous context manager with raise_exception=False
@pytest.mark.asyncio
async def test_async_log_step_no_raise_exception(caplog):
    with caplog.at_level(logging.INFO):
        # Attempt to raise an exception without re-raising
        try:
            async with alogged_step("Async Faulty Step", raise_exception=False):
                raise RuntimeError("Async runtime error")
        except RuntimeError:
            pytest.fail("Exception was raised despite raise_exception=False")

        # Check logs
        assert any(
            "Step(Async Faulty Step): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the async faulty step"
        assert any(
            "Step(Async Faulty Step): Failed! Reason: Async runtime error"
            in record.message
            for record in caplog.records
        ), "No log message for failed async step"


# 13. Test multiple exceptions raised by the context manager
def test_log_step_multiple_exceptions(caplog):
    with caplog.at_level(logging.INFO):
        # First exception
        with pytest.raises(ValueError, match="First error"):
            with logged_step("Multiple Exceptions"):
                raise ValueError("First error")

        # Second exception
        with pytest.raises(TypeError, match="Second error"):
            with logged_step("Multiple Exceptions"):
                raise TypeError("Second error")

        # Check logs for both exceptions
        assert any(
            "Step(Multiple Exceptions): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the multiple exceptions step"
        assert any(
            "Step(Multiple Exceptions): Failed! Reason: First error" in record.message
            for record in caplog.records
        ), "No log message for first exception"
        assert any(
            "Step(Multiple Exceptions): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the second exception step"
        assert any(
            "Step(Multiple Exceptions): Failed! Reason: Second error" in record.message
            for record in caplog.records
        ), "No log message for second exception"


# 14. Test context manager with functions that have side effects
counter = 0


def increment_counter():
    global counter
    with logged_step("Increment Counter"):
        global counter
        counter += 1


def test_log_step_side_effect(caplog):
    global counter
    counter = 0  # Reset counter
    with caplog.at_level(logging.INFO):
        increment_counter()
        assert counter == 1, "Counter should be incremented to 1"

        # Check log messages
        assert any(
            "Step(Increment Counter): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the counter increment step"
        assert any(
            "Step(Increment Counter): Executed." in record.message
            for record in caplog.records
        ), "No log message for finishing the counter increment step"


# 15. Test context manager with functions returning complex objects
def return_complex_object():
    with logged_step("Return Complex Object"):
        return {"key": "value", "number": 42}


def test_log_step_return_complex_object(caplog):
    with caplog.at_level(logging.INFO):
        result = return_complex_object()
        assert result == {
            "key": "value",
            "number": 42,
        }, "Function should return the expected complex object"

        # Check log messages
        assert any(
            "Step(Return Complex Object): Executing..." in record.message
            for record in caplog.records
        ), "No log message for starting the return complex object step"
        assert any(
            "Step(Return Complex Object): Executed." in record.message
            for record in caplog.records
        ), "No log message for finishing the return complex object step"
