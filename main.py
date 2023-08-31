import base64

import requests
from mirai import Image

from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost
from plugins.QChatWeather.config.config import Config
from plugins.QChatWeather.pkg.render_pic import render
from plugins.QChatWeather.pkg.weather_data import Weather, CityNotFoundError


def get_img(city):
    try:
        import plugins.QChatMarkdown
    except ImportError:
        return base64.b64encode(requests.get(requests.get('https://xiaobai.klizi.cn/API/wl/tianqi_1.php', params={'msg': city}).json()['url']).content).decode()
    config = Config()
    w_data = Weather(city_name=city, api_key=config.qweather_apikey, api_type=config.qweather_apitype)
    try:
        w_data.load_data()
        img = render(w_data)
        return base64.b64encode(img).decode()
    except CityNotFoundError:
        return ''

def send_msg(kwargs, msg):
    host: pkg.plugin.host.PluginHost = kwargs['host']
    host.send_person_message(kwargs['launcher_id'], msg) if kwargs[
                                                                'launcher_type'] == 'person' else host.send_group_message(
        kwargs['launcher_id'], msg)



# 注册插件
@register(name="QChatWeather", description="以图片形式输出天气", version="0.1", author="oliverkirk-sudo")
class QChatWeatherPlugin(Plugin):

    def __init__(self, plugin_host: PluginHost):
        pass

    @on(NormalMessageResponded)
    def process_message(self, event: EventContext, **kwargs):
        pass

    # 当收到个人消息时触发
    @on(PersonNormalMessageReceived)
    @on(GroupNormalMessageReceived)
    def normal_message_received(self, event: EventContext, **kwargs):
        pass

    @on(PersonCommandSent)
    @on(GroupCommandSent)
    def command_message_received(self, event: EventContext, **kwargs):
        if kwargs['command'] == '天气':
            if not kwargs['params']:
                send_msg(kwargs, ['地点是...空气吗?? >_<'])
            else:
                city = kwargs['params'][0]
                b64 = get_img(city)
                if b64:
                    event.add_return('reply', [Image(base64=b64)])
                else:
                    event.add_return('reply', ["天气获取失败"])
            event.prevent_default()
            event.prevent_postorder()
        pass

    # 插件卸载时触发
    def __del__(self):
        pass
