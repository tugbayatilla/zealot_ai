import pytest
import logging
from ally_ai_core.Decorators import logstep
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
    
# tests/test_logstep_decorator.py

import pytest
import logging
import asyncio


# Sample synchronous functions
@logstep("Sync Operation")
def add(a, b):
    """Adds two numbers."""
    return a + b

@logstep("Sync Operation", level=logging.DEBUG, show_start=True, show_finish=True)
def multiply(a, b):
    """Multiplies two numbers."""
    return a * b

@logstep("Sync Operation")
def greet(name: str) -> str:
    """Greets a person."""
    return f"Hello, {name}!"

# Sample asynchronous functions
@logstep("Async Operation")
async def async_add(a, b):
    """Asynchronously adds two numbers."""
    await asyncio.sleep(0.1)
    return a + b

@logstep("Async Operation", level=logging.WARNING, show_start=True, show_finish=True)
async def async_multiply(a, b):
    """Asynchronously multiplies two numbers."""
    await asyncio.sleep(0.1)
    return a * b

# Function that raises an exception
@logstep("Exception Handling")
def divide(a, b):
    """Divides two numbers."""
    return a / b

@logstep("Exception Handling", level=logging.ERROR)
async def async_divide(a, b):
    """Asynchronously divides two numbers."""
    await asyncio.sleep(0.1)
    return a / b

# Function with various arguments
@logstep("Complex Function")
def complex_function(a, b=2, *args, **kwargs):
    """Function with various arguments."""
    return a + b + sum(args) + sum(kwargs.values())

# ---------------------------
# Test Cases
# ---------------------------

