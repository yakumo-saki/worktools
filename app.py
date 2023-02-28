from src.main import config, WorkToolsApp
from src.config import Config
from src.consts import Strings
import logging

logger: logging.Logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        format="{asctime} [{levelname:.5}] {name}: {message}",
        style="{",
        encoding="utf-8",
        level=logging.DEBUG,
        force=True,
        filename='/tmp/WorkTools.log',
        filemode='w'
    )

    logger.info(f"{Strings.APP_TITLE} start.")

    config = Config()
    config.load_config()

    WorkToolsApp().run()
