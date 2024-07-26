from ally_ai_llamaindex.LLM import LLM

def test_llamaindex_llm_init():
    llm = LLM()

    assert llm is not None
    