from src.zealot_ai.langchain import LLM, Embeddings, Settings
def test_llm_is_not_none():
    llm = LLM()

    assert llm is not None

def test_embeddings_is_not_none():
    embeddings = Embeddings()

    assert embeddings is not None

def test_settings_is_not_none():
    embeddings = Settings(section='llm')

    assert embeddings is not None
