import rumps
from src.consts import * 
from src.pomodoro import Pomodoro, PomoType
from src.about import *
from src.hue import HueBridge
from src.config import Config
from typing import Optional
import os
from src.util import *

from logging import getLogger
logger = getLogger(__name__)

# at first read config
config = Config()
config.load_config()

class WorkToolsApp(rumps.App):

    def __init__(self):
        super(WorkToolsApp, self).__init__(type(self).__name__)

        rumps.debug_mode(False)
        self.icon = os.path.join(Strings.IMG_DIR, 'circle_gray.png')
        self.timer = rumps.Timer(self.timer_tick, 1)
        self.pomodoro = Pomodoro()
        self.hue = HueBridge()
        self.startup()

        # メニュー構築
        menu_connected = rumps.MenuItem(Strings.MENU_HUE_CONNECT, callback=self.hue_connect)
        menu_connected.state = self.hue.is_connected()

        menu_auto_light = rumps.MenuItem(Strings.MENU_HUE_AUTO_LIGHT, callback=self.auto_color_change)
        menu_auto_light.state = config.auto_color_change

        self.menu = [
            Strings.MENU_POMO,
            Strings.MENU_START_POMO,
            Strings.MENU_STOP_POMO,
            None,
            Strings.MENU_ZONE,
            Strings.MENU_START_ZONE,
            Strings.MENU_STOP_ZONE,
            None,
            Strings.MENU_HUE,
            menu_connected,
            menu_auto_light,
            Strings.MENU_HUE_MEETING,
            Strings.MENU_HUE_FOCUS,
            Strings.MENU_HUE_ZONE,
            Strings.MENU_HUE_OFF,
            None,
            
            (Strings.MENU_OTHERS, [
                #rumps.SliderMenuItem(10, 0, 100),
                rumps.MenuItem(Strings.MENU_LIST_LIGHTS, callback=self.show_lights),
                rumps.MenuItem(Strings.MENU_PREFERENCES, callback=self.show_prefs),
                rumps.MenuItem(Strings.MENU_ABOUT, callback=self.show_about)
            ]),
            None,
        ]

    def startup(self):
        if is_blank(config.get_bridge_ip() == False):
            self.hue.connect(config.get_bridge_ip())

    @rumps.clicked(Strings.MENU_START_POMO)
    def start(self, _):
        next = self.pomodoro.get_next()
        self.pomodoro.start(next)
        self.timer.start()

        if config.auto_color_change:
            self._hue_on(HueEventType.from_pomoType(self.pomodoro.currentType))

    @rumps.clicked(Strings.MENU_STOP_POMO)
    def stop(self, _):
        if config.auto_color_change:
            self._hue_off(HueEventType.from_pomoType(self.pomodoro.currentType))

        self.title = ""
        self.pomodoro.stop()
        self.timer.stop()



    @rumps.clicked(Strings.MENU_HUE_AUTO_LIGHT)
    def auto_color_change(self, sender):
        sender.state = not sender.state
        config.auto_color_change = sender.state

    @rumps.clicked(Strings.MENU_HUE_CONNECT)
    def hue_connect(self, sender):
        ret = self.hue.connect(config.get_bridge_ip())
        sender.state = ret

    @rumps.clicked(Strings.MENU_HUE_MEETING)
    def hue_meeting(self, sender):
        self._hue_on('meeting')

    def _hue_on(self, type:str):
        cfg = config.get_light_config(type)
        if cfg.get_brightness() == 0:
            self.hue.light_off(cfg.get_light_id())
        else:    
            self.hue.light_on(cfg.get_light_id(), cfg.get_rgb(), cfg.get_brightness(), cfg.get_saturation())

    def _hue_off(self, type:str):
        cfg = config.get_light_config(type)
        self.hue.light_off(cfg.get_light_id())

    @rumps.clicked(Strings.MENU_HUE_OFF)
    def hue_off(self, sender):
        """すべてのlightをoffにする"""
        self.hue.all_lights_off()

    # サブメニューのハンドラ
    def show_lights(self, sender):
        """登録されているlightの一覧"""
        rumps.alert("not impl")

    def show_prefs(self, _):
        """設定画面（多分rumpsだと作れなそう）"""
        rumps.alert("no preferences available!")

    def show_about(self, _):
        """about画面"""
        showAboutWindow()


    def timer_tick(sender, self):
        """タイマー1秒のコールバック"""

        left, max = sender.pomodoro.tick()

        if left < 0:
            return # -1 means error
        elif left > 0:
            pct = "{:0>3}".format(int( (max - left) / max * 100))
            p = pct[1:2]
            icon = os.path.join(Strings.IMG_DIR, f"circle_{p}.png")
            sender.icon = icon
            sender.title = f'{left}'
            return

        # 完了した時の通知
        next = sender.pomodoro.get_next()
        if next == PomoType.FOCUS:
            rumps.notification(Strings.APP_TITLE, Strings.NOTIFY_DONE_SUBTITLE, Strings.NOTIFY_NEXT_FOCUS)
        elif next == PomoType.BREAK:
            rumps.notification(Strings.APP_TITLE, Strings.NOTIFY_DONE_SUBTITLE, Strings.NOTIFY_NEXT_BREAK)
        elif next == PomoType.RELAX:
            rumps.notification(Strings.APP_TITLE, Strings.NOTIFY_DONE_SUBTITLE, Strings.NOTIFY_NEXT_RELAX)

        sender.icon = os.path.join(Strings.IMG_DIR, 'circle_10.png')
        sender.stop(sender)
        
