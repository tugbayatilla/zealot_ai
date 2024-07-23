from src.zealot_ai.models.langchain.openai.LLM import LLM


def test_default_llm_is_not_none():
    llm = LLM()

    assert llm is not None
