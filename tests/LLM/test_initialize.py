from src.zealot_ai.models.langchain.openai.LLM import LLM


def test_default_llm_is_not_none():
    llm = LLM()

    assert llm is not None


def test_default_llm_settings_is_not_none():
    llm = LLM()

    assert llm._settings is not None

def test_call_is_not_none():
    llm = LLM()
    model = llm()

    assert model is not None