#!/usr/bin/python
import os
import typing

from phue import Bridge, PhueRegistrationException,Light
from src.config import get_config_dir
from src.consts import Strings
from rgbxy import Converter

from logging import getLogger
logger = getLogger(__name__)

rgbxyconv = Converter()

class HueBridge:

    def __init__(self) -> None:
        self._bridge: typing.Optional[Bridge] = None
        self._connected = False

    def is_connected(self):
        return self._connected

    def connect(self, bridge_ip: str) -> bool:
        bridge_config_path = os.path.join(get_config_dir(), Strings.PHUE_FILE)

        try:
            self._bridge = Bridge(ip=bridge_ip, config_file_path=bridge_config_path) # Enter bridge IP here.
            self._connected = True
            return True
        except PhueRegistrationException:
            self._connected = False
            logger.info("Connect to hue bridge failed. press bridge button and try again")
            return False
        
    def get_lights(self) -> typing.Dict[int, Light]:
        if self.is_connected == False:
            return {}
        
        lights = self._bridge.get_light_objects('id')
        if lights == None:
            return {}
            
        return lights

    def get_light_by_id(self, light_id:int) -> typing.Optional[Light]:
        """
        ライトを取得する。ついでにreachableかどうかもチェックする。
        条件に合わない場合は、Noneが帰る
        """
        if self.is_connected() == False:
            logger.info(f"cant get light_id {light_id}: not connected")
            return None

        lights: dict = self.get_lights()
        if light_id not in lights:
            logger.info(f"specified id {light_id} not found")
            return None

        light: Light = lights[light_id]
        if light == None:
            return None
        
        if light.reachable == False:
            logger.info(f"cant get light_id {light_id}: found but not reachable")
            return None
        
        return light

    def light_on(self, light_id: int, rgb: typing.List[int], brightness: int, saturation: int) -> bool:
        """
        ライトをONにする

        Args:
            light_id : get_lights で得られるID
            rgb: 色
            brightness: 0-254
            saturation: 0-254
        """
        light = self.get_light_by_id(light_id)
        if light == None:
            return False

        if brightness > 254:
            raise ValueError("brightness {brightness} is invalid, must be 0-254")
        elif brightness == 0:
            logger.info('light_on called with brightness=0. Should call light_off.')
            self.light_off(light_id)
            return True

        if saturation > 254:
            raise ValueError("saturation {saturation} is invalid, must be 0-254")

        # RGB colors to XY  
        xy = rgbxyconv.rgb_to_xy(*rgb)

        light.on = True
        light.xy = xy
        light.brightness = brightness
        light.saturation = saturation
        return True

    def light_off(self, light_id: int) -> bool:
        light = self.get_light_by_id(light_id)
        if light == None:
            return False

        light.on = False
        return True

    def all_lights_off(self) -> None:
        lights = self.get_lights()
        for id in lights.keys():
            self.light_off(id)

