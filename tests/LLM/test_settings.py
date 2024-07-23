from src.ally_ai.langchain import LLM


def test_settings_path_property():
    llm = LLM()

    assert llm.settings.path == './app-settings.yaml'


def test_settings_section_property():
    llm = LLM()

    assert llm.settings.section == 'llm'


def test_settings_has_api_key():
    llm = LLM()

    assert llm.settings['api_key'] == '<private-key>'
