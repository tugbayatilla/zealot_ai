import src.zealot_ai as zealot
from tests import TEST_SETTINGS_PATH

def test_llm_is_not_none():
    llm_settings = zealot.LLMSettings(
        path=TEST_SETTINGS_PATH)
    llm = zealot.LLM(settings=llm_settings)
    model = llm()

    assert model is not None

def test_llm_is_not_none():
    llm_settings = zealot.LLMSettings(
        path=TEST_SETTINGS_PATH)
    llm = zealot.LLM(settings=llm_settings)
    model = llm()

    assert model is not None