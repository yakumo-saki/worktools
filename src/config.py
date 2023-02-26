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
        self._light_id = cfg.get('light_id')

        self._rgb = self._rgb if self._rgb != None else [255, 255, 255]
        self._brightness = self._brightness if  self._brightness != None else 254
        self._saturation = self._saturation if  self._saturation != None else 254

    def get_rgb(self) -> List[int]:
        return self._rgb

    def get_brightness(self) -> int:
        return self._brightness
        
    def get_saturation(self) -> int:
        return self._saturation

    def get_light_id(self) -> int:
        return self._light_id

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

    def __init__(self) -> None:
        cfgpath = os.path.join(get_config_dir(), Strings.CFG_FILE)
        self._cfgpath = cfgpath
        logging.debug(f"config file path = {self._cfgpath}")

    def load_config(self):
        """
        configをロードします。
        存在しない場合デフォルト値の設定ファイルを生成します。
        """
        if os.path.isfile(self._cfgpath) == False:
            self._create_default_config(self._cfgpath)

        self._config = self._load_config_file(self._cfgpath)

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

    def get_bridge_ip(self) -> str:
        return self._config['hue']['bridge_ip']
    
    def get_light_config(self, type:str) -> LightConfig:
        cfg = self._config['hue'][type]
        
        id = cfg.get('light_id')
        cfg['light_id'] = id if id != None else self._config['hue']['default_light_id']
        
        return LightConfig(cfg)

    @property
    def auto_color_change(self) -> bool:
        flag = self._config['hue'].get('auto_color_change')
        return flag == True

    @auto_color_change.setter
    def auto_color_change(self, onoff: bool):
        self._config['hue']['auto_color_change'] = onoff
        self.write_config()

    def write_config(self):
        with open(self._cfgpath, "wb") as f:
            tomli_w.dump(self._config, f)
        