# 1. Test synchronous function without decorator arguments
def test_logstep_add(caplog):
    with caplog.at_level(logging.INFO):
        result = add(2, 3)
        assert result == 5, "add function should return the sum of two numbers"

        # Check that a log message was emitted
        assert any("Sync Operation - Starting add" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Starting add'"

        assert any("Sync Operation - Finished add with result: 5" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Finished add with result: 5'"

# 2. Test synchronous function with decorator arguments
def test_logstep_multiply(caplog):
    with caplog.at_level(logging.DEBUG):
        result = multiply(3, 4)
        assert result == 12, "multiply function should return the product of two numbers"

        # Check that a log message was emitted with the custom message
        assert any("Sync Operation - Starting multiply" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Starting multiply'"

        assert any("Sync Operation - Finished multiply with result: 12" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Finished multiply with result: 12'"

# 3. Test asynchronous function without decorator arguments
@pytest.mark.asyncio
async def test_logstep_async_add(caplog):
    with caplog.at_level(logging.INFO):
        result = await async_add(5, 7)
        assert result == 12, "async_add function should return the sum of two numbers"

        # Check that a log message was emitted
        assert any("Async Operation - Starting async_add" in record.message for record in caplog.records), \
            "No log message contains 'Async Operation - Starting async_add'"

        assert any("Async Operation - Finished async_add with result: 12" in record.message for record in caplog.records), \
            "No log message contains 'Async Operation - Finished async_add with result: 12'"

# 4. Test asynchronous function with decorator arguments
@pytest.mark.asyncio
async def test_logstep_async_multiply(caplog):
    with caplog.at_level(logging.WARNING):
        result = await async_multiply(6, 8)
        assert result == 48, "async_multiply function should return the product of two numbers"

        # Check that a log message was emitted with the custom message
        assert any("Async Operation - Starting async_multiply" in record.message for record in caplog.records), \
            "No log message contains 'Async Operation - Starting async_multiply'"

        assert any("Async Operation - Finished async_multiply with result: 48" in record.message for record in caplog.records), \
            "No log message contains 'Async Operation - Finished async_multiply with result: 48'"

# 5. Test decorator on function that raises an exception (synchronous)
def test_logstep_divide_exception(caplog):
    with caplog.at_level(logging.INFO):
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        # Even if the function raises, the decorator should log the exception
        assert any("Exception Handling - Starting divide" in record.message for record in caplog.records), \
            "No log message contains 'Exception Handling - Starting divide'"

        assert any("Exception Handling - divide raised an exception: division by zero" in record.message for record in caplog.records), \
            "No log message contains 'Exception Handling - divide raised an exception: division by zero'"

# 6. Test decorator on function that raises an exception (asynchronous)
@pytest.mark.asyncio
async def test_logstep_async_divide_exception(caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ZeroDivisionError):
            await async_divide(10, 0)

        # Even if the function raises, the decorator should log the exception
        assert any("Exception Handling - Starting async_divide" in record.message for record in caplog.records), \
            "No log message contains 'Exception Handling - Starting async_divide'"

        assert any("Exception Handling - async_divide raised an exception: division by zero" in record.message for record in caplog.records), \
            "No log message contains 'Exception Handling - async_divide raised an exception: division by zero'"

# 7. Test decorator preserves function metadata (__name__, __doc__)
def test_logstep_metadata():
    assert add.__name__ == "add", "Decorator should preserve the function name"
    assert add.__doc__ == "Adds two numbers.", "Decorator should preserve the function docstring"

    assert multiply.__name__ == "multiply", "Decorator should preserve the function name"
    assert multiply.__doc__ == "Multiplies two numbers.", "Decorator should preserve the function docstring"

    assert async_add.__name__ == "async_add", "Decorator should preserve the function name"
    assert async_add.__doc__ == "Asynchronously adds two numbers.", "Decorator should preserve the function docstring"

    assert async_multiply.__name__ == "async_multiply", "Decorator should preserve the function name"
    assert async_multiply.__doc__ == "Asynchronously multiplies two numbers.", "Decorator should preserve the function docstring"

    assert divide.__name__ == "divide", "Decorator should preserve the function name"
    assert divide.__doc__ == "Divides two numbers.", "Decorator should preserve the function docstring"

    assert async_divide.__name__ == "async_divide", "Decorator should preserve the function name"
    assert async_divide.__doc__ == "Asynchronously divides two numbers.", "Decorator should preserve the function docstring"

    assert complex_function.__name__ == "complex_function", "Decorator should preserve the function name"
    assert complex_function.__doc__ == "Function with various arguments.", "Decorator should preserve the function docstring"

# 8. Test decorator on function with various arguments
def test_logstep_complex_function(caplog):
    with caplog.at_level(logging.INFO):
        result = complex_function(1, 3, 5, 7, x=9, y=11)
        assert result == 1 + 3 + 5 + 7 + 9 + 11, "complex_function should correctly sum all arguments"

        # Check that a log message was emitted
        assert any("Complex Function - Starting complex_function" in record.message for record in caplog.records), \
            "No log message contains 'Complex Function - Starting complex_function'"

        assert any("Complex Function - Finished complex_function with result: 36" in record.message for record in caplog.records), \
            "No log message contains 'Complex Function - Finished complex_function with result: 36'"

# 9. Test decorator used with and without arguments
def test_logstep_decorator_usage(caplog):
    with caplog.at_level(logging.DEBUG):
        # Function decorated without arguments
        result_add = add(4, 5)
        assert result_add == 9, "add function should return the sum of two numbers"

        # Function decorated with arguments
        result_multiply = multiply(4, 5)
        assert result_multiply == 20, "multiply function should return the product of two numbers"

        # Check log messages
        assert any("Sync Operation - Starting add" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Starting add'"

        assert any("Sync Operation - Finished add with result: 9" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Finished add with result: 9'"

        assert any("Sync Operation - Starting multiply" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Starting multiply'"

        assert any("Sync Operation - Finished multiply with result: 20" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Finished multiply with result: 20'"

# 10. Test decorator with different logging levels
def test_logstep_logging_levels(caplog):
    with caplog.at_level(logging.DEBUG):
        multiply(2, 3)  # Decorated with DEBUG level
        add(2, 3)       # Decorated with INFO level

        # Check that multiply logs at DEBUG level
        debug_logs = [record for record in caplog.records if record.levelno == logging.DEBUG]
        assert any("Sync Operation - Starting multiply" in record.message for record in debug_logs), \
            "No DEBUG level log contains 'Sync Operation - Starting multiply'"

        assert any("Sync Operation - Finished multiply with result: 6" in record.message for record in debug_logs), \
            "No DEBUG level log contains 'Sync Operation - Finished multiply with result: 6'"

        # Check that add logs at INFO level
        info_logs = [record for record in caplog.records if record.levelno == logging.INFO]
        assert any("Sync Operation - Starting add" in record.message for record in info_logs), \
            "No INFO level log contains 'Sync Operation - Starting add'"

        assert any("Sync Operation - Finished add with result: 5" in record.message for record in info_logs), \
            "No INFO level log contains 'Sync Operation - Finished add with result: 5'"

# 11. Test multiple decorations on the same function
@logstep("First decorator", level=logging.INFO)
@logstep("Second decorator", level=logging.DEBUG)
def double(a):
    """Doubles a number."""
    return a * 2

def test_logstep_multiple_decorators(caplog):
    with caplog.at_level(logging.DEBUG):
        result = double(5)
        assert result == 10, "double function should return twice the input"

        # Since decorators are applied from bottom to top, the outermost decorator is "First decorator"
        # The log messages should reflect both decorators
        # Example:
        # "First decorator - Starting double ..."
        # "Second decorator - Starting double ..."
        # "Second decorator - Finished double ..."
        # "First decorator - Finished double ..."

        # Check for the innermost decorator's log first
        assert any("Second decorator - Starting double" in record.message for record in caplog.records), \
            "No log message contains 'Second decorator - Starting double'"

        assert any("Second decorator - Finished double with result: 10" in record.message for record in caplog.records), \
            "No log message contains 'Second decorator - Finished double with result: 10'"

        # Check for the outermost decorator's log
        assert any("First decorator - Starting double" in record.message for record in caplog.records), \
            "No log message contains 'First decorator - Starting double'"

        assert any("First decorator - Finished double with result: 10" in record.message for record in caplog.records), \
            "No log message contains 'First decorator - Finished double with result: 10'"

# 12. Test decorator with functions returning different types
def test_logstep_various_return_types(caplog):
    with caplog.at_level(logging.INFO):
        # Function returning string
        greeting = greet("Alice")
        assert greeting == "Hello, Alice!", "greet function should return a greeting string"

        # Function returning integer
        result_add = add(10, 20)
        assert result_add == 30, "add function should return the sum of two numbers"

        # Check log messages
        assert any("Sync Operation - Starting greet" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Starting greet'"

        assert any("Sync Operation - Finished greet with result: Hello, Alice!" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Finished greet with result: Hello, Alice!'"

        assert any("Sync Operation - Starting add" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Starting add'"

        assert any("Sync Operation - Finished add with result: 30" in record.message for record in caplog.records), \
            "No log message contains 'Sync Operation - Finished add with result: 30'"

# 13. Test decorator with functions returning None
@logstep("Void Function")
def void_function():
    """Function that returns nothing."""
    pass

def test_logstep_void_function(caplog):
    with caplog.at_level(logging.INFO):
        result = void_function()
        assert result is None, "void_function should return None"

        # Check that a log message was emitted
        assert any("Void Function - Starting void_function" in record.message for record in caplog.records), \
            "No log message contains 'Void Function - Starting void_function'"

        assert any("Void Function - Finished void_function with result: None" in record.message for record in caplog.records), \
            "No log message contains 'Void Function - Finished void_function with result: None'"

# 14. Test decorator with functions having no arguments
@logstep("No Args Function")
def no_args_function():
    """Function that takes no arguments."""
    return "No args"

def test_logstep_no_args_function(caplog):
    with caplog.at_level(logging.INFO):
        result = no_args_function()
        assert result == "No args", "no_args_function should return 'No args'"

        # Check that a log message was emitted
        assert any("No Args Function - Starting no_args_function" in record.message for record in caplog.records), \
            "No log message contains 'No Args Function - Starting no_args_function'"

        assert any("No Args Function - Finished no_args_function with result: No args" in record.message for record in caplog.records), \
            "No log message contains 'No Args Function - Finished no_args_function with result: No args'"

# 15. Test decorator with functions having keyword-only arguments
@logstep("Keyword Only Function")
def keyword_only_function(a, *, b=10):
    """Function with keyword-only arguments."""
    return a + b

def test_logstep_keyword_only_function(caplog):
    with caplog.at_level(logging.INFO):
        result = keyword_only_function(5, b=15)
        assert result == 20, "keyword_only_function should correctly handle keyword-only arguments"

        # Check that a log message was emitted
        assert any("Keyword Only Function - Starting keyword_only_function" in record.message for record in caplog.records), \
            "No log message contains 'Keyword Only Function - Starting keyword_only_function'"

        assert any("Keyword Only Function - Finished keyword_only_function with result: 20" in record.message for record in caplog.records), \
            "No log message contains 'Keyword Only Function - Finished keyword_only_function with result: 20'"

# ---------------------------
# Additional Test Cases (Optional)
# ---------------------------

# 16. Test decorator on method within a class
class SampleClass:
    @logstep("Class Method Operation")
    def method_add(self, a, b):
        """Method that adds two numbers."""
        return a + b

    @logstep("Class Method Operation", level=logging.ERROR)
    async def async_method_multiply(self, a, b):
        """Asynchronously multiplies two numbers."""
        await asyncio.sleep(0.1)
        return a * b

def test_logstep_class_methods(caplog):
    with caplog.at_level(logging.INFO):
        instance = SampleClass()
        result = instance.method_add(7, 8)
        assert result == 15, "method_add should return the sum of two numbers"

        # Check that a log message was emitted
        assert any("Class Method Operation - Starting method_add" in record.message for record in caplog.records), \
            "No log message contains 'Class Method Operation - Starting method_add'"

        assert any("Class Method Operation - Finished method_add with result: 15" in record.message for record in caplog.records), \
            "No log message contains 'Class Method Operation - Finished method_add with result: 15'"

@pytest.mark.asyncio
async def test_logstep_async_class_methods(caplog):
    with caplog.at_level(logging.ERROR):
        instance = SampleClass()
        result = await instance.async_method_multiply(3, 4)
        assert result == 12, "async_method_multiply should return the product of two numbers"

        # Check that a log message was emitted with the custom message and ERROR level
        error_logs = [record for record in caplog.records if record.levelno == logging.ERROR]
        assert any("Class Method Operation - Starting async_method_multiply" in record.message for record in error_logs), \
            "No ERROR level log contains 'Class Method Operation - Starting async_method_multiply'"

        assert any("Class Method Operation - Finished async_method_multiply with result: 12" in record.message for record in error_logs), \
            "No ERROR level log contains 'Class Method Operation - Finished async_method_multiply with result: 12'"

# 17. Test decorator on lambda function
@logstep("Lambda Function Operation")
def decorated_lambda():
    """Function returning a lambda."""
    return lambda x: x * x

def test_logstep_lambda_function(caplog):
    with caplog.at_level(logging.INFO):
        lambda_func = decorated_lambda()
        assert lambda_func(5) == 25, "Lambda function should return the square of the input"

        # Check that a log message was emitted
        assert any("Lambda Function Operation - Starting decorated_lambda" in record.message for record in caplog.records), \
            "No log message contains 'Lambda Function Operation - Starting decorated_lambda'"

        assert any("Lambda Function Operation - Finished decorated_lambda with result: <function" in record.message for record in caplog.records), \
            "No log message contains 'Lambda Function Operation - Finished decorated_lambda with result: <function'"

# 18. Test decorator with functions having default mutable arguments
@logstep("Default Mutable Arguments")
def append_to_list(item, lst=None):
    """Function that appends an item to a list."""
    if lst is None:
        lst = []
    lst.append(item)
    return lst

def test_logstep_default_mutable_arguments(caplog):
    with caplog.at_level(logging.INFO):
        result1 = append_to_list(1)
        result2 = append_to_list(2)

        assert result1 == [1], "First call should return [1]"
        assert result2 == [2], "Second call should return [2], ensuring no shared mutable default"

        # Check that two log messages were emitted
        log_messages = [record.message for record in caplog.records if "Default Mutable Arguments - Starting append_to_list" in record.message]
        assert len(log_messages) == 2, "Two log messages should be emitted for two function calls"

# 19. Test decorator on generator function
@logstep("Generator Function Operation")
def generator_function(n):
    """Generator that yields numbers up to n."""
    for i in range(n):
        yield i

def test_logstep_generator_function(caplog):
    with caplog.at_level(logging.INFO):
        gen = generator_function(3)
        result = list(gen)
        assert result == [0, 1, 2], "generator_function should yield numbers from 0 to n-1"

        # Since generator_function is a generator, the decorator logs after the generator is created, not after iteration
        assert any("Generator Function Operation - Starting generator_function" in record.message for record in caplog.records), \
            "No log message contains 'Generator Function Operation - Starting generator_function'"

        assert any("Generator Function Operation - Finished generator_function with result: <generator object generator_function at" in record.message for record in caplog.records), \
            "No log message contains 'Generator Function Operation - Finished generator_function with result: <generator object generator_function at'"

# 20. Test decorator on class constructor (__init__)
class ClassWithInit:
    @logstep("Class Constructor Operation")
    def __init__(self, value):
        """Constructor that initializes the value."""
        self.value = value

def test_logstep_class_constructor(caplog):
    with caplog.at_level(logging.INFO):
        obj = ClassWithInit(10)
        assert obj.value == 10, "ClassWithInit should correctly initialize the value"

        # Check that a log message was emitted for __init__
        assert any("Class Constructor Operation - Starting __init__" in record.message for record in caplog.records), \
            "No log message contains 'Class Constructor Operation - Starting __init__'"

        assert any("Class Constructor Operation - Finished __init__ with result: None" in record.message for record in caplog.records), \
            "No log message contains 'Class Constructor Operation - Finished __init__ with result: None'"