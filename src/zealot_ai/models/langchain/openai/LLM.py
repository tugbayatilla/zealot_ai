from langchain_openai import AzureChatOpenAI
from typing import Optional, Union
from pydantic import BaseModel
from ....settings.LLMSettings import LLMSettings

class LLM:

    def __init__(self, settings: LLMSettings = LLMSettings()) -> None:
        self._settings = settings

    def __call__(self, schema: Union[dict, BaseModel, None] = None) -> AzureChatOpenAI:
        """ 
        Returns llm model
        """

        settings = self._settings

        llm = AzureChatOpenAI(
            api_key=settings.api_key,
            api_version=settings.api_version,
            azure_endpoint=settings.endpoint,
            model=settings.model,
            deployment_name=settings.deployment_name,
            temperature=settings.temperature,
            streaming=settings.streaming
        )
        if schema:
            llm = llm.with_structured_output(schema=schema)

        return llm


if __name__ == '__main__':
    llm = LLM(settings=LLMSettings())
    llm_model = llm(schema=None)