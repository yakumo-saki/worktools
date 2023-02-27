class HueEventType:
    """config hue.*"""

    # used for
    # app hue light status
    # config.toml hue light section names
    FOCUS = "focus" # Start Pomodoro
    RELAX = "relax"
    BREAK = "break"
    ZONE = "zone"
    MEETING = "meeting"

    IDLE='IDLE'   # this is not related to config.toml

    @classmethod
    def from_pomoType(cls, pomoType:str) -> str:
        from src.pomodoro import PomoType
        if pomoType == PomoType.FOCUS:
            return HueEventType.FOCUS
        elif pomoType == PomoType.BREAK:
            return HueEventType.BREAK
        elif pomoType == PomoType.RELAX:
            return HueEventType.RELAX
        
        raise ValueError(f"unknown {pomoType}")

class Strings:
    APP_TITLE = "Work Tools"
    CFG_DIR = "WorkTools"
    CFG_FILE = "config.toml"
    IMG_DIR = 'resources/img'
    PHUE_FILE = "python_hue.conf"

    MENU_POMO = "Pomodoro"
    MENU_START_POMO = "Start pomo"
    MENU_STOP_POMO = "Stop pomo"
    MENU_SKIP_RELAX = "Skip Relax"
    
    MENU_ZONE = "Zone"
    MENU_START_ZONE = "Enter zone"
    MENU_STOP_ZONE = "Exit zone"

    MENU_HUE = "Philips Hue"
    MENU_HUE_AUTO_LIGHT = "Set Light color on Pomo/Zone"
    MENU_HUE_CONNECT = "Connect to hue bridge"

    MENU_HUE_OVERRIDE = "Hue Override"
    MENU_HUE_FOCUS = "Set Focus"
    MENU_HUE_ZONE = "Set Zone"
    MENU_HUE_MEETING = "Set Meeting"
    MENU_HUE_OFF = "Turn off light"

    MENU_OTHERS = "Others"
    MENU_PREFERENCES = "Preferences"
    MENU_LIST_LIGHTS = "Show lights"
    MENU_ABOUT = "About"

    NOTIFY_DONE_SUBTITLE = '完了！'
    NOTIFY_NEXT_RELAX = '時間です。少しリラックスしましょう！'
    NOTIFY_NEXT_FOCUS = '休憩完了！集中していきましょう！'
    NOTIFY_NEXT_BREAK = 'かなり集中しました。一息つきましょう。'

