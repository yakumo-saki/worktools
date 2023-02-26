import os
from src.consts import Strings
import logging
from typing import List, Optional
import tomli
import tomli_w

from logging import getLogger
logger = getLogger(__name__)

class LightConfig:
    def __init__(self, cfg: dict) -> None:
        self._rgb = cfg.get('rgb')
        self._brightness = cfg.get('brightness')
        self._saturation = cfg.get('saturation')

        self._rgb = self._rgb if self._rgb != None else [255, 255, 255]
        self._brightness = self._brightness if  self._brightness != None else 254
        self._saturation = self._saturation if  self._saturation != None else 254

    def get_rgb(self) -> List[int]:
        return self._rgb

    def get_brightness(self) -> List[int]:
        return self._brightness
        
    def get_saturation(self) -> List[int]:
        return self._saturation

def get_config_dir():
    """
    configファイルを置くディレクトリを取得します
    return:
        path ~/Library/Application Support/worktools or ENV[XDG_CONFIG_HOME]/worktools
    """
    cfgdir = os.environ.get("XDG_CONFIG_HOME")
    if cfgdir == None:
        return os.path.expanduser("~/Library/Application Support")

    return os.path.join(cfgdir, Strings.CFG_DIR)

class Config:

    def load_config(self):
        """
        configをロードします。
        存在しない場合デフォルト値の設定ファイルを生成します。
        """
        cfgpath = os.path.join(get_config_dir(), Strings.CFG_FILE)
        if os.path.isfile(cfgpath) == False:
            self._create_default_config(cfgpath)

        logging.debug(cfgpath)
        self._config = self._load_config_file(cfgpath)

    def _load_config_file(self, cfgpath: str) -> dict:
        dict = {}
        with open(cfgpath, 'rb') as f:
            dict = tomli.load(f)

        logger.debug(dict)
        return dict


    def _create_default_config(self, cfgpath: str):
        import shutil
        import pathlib
        os.makedirs(pathlib.Path(cfgpath).parent, exist_ok=True)
        shutil.copyfile("resources/default_config.toml", cfgpath)
        
        logger.info("default config created on {cfgpath}")

    def get_light_config(self, type:str) -> LightConfig:
        cfg = self._config['hue'][type]

