from typing import Literal
import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)
import os

def get_api_key(api_env_key: Literal['LLM_KEY', 'EMBEDDINGS_KEY'],  **kwargs):
        f"""
        - kwargs['api_key'] : direct api key
        - kwargs['api_env_key'] : environment variable key
        """

        if 'api_key' in kwargs:
            logger.info(f"using 'api_key' from kwargs")
            return kwargs['api_key']
        
        if 'api_env_key' in kwargs:
            logger.info(f"change environment variables key from '{api_env_key}' to '{kwargs['api_env_key']}'")
            api_env_key = kwargs['api_env_key']

        logger.info(f"using environment variables key '{api_env_key}'")
        api_key = os.environ.get(api_env_key, '<Not-Found-In-Env>')
        if api_key == '<Not-Found-In-Env>':
            logger.error(f"api_key could not be found ({api_key}) with key '{api_env_key}' in the environment variables.")
        return api_key