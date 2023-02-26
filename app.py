from src.main import *
from src.config import Config
import logging

config: Config = None
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    # at first read config
    config = Config()
    config.load_config()

    WorkToolsApp().run()
