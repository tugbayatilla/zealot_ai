from langchain_openai import AzureOpenAIEmbeddings
from ....settings import EmbeddingSettings


class Embeddings:

    def __init__(self, settings: EmbeddingSettings) -> None:
        self._settings = settings

    def __call__(self) -> AzureOpenAIEmbeddings:
        """ 
        - Reads 'embeddings' section from the app-settings.yaml file and apply changes
        - The values can be overriden in Settings
        """

        embed_model = AzureOpenAIEmbeddings(
            api_key=self._settings.api_key,
            azure_endpoint=self._settings.endpoint,
            api_version=self._settings.api_version,
            model=self._settings.model,
            azure_deployment=self._settings.deployment_name,
        )

        return embed_model
