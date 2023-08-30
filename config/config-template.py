from typing import Optional

from plugins.QChatWeather.pkg.model import HourlyType


class Config:
    qweather_apikey: Optional[str] = ''
    qweather_apitype: Optional[int] = 0
    qweather_info: Optional[str] = '1,5,9,16'
    qweather_hourlytype: Optional[HourlyType] = HourlyType.current_12h
    debug: bool = False


plugin_config = Config()
QWEATHER_APIKEY = plugin_config.qweather_apikey
QWEATHER_APITYPE = plugin_config.qweather_apitype
QWEATHER_HOURLYTYPE = plugin_config.qweather_hourlytype
DEBUG = plugin_config.debug
