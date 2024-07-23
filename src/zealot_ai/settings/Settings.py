import yaml
import logging
from typing import Literal, Optional
from ..errors import YamlParseError
from ..core.utils import _kwargs_or_default


class Settings():

    def __init__(self, path='./app-settings.yaml', **kwargs):
        """
        - Use kwargs to override values
        """
        self._path = path
        self.kwargs = kwargs

    def _read_yaml(self):
        try:
            with open(self._path, 'r') as file:
                yaml_content = yaml.safe_load(file)
                return yaml_content
        except FileNotFoundError:
            raise
        except Exception as ex:
            raise YamlParseError(
                f"File '{self._path}' could not be parsed correcty to yaml! Original: {ex}")

    def __call__(self, section: Literal['llm', 'embeddings', 'vectordb']) -> Optional[dict]:
        """
            Returns None or dictionary
        """
        try:
            yaml_content = self._read_yaml()
            dict = yaml_content[section]

            dict.update({
                key: value
                for key, value in self.kwargs.items()
                if key in dict
            })

            return dict
        except Exception as ex:
            logging.error(
                f"Failed to read '{section}' section from '{self._path}'. Original: {ex}")
            raise
