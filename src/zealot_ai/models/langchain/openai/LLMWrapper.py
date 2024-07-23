from langchain_openai import AzureChatOpenAI
from typing import Optional, Union
from pydantic import BaseModel
from ....settings.LLMSettings import LLMSettings

class LLMWrapper(AzureChatOpenAI):

    def __init__(self, 
                 settings: LLMSettings = LLMSettings(), 
                 schema: Union[dict, BaseModel, None] = None) -> None:
        
        self.api_key=settings.api_key,
        self.api_version=settings.api_version,
        self.azure_endpoint=settings.endpoint,
        self.model=settings.model,
        self.deployment_name=settings.deployment_name,
        self.temperature=settings.temperature,
        self.streaming=settings.streaming
    
        if schema:
            self = self.with_structured_output(schema=schema)