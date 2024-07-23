from typing import Optional
from langchain_openai import AzureOpenAIEmbeddings
from ....settings.Settings import Settings


class Embeddings(AzureOpenAIEmbeddings):

    def __init__(self, settings: Optional[Settings] = None, **kwargs) -> None:
        if settings is None:
            settings = Settings(section='embeddings')

        settings['azure_endpoint'] = settings.pop('endpoint')
        settings['azure_deployment'] = settings.pop('deployment_name')

        super().__init__(**settings, **kwargs)
