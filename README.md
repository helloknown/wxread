本项目基于 https://github.com/findmover/wxread ，因为可能需要帮其他朋友一起挂机阅读 项目增加了多用户配置
1、users 目录下的每一个配置文件代表一个用户的信息，  
- headers: 请求头，注意要把json文件中headers的cookie属性删掉，必填
- cookies: 用户 cookie，必填
- max_times: 执行次数，这里代表翻页的次数，次数越大，代表自动阅读时间越长，反之越小。默认50  
- token: 发起通知的令牌，这里使用的 [server酱](https://sct.ftqq.com)，仅通知开始和结束自动阅读，每日5次免费通知，足够用了。不配置则不发送通知

2、使用 python 的定时调度替代原项目的 crontab 方案，默认早上6:30 ~ 7:00 点之后开始自动，避开用户常规阅读时间