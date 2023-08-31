from typing import Optional

class Config:
    qweather_apikey: Optional[str] = ''
    qweather_apitype: Optional[int] = 0
    qweather_info: Optional[str] = '1,5,9,16'
    defulte_mode: Optional[bool] = False
    debug: bool = False

