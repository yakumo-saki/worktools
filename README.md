# Work Tools

My work support tool for macOS.

* Pomodoro Timer
* Philips hue integration

## Install

* Download from release section
* Extract and copy *.app to Applications

## How to use

Timers are usable out of the box.
You want to use Philips Hue integration. follow these steps.

1. Start Work Tools.app to create default config
2. Open your ~/Library/Application Support/WorkTools/config.toml
3. Edit it. (at least bridge_ip must be filled.)
4. (re) Start app
5. Push your phillips hue bridge's center button
6. Click `Menubar icon -> Connect to hue bridge` within 30sec.


## config

config file is TOML format. Default location is ~/Library/Application Support/WorkTools/config.toml
If you define environment value XDG_CONFIG_HOME, config file is $XDG_CONFIG_HOME/WorkTools/config.toml

### hue

* `bridge_ip` Philips hue bridge IP address.
* `default_light_id` Which light you want to use. get id by `Utility -> Show lights`

## Develop

```
pip3 install -r requirements.txt
python3 app.py
```

## Build as .app

```
python3 setup.py py2app
```

## Icon license

* Application icon is [瞑想の達人](https://icons8.com/icon/8xS9Iz7hUgkw/%E7%9E%91%E6%83%B3%E3%81%AE%E9%81%94%E4%BA%BA) icon by [Icons8](https://icons8.com)