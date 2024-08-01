from typing import Optional
from langchain_openai import AzureOpenAIEmbeddings
from ally_ai_core import Settings
import logging

from ally_ai_langchain.api_key import get_api_key

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

class EmbeddingModel(AzureOpenAIEmbeddings):

    ally_settings: Settings = None

    def __init__(self, settings: Optional[Settings] = None, **kwargs) -> None:
        if settings is None:
            settings = Settings(section='embeddings')

        settings['azure_endpoint'] = settings.pop('endpoint')
        settings['azure_deployment'] = settings.pop('deployment_name')
        settings['api_key'] = get_api_key(api_env_key='LLM_KEY', **kwargs)
        
        super().__init__(**settings, **kwargs)

        self.ally_settings = settings

