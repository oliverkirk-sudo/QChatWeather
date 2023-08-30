from typing import Union, Optional

import logging as logger

import requests
from httpx import Response

from plugins.QChatWeather.pkg.model import AirApi, NowApi, DailyApi, HourlyApi, WarningApi, WeatherInfo
from plugins.QChatWeather.config.config import Config

config = Config()


class APIError(Exception):
    ...


class ConfigError(Exception):
    ...


class CityNotFoundError(Exception):
    ...


def _get_data(url: str, params: dict) -> Response:
    with requests.Session() as client:
        res = client.get(url, params=params)
    return res


def _check_response(response: Response) -> bool:
    if response.status_code == 200:
        logger.debug(f"{response.json()}")
        return True
    else:
        raise APIError(f"Response code:{response.status_code}")


class Weather:
    def __url__(self):
        self.url_geoapi = "https://geoapi.qweather.com/v2/city/"
        if self.api_type == 2 or self.api_type == 1:
            self.url_weather_api = "https://api.qweather.com/v7/weather"
            self.url_weather_warning = "https://api.qweather.com/v7/warning/now"
            self.url_air = "https://api.qweather.com/v7/air/now"
            self.url_hourly = "https://api.qweather.com/v7/weather/24h"
            self.url_info = "https://api.qweather.com/v7/indices/1d"
            self.forecast_days = 7
            # if self.api_type == 1:
            logger.info("使用标准订阅API")
            # else:
            #     logger.info("使用商业版API")
        elif self.api_type == 0:
            self.url_weather_api = "https://devapi.qweather.com/v7/weather/"
            self.url_weather_warning = "https://devapi.qweather.com/v7/warning/now"
            self.url_air = "https://devapi.qweather.com/v7/air/now"
            self.url_hourly = "https://devapi.qweather.com/v7/weather/24h"
            self.url_info = "https://devapi.qweather.com/v7/indices/1d"
            self.forecast_days = 7
            logger.info("使用免费订阅API")
        else:
            raise ConfigError(
                "api_type 必须是为 (int)0 -> 免费订阅, (int)1 -> 标准订阅, (int)2 -> 商业版"
                f"\n当前为: ({type(self.api_type)}){self.api_type}"
            )

    def __init__(self, city_name: str, api_key: str, api_type: Union[int, str] = 0):
        self.city_name = city_name
        self.apikey = api_key
        self.api_type = int(api_type)
        self.__url__()

        # self.now: Optional[Dict[str, str]] = None
        # self.daily = None
        # self.air = None
        # self.warning = None
        self.__reference = "\n请参考: https://dev.qweather.com/docs/start/status-code/"

    def load_data(self):
        self.city_id = self._get_city_id()
        (
            self.now,
            self.daily,
            self.air,
            self.warning,
            self.hourly,
            self.info
        ) = (
            self._now, self._daily, self._air, self._warning, self._hourly, self._info()
        )
        self._data_validate()

    def _get_city_id(self, api_type: str = "lookup"):
        res = _get_data(
            url=self.url_geoapi + api_type,
            params={"location": self.city_name, "key": self.apikey, "number": 1},
        )

        res = res.json()
        logger.debug(res)
        if res["code"] == "404":
            raise CityNotFoundError()
        elif res["code"] != "200":
            raise APIError("错误! 错误代码: {}".format(res["code"]) + self.__reference)
        else:
            self.city_name = res["location"][0]["name"]
            return res["location"][0]["id"]

    def _data_validate(self):
        if self.now.code == "200" and self.daily.code == "200":
            pass
        else:
            raise APIError(
                "错误! 请检查配置! "
                f"错误代码: now: {self.now.code}  "
                f"daily: {self.daily.code}  "
                + "air: {}  ".format(self.air.code if self.air else "None")
                + "warning: {}".format(self.warning.code if self.warning else "None")
                + self.__reference
            )

    @property
    def _now(self) -> NowApi:
        res = _get_data(
            url=self.url_weather_api + "now",
            params={"location": self.city_id, "key": self.apikey},
        )
        _check_response(res)
        return NowApi(**res.json())

    @property
    def _daily(self) -> DailyApi:
        res = _get_data(
            url=self.url_weather_api + str(self.forecast_days) + "d",
            params={"location": self.city_id, "key": self.apikey},
        )
        _check_response(res)
        return DailyApi(**res.json())

    @property
    def _air(self) -> AirApi:
        res = _get_data(
            url=self.url_air,
            params={"location": self.city_id, "key": self.apikey},
        )
        _check_response(res)
        return AirApi(**res.json())

    @property
    def _warning(self) -> Optional[WarningApi]:
        res = _get_data(
            url=self.url_weather_warning,
            params={"location": self.city_id, "key": self.apikey},
        )
        _check_response(res)
        return None if res.json().get("code") == "204" else WarningApi(**res.json())

    @property
    def _hourly(self) -> HourlyApi:
        res = _get_data(
            url=self.url_hourly,
            params={"location": self.city_id, "key": self.apikey},
        )
        _check_response(res)
        return HourlyApi(**res.json())

    def _info(self) -> WeatherInfo:
        res = _get_data(
            url=self.url_info,
            params={"location": self.city_id, "key": self.apikey, "type": config.qweather_info, 'lang': 'zh'}
        )
        _check_response(res)
        return WeatherInfo(**res.json())
