from .Settings import Settings
from ..core.utils import _kwargs_or_default
from typing import Union
from pydantic import BaseModel

class LLMSettings():

    def __init__(self, **kwargs):
        """
        - use kwargs to override values
        """
        settings = Settings(**kwargs)
        section = settings(section='llm')

        self.api_key: str = _kwargs_or_default(key='api_key', default=section['api_key'], **kwargs)
        self.endpoint: str = _kwargs_or_default(key='endpoint', default=section['endpoint'], **kwargs)
        self.api_version: str = _kwargs_or_default(key='api_version', default=section['api_version'], **kwargs)
        self.model: str = _kwargs_or_default(key='model', default=section['model'], **kwargs)
        self.deployment_name: str = _kwargs_or_default(key='deployment_name', default=section['deployment_name'], **kwargs)
        self.temperature: int = _kwargs_or_default(key='temperature', default=section['temperature'], **kwargs)
        self.streaming:bool = _kwargs_or_default(key='streaming', default=section['streaming'], **kwargs)
        self.schema: Union[dict, BaseModel, None] = None
