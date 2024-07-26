from typing import Optional
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import Settings as LlamaSettings
from ally_ai.core import Settings


class Embeddings(AzureOpenAIEmbedding):

    settings: Settings = None

    def __init__(self, settings: Optional[Settings] = None, **kwargs) -> None:
        if settings is None:
            settings = Settings(section='embeddings')

        settings['azure_endpoint'] = settings.pop('endpoint')
        settings['azure_deployment'] = settings.pop('deployment_name')

        super().__init__(**settings, **kwargs)

        self.settings = settings

        LlamaSettings.embed_model = self
