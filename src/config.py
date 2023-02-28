import os
from src.consts import Strings
import logging
from typing import List, Optional, Dict
import tomli
import tomli_w

from logging import getLogger

logger = getLogger(__name__)


class PomoConfigKey:
    FOCUS = "focus"
    RELAX = "relax"
    BREAK = "break"
    BREAK_AFTER = "break_after_pomo"


class LightConfig:
    def __init__(self, cfg: dict) -> None:
        self._rgb = cfg.get("rgb")
        self._brightness = cfg.get("brightness")
        self._saturation = cfg.get("saturation")
        self._light_id = cfg.get("light_id")

        self._rgb = self._rgb if self._rgb != None else [255, 255, 255]
        self._brightness = self._brightness if self._brightness != None else 254
        self._saturation = self._saturation if self._saturation != None else 254

    @property
    def rgb(self) -> List[int]:
        return self._rgb

    @property
    def brightness(self) -> int:
        return self._brightness

    @property
    def saturation(self) -> int:
        return self._saturation

    @property
    def light_id(self) -> int:
        return self._light_id


def get_config_dir():
    """
    configファイルを置くディレクトリを取得します。優先順位は以下の通り
    1. XDG_CONFIG_HOME
    2. ~/.config/worktools if exist  (because cant set XDG_CONFIG_HOME when launch from GUI)
    3. Application Support
    return:
        path ~/Library/Application Support/worktools or ENV[XDG_CONFIG_HOME]/worktools
    """
    cfgdir = os.environ.get("XDG_CONFIG_HOME")
    if cfgdir != None:
        return os.path.join(cfgdir, Strings.CFG_DIR)
    
    dotconfig = os.path.expanduser(f"~/.config/{Strings.CFG_DIR}")
    if os.path.isdir(dotconfig):
        return dotconfig

    return os.path.expanduser("~/Library/Application Support/{Strings.CFG_DIR}")


class Config:
    def __init__(self) -> None:
        cfgpath = os.path.join(get_config_dir(), Strings.CFG_FILE)
        self._cfgpath = cfgpath

    def load_config(self):
        """
        configをロードします。
        存在しない場合デフォルト値の設定ファイルを生成します。
        """
        if os.path.isfile(self._cfgpath) == False:
            self._create_default_config(self._cfgpath)

        logging.info(f"config file path = {self._cfgpath}")
        self._config = self._load_config_file(self._cfgpath)

    def _load_config_file(self, cfgpath: str) -> dict:
        dict = {}
        with open(cfgpath, "rb") as f:
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
        return self._config["hue"]["bridge_ip"]

    def get_light_config(self, type: str) -> LightConfig:
        cfg = self._config["hue"][type]

        id = cfg.get("light_id")
        cfg["light_id"] = id if id != None else self._config["hue"]["default_light_id"]

        return LightConfig(cfg)

    def get_pomodoro_config(self) -> Dict[str, int]:
        cfg = self._config["pomodoro"]
        ret = {}

        defaults = {
            PomoConfigKey.FOCUS: 25,
            PomoConfigKey.RELAX: 5,
            PomoConfigKey.BREAK: 15,
            PomoConfigKey.BREAK_AFTER: 4,
        }

        for k in defaults:
            ret[k] = defaults[k] if k in cfg else cfg[k]

        to_minutes = [PomoConfigKey.FOCUS, PomoConfigKey.RELAX, PomoConfigKey.BREAK]
        for k in to_minutes:
            ret[k] = ret[k] * 60

        return ret

    @property
    def auto_color_change(self) -> bool:
        flag = self._config["hue"].get("auto_color_change")
        return flag == True

    @auto_color_change.setter
    def auto_color_change(self, onoff: bool):
        self._config["hue"]["auto_color_change"] = onoff
        self.write_config()

    def write_config(self):
        with open(self._cfgpath, "wb") as f:
            tomli_w.dump(self._config, f)
