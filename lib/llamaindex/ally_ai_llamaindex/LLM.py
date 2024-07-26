from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.base.llms.types import ChatResponse, ChatMessage
from llama_index.core import Settings as LlamaSettings
from typing import Optional, Sequence, Any
from ally_ai_core import Settings


class LLM(AzureOpenAI):
    """
    Interited from AzureChatOpenAI Model
    """
    settings: Settings = None

    def __init__(self, settings: Optional[Settings] = None, **kwargs) -> None:

        if settings is None:
            settings = Settings(section='llm')

        settings['azure_endpoint'] = settings.pop('endpoint')
        settings['azure_deployment'] = settings.pop('deployment_name')

        super().__init__(**settings, **kwargs)

        self.settings = settings

        LlamaSettings.llm = self


    def invoke(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        return self.chat(messages=messages, **kwargs)