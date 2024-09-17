from ally_ai_langsmith import Langsmith
import os
from ..Utils import env_var_on_off


def test_activate_langsmith():
    Langsmith()

    assert os.environ['LANGCHAIN_TRACING_V2'] == 'true'
    assert os.environ['LANGCHAIN_ENDPOINT'] == "https://api.smith.langchain.com"
    assert os.environ['LANGCHAIN_PROJECT'] == 'my-project'
    assert os.environ['LANGCHAIN_API_KEY'] == '<your-api-key>'

def test_activate_langsmith_set_api_key_differently():
    with env_var_on_off('langsmith__langchain_api_key', 'test_key'):
        Langsmith()

        assert os.environ['LANGCHAIN_TRACING_V2'] == 'true'
        assert os.environ['LANGCHAIN_ENDPOINT'] == "https://api.smith.langchain.com"
        assert os.environ['LANGCHAIN_PROJECT'] == 'my-project'
        assert os.environ['LANGCHAIN_API_KEY'] == 'test_key'
