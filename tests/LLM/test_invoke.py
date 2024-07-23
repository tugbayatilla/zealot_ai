import pytest
from src.zealot_ai.langchain import LLM
from openai import APIConnectionError

def test_invoke_simple_raises_APIConnectionError():
    llm = LLM()
    with pytest.raises(APIConnectionError):
        llm.invoke('test')