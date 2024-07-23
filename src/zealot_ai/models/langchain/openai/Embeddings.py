from typing import Optional
from langchain_openai import AzureOpenAIEmbeddings
from ....settings.Settings import Settings


class Embeddings(AzureOpenAIEmbeddings):

    def __init__(self, settings: Optional[Settings] = None, section: str = 'embeddings', **kwargs) -> None:
        if settings is None:
            settings = Settings()

        section = settings(section=section)
        section['azure_endpoint'] = section['endpoint']

        super().__init__(**section, **kwargs)
