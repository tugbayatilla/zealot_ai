import pytest
import logging
from ally_ai_core.Logs import logstep
import asyncio

@pytest.fixture(autouse=True)
def configure_logging():
    """Configure logging for the tests."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
    yield
    # Reset logging configuration after tests if needed
    logging.getLogger().handlers = []

def test_logstep_sync_function(caplog):
    @logstep("Test Sync", show_start=True, show_finish=True)
    def add(a, b):
        return a + b

    with caplog.at_level(logging.INFO):
        result = add(2, 3)
    
    assert result == 5

    # Check that start and finish logs are present
    assert "Test Sync - Starting add with args: (2, 3), kwargs: {}" in caplog.text
    assert "Test Sync - Finished add with result: 5" in caplog.text

def test_logstep_sync_function_no_start(caplog):
    @logstep("Test Sync No Start", show_start=False, show_finish=True)
    def multiply(a, b):
        return a * b

    with caplog.at_level(logging.INFO):
        result = multiply(4, 5)
    
    assert result == 20

    # Start log should not be present
    assert "Test Sync No Start - Starting multiply" not in caplog.text
    # Finish log should be present
    assert "Test Sync No Start - Finished multiply with result: 20" in caplog.text

def test_logstep_sync_function_no_finish(caplog):
    @logstep("Test Sync No Finish", show_start=True, show_finish=False)
    def subtract(a, b):
        return a - b

    with caplog.at_level(logging.INFO):
        result = subtract(10, 4)
    
    assert result == 6

    # Start log should be present
    assert "Test Sync No Finish - Starting subtract with args: (10, 4), kwargs: {}" in caplog.text
    # Finish log should not be present
    assert "Test Sync No Finish - Finished subtract" not in caplog.text

def test_logstep_async_function(caplog):
    @logstep("Test Async", show_start=True, show_finish=True)
    async def async_add(a, b):
        await asyncio.sleep(0.1)
        return a + b

    async def run_test():
        with caplog.at_level(logging.INFO):
            result = await async_add(5, 7)
        assert result == 12
        assert "Test Async - Starting async_add with args: (5, 7), kwargs: {}" in caplog.text
        assert "Test Async - Finished async_add with result: 12" in caplog.text

    asyncio.run(run_test())

@pytest.mark.asyncio
async def test_logstep_async_function_asyncio_marker(caplog):
    @logstep("Test Async Marker", show_start=True, show_finish=True)
    async def async_multiply(a, b):
        await asyncio.sleep(0.1)
        return a * b

    with caplog.at_level(logging.INFO):
        result = await async_multiply(3, 4)
    
    assert result == 12
    assert "Test Async Marker - Starting async_multiply with args: (3, 4), kwargs: {}" in caplog.text
    assert "Test Async Marker - Finished async_multiply with result: 12" in caplog.text

def test_logstep_logging_level(caplog):
    @logstep("Test Logging Level", level=logging.DEBUG, show_start=True, show_finish=True)
    def divide(a, b):
        return a / b

    with caplog.at_level(logging.DEBUG):
        result = divide(10, 2)
    
    assert result == 5
    assert "Test Logging Level - Starting divide with args: (10, 2), kwargs: {}" in caplog.text
    assert "Test Logging Level - Finished divide with result: 5" in caplog.text

def test_logstep_function_arguments(caplog):
    @logstep("Test Args Logging", show_start=True, show_finish=True)
    def concatenate(a, b, sep=" "):
        return f"{a}{sep}{b}"

    with caplog.at_level(logging.INFO):
        result = concatenate("Hello", "World", sep=", ")
    
    assert result == "Hello, World"
    assert "Test Args Logging - Starting concatenate with args: ('Hello', 'World'), kwargs: {'sep': ', '}" in caplog.text
    assert "Test Args Logging - Finished concatenate with result: Hello, World" in caplog.text

def test_logstep_no_logging(caplog):
    @logstep("Test No Logging", show_start=False, show_finish=False)
    def noop():
        return "No Operation"

    with caplog.at_level(logging.INFO):
        result = noop()
    
    assert result == "No Operation"
    # No logs should be present
    assert "Test No Logging - Starting noop" not in caplog.text
    assert "Test No Logging - Finished noop" not in caplog.text
    
