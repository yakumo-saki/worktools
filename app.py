import rumps
from strings import Strings 

class WorkToolsApp(rumps.App):
    def __init__(self):
        super(WorkToolsApp, self).__init__(type(self).__name__)
        self.menu = [
            Strings.MENU_START_POMO,
            Strings.MENU_STOP_POMO,
            Strings.MENU_POMO_AUTO_LIGHT,
            None,
            Strings.MENU_SET_LIGHT_RED,
            Strings.MENU_SET_LIGHT_YELLOW,
            None,
            Strings.MENU_PREFERENCES,
            None,
        ]
        rumps.debug_mode(True)
        self.timer = rumps.Timer(self.timerTick, 1)
        self.timer.stop()

    @rumps.clicked(Strings.MENU_PREFERENCES)
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked(Strings.MENU_START_POMO)
    def start(self, sender):
        sender.state = not sender.state
        self.timer.start()

    @rumps.clicked(Strings.MENU_STOP_POMO)
    def stop(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")
        self.title = ""
        self.timer.stop()

    @rumps.clicked(Strings.MENU_POMO_AUTO_LIGHT)
    def autoColorChange(self, sender):
        sender.state = not sender.state

    def timerTick(sender, self):
        import time

        timestr = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
        print(timestr)
        sender.title = timestr


if __name__ == "__main__":
    WorkToolsApp().run()
