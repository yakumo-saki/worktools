#!/usr/bin/python
import os
import typing

from phue import Bridge, PhueRegistrationException,Light
from src.config import get_config_dir
from src.consts import Strings


from rgbxy import Converter

rgbxyconv = Converter()

class HueBridge:

    def __init__(self) -> None:
        self._bridge: Bridge = None
        self._connected = False

    def is_connected(self):
        return self._connected

    def connect(self, bridge_ip: str) -> bool:
        bridge_config_path = os.path.join(get_config_dir(), Strings.PHUE_FILE)

        try:
            self._bridge = Bridge(ip=bridge_ip, config_file_path=bridge_config_path) # Enter bridge IP here.
            self._bridge.connect()
            self._connected = True
            return True
        except PhueRegistrationException:
            self._connected = False
            return False
        
    def get_lights(self) -> typing.Dict[int, Light]:
        if self.is_connected == False:
            return []
        
        lights = self._bridge.get_light_objects('id')
        return lights

    def get_light_by_id(self, light_id:int) -> Light:
        """
        ライトを取得する。ついでにreachableかどうかもチェックする。
        条件に合わない場合は、Noneが帰る
        """
        if self.is_connected() == False:
            return None

        light: Light = self._bridge.get_light(light_id)
        if light == None:
            return None
        
        if light.reachable == False:
            return None
        
        return light

    def lights_on(self, light_id: int, rgb: typing.List[int, int, int], brightness: int) -> bool:
        """
        ライトをONにする
        args:
            light_id get_lights で得られるID
            rgb: 色
            brightness 0-254
        """
        light = self.get_light_by_id(light_id)
        if light == None:
            return False

        # RGB colors to XY  
        xy = rgbxyconv.rgbtoxy(**rgb)

        light.xy = xy
        light.brightness = brightness
        light.on = True
        return True

    def lights_off(self, light_id: int) -> bool:
        light = self.get_light_by_id(light_id)
        if light == None:
            return False

        light.on = False
        return True

