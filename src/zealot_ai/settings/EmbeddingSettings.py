from typing import Literal
from .Settings import Settings
from ..core.utils import _kwargs_or_default


class EmbeddingSettings(Settings):

    def __init__(self, **kwargs):
        """
        - use kwargs to override values
        """
        super.__init__()
        section = self.get_section(name='llm')

        self.api_key: str = _kwargs_or_default(key='api_key', default=section['api_key'], kwargs=kwargs) 
        self.api_version: str = _kwargs_or_default(key='api_version', default=section['api_version'], kwargs=kwargs)
        self.endpoint: str = _kwargs_or_default(key='endpoint', default=section['endpoint'], kwargs=kwargs)
        self.model: str = _kwargs_or_default(key='model', default=section['model'], kwargs=kwargs)
        self.deployment_name: str = _kwargs_or_default(key='deployment_name', default=section['deployment_name'], kwargs=kwargs)

    def __call__(self):
        return self