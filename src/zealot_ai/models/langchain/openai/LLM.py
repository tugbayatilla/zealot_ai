from langchain_openai import AzureChatOpenAI
from typing import Optional, Union
from pydantic import BaseModel
from ....settings.Settings import Settings

class LLM(AzureChatOpenAI):
    """
    Interited from AzureChatOpenAI Model
    """
    
    def __init__(self, settings: Optional[Settings] = None, **kwargs) -> None:
        
        if settings is None:
            settings = Settings(section='llm')

        settings['azure_endpoint'] = settings['endpoint']

        super().__init__(**settings, **kwargs)
        

    def __call__(self, schema: Union[dict, BaseModel, None] = None) -> AzureChatOpenAI:
        """ 
        Returns llm model
        """
        if schema:
            return self.with_structured_output(schema=schema)

        return self
