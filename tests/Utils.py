from contextlib import contextmanager
import os

@contextmanager
def env_var_on_off(key, value):

    backup = os.environ.get(key, None)
    os.environ[key] = value
    
    yield
    
    if backup is None:
        del os.environ[key]
    else:
        os.environ[key] = backup
    