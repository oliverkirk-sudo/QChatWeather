# QChatAIPaint

适用于[QChatGPT](https://github.com/RockChinQ/QChatGPT)的天气插件
<br>
代码参考于[nonebot-plugin-heweather](https://github.com/kexue-z/nonebot-plugin-heweather)

## 1、前置工作

- 在[和风天气](https://dev.qweather.com/)申请apikey
- 下载本插件`!plugin get https://github.com/oliverkirk-sudo/QChatWeather.git`
- 可选安装[QChatMarkdown](https://github.com/oliverkirk-sudo/QChatMarkdown),安装后启用配置文件中的选项，不安装则使用默认生成

<details>
<summary>安装QChatMarkdown前</summary>

![img1](./pic/1.jpg)

</details>

<details>
<summary>安装QChatMarkdown后</summary>

![img2](./pic/2.png)

</details>

## 2、修改配置文件

```python
class Config:
    qweather_apikey: Optional[str] = '' # 和风天气apikey
    qweather_apitype: Optional[int] = 0 # apikey类型 0 -> 免费订阅, 1 -> 标准订阅, 2 -> 商业版
    qweather_info: Optional[str] = '1,5,9,16' # 天气指数，具体看https://dev.qweather.com/docs/resource/indices-info/
    defulte_mode: Optional[bool] = False # 启用默认模式，即安装QChatMarkdown前
}
```

## 3、包含的指令

用户使用命令：

- `!天气 <城市>`

</br>
<b>该软件仅供学习交流，一切由该软件产生的不良影响由使用者承担</b>
</br>
