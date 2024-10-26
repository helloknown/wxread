本项目基于 https://github.com/findmover/wxread ，这里主要增加了多用户配置自动阅读  
  
1、users 目录下的每一个配置文件代表一个用户的信息，  
- headers: 请求头，必填  
- cookies: 用户 cookie，必填  
- max_times: 执行次数，这里代表翻页的次数，每次翻页后暂停大概 25~45s，必填  
- token: 发起通知的令牌，这里使用的 [server酱](https://sct.ftqq.com)，每日5次免费通知，已经够用了,不配置则不发送通知  