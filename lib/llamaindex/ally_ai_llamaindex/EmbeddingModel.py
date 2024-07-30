from typing import Optional
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import Settings as LlamaSettings
from ally_ai.core import Settings
import logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

class EmbeddingModel(AzureOpenAIEmbedding):

    ally_settings: Settings = None

    def __init__(self, settings: Optional[Settings] = None, **kwargs) -> None:
        if settings is None:
            settings = Settings(section='embeddings')

        settings['azure_endpoint'] = settings.pop('endpoint')
        settings['azure_deployment'] = settings.pop('deployment_name')

        super().__init__(**settings, **kwargs)

        self.ally_settings = settings

        LlamaSettings.embed_model = self
