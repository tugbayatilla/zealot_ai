from ally_ai_langchain import LLM, EmbeddingModel, Settings


def test_llm_is_not_none():
    llm = LLM()

    assert llm is not None


def test_embeddings_is_not_none():
    embeddings = EmbeddingModel()

    assert embeddings is not None


def test_settings_is_not_none():
    embeddings = Settings(section='llm')

    assert embeddings is not None
