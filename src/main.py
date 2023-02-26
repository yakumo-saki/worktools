import rumps
from src.consts import * 
from src.pomodoro import Pomodoro, PomoType
from src.about import *
from src.hue import HueBridge
import os

from logging import getLogger
logger = getLogger(__name__)

class WorkToolsApp(rumps.App):

    def __init__(self):
        super(WorkToolsApp, self).__init__(type(self).__name__)
        self.menu = [
            Strings.MENU_START_POMO,
            Strings.MENU_STOP_POMO,
            None,
            Strings.MENU_START_ZONE,
            Strings.MENU_STOP_ZONE,
            None,
            Strings.MENU_POMO_AUTO_LIGHT,
            None,
            Strings.MENU_HUE_CONNECT,
            Strings.MENU_HUE_MEETING,
            Strings.MENU_HUE_FOCUS,
            Strings.MENU_HUE_ZONE,
            None,
            Strings.MENU_PREFERENCES,
            (Strings.MENU_UTIL, [rumps.MenuItem(Strings.MENU_LIST_LIGHTS, callback=self.show_lights)]),
            Strings.MENU_ABOUT,
            None,
        ]
        rumps.debug_mode(False)
        self.icon = os.path.join(Strings.IMG_DIR, 'circle_gray.png')
        self.timer = rumps.Timer(self.timer_tick, 1)
        self.pomodoro = Pomodoro()
        self.hue = HueBridge()

    @rumps.clicked(Strings.MENU_ABOUT)
    def about(self, _):
        showAboutWindow()

    @rumps.clicked(Strings.MENU_PREFERENCES)
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked(Strings.MENU_START_POMO)
    def start(self, _):
        next = self.pomodoro.get_next()
        self.pomodoro.start(next)
        self.timer.start()

    @rumps.clicked(Strings.MENU_STOP_POMO)
    def stop(self, _):
        self.title = ""
        self.pomodoro.stop()
        self.timer.stop()

    @rumps.clicked(Strings.MENU_POMO_AUTO_LIGHT)
    def auto_color_change(self, sender):
        sender.state = not sender.state

    @rumps.clicked(Strings.MENU_POMO_AUTO_LIGHT)
    def auto_color_change(self, sender):
        sender.state = not sender.state

    @rumps.clicked(Strings.MENU_HUE_CONNECT)
    def hue_connect(self, sender):
        ret = self.hue.connect("10.1.0.195")
        sender.state = ret

    @rumps.clicked(Strings.MENU_HUE_MEETING)
    def hue_meeting(self, sender):
        self.hue.light_on(7, [255, 0, 0], 254)

    @rumps.clicked(Strings.MENU_LIST_LIGHTS) # サブメニューはこの形式でイベントハンドラを追加できない
    def show_lights(self, sender):
        rumps.alert("not impl")

    def timer_tick(sender, self):
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
        
