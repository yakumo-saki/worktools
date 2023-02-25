import rumps
from src.consts import Strings

def showAboutWindow():
    opt = {
        "icon_path": 'nonfree/app-icon.icns',
        "title": f"About {Strings.APP_TITLE}",
        "message": 
        'https://github.com/yakumo-saki/worktool\n'
        '\n'
        'Application icon by\nIcons8 https://icons8.com'
    }

    window = rumps.alert(**opt)
