from src.main import *
from src.config import Config
import logging

config: Config = None
logger:logging.Logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(format='{asctime} [{levelname:.5}] {name}: {message}', style='{',encoding='utf-8', level=logging.DEBUG, force=True)
    
    logger.info(f"{Strings.APP_TITLE} start.")
    WorkToolsApp().run()
