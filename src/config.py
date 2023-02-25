from tomlkit import comment
from tomlkit import document
from tomlkit import TOMLDocument
from tomlkit import parse
import os
from src.consts import Strings
import logging

class Config:

    def get_config_dir(self):
        cfgdir = os.environ.get("XDG_CONFIG_HOME")
        if cfgdir == None:
            return os.path.expanduser("~/Library/Application Support")

        return os.path.join(cfgdir, Strings.CFG_DIR)

    def load_config(self) -> document:
        """
        configをロードします。
        存在しない場合デフォルト値の設定ファイルを生成します。
        """
        cfgpath = os.path.join(self.get_config_dir(), Strings.CFG_FILE)
        if os.path.isfile(cfgpath) == False:
            self._create_default_config(cfgpath)

        logging.debug(cfgpath)
        self._config = self._load_config_file(cfgpath)

    def _load_config_file(self, cfgpath: str) -> TOMLDocument:
        cfg = ''
        with open(cfgpath) as f:
            cfg = f.read()

        logging.debug(cfg)
        return parse(cfg)


    def _create_default_config(self, cfgpath: str):
        import shutil
        import pathlib
        os.makedirs(pathlib.Path(cfgpath).parent, exist_ok=True)
        shutil.copyfile("resources/default_config.toml", cfgpath)
        
        logging.info("default config created on {cfgpath}")

