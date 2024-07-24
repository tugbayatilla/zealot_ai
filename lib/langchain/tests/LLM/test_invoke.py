import pytest
from ally_ai_langchain import LLM
from openai import APIConnectionError


def test_invoke_simple_raises_APIConnectionError():
    llm = LLM()
    with pytest.raises(APIConnectionError):
        llm.invoke('test')
