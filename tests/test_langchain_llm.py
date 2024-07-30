from ally_ai_langchain import LLM
from openai import APIConnectionError
import pytest


def test_default_llm_is_not_none():
    llm = LLM()
    assert llm is not None



def test_invoke_simple_raises_APIConnectionError():
    llm = LLM()
    with pytest.raises(APIConnectionError):
        llm.invoke('test')

def test_settings_path_property():
    llm = LLM()

    assert llm.ally_settings.path == './app-settings.yaml'


def test_settings_section_property():
    llm = LLM()

    assert llm.ally_settings.section == 'llm'


def test_settings_has_api_key():
    llm = LLM()

    assert llm.ally_settings['api_key'] == '<private-key>'

