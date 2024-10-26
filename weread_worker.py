import time
import random
import requests
import json
import hashlib
import urllib.parse
from typing import Optional
from cookie import get_wr_skey
from push import sc_send
from config import UserConfig
from logger import setup_logger
from scheduler import TaskScheduler

class WeReadWorker:
    def __init__(self, user_config: UserConfig, user_id: str):
        self.config = user_config
        self.user_id = user_id
        self.logger = setup_logger(f"ReadingLogger_{user_id}", f"logs/wxread_{user_id}.log")
        self.url = "https://weread.qq.com/web/book/read"
        self.key = "3c5c8717f3daf09iop3423zafeqoi"
        self.scheduler = TaskScheduler(self.logger)

    def encode_data(self, data: dict, keys_to_include: Optional[list] = None) -> str:
        sorted_keys = sorted(data.keys())
        query_string = ''
        for key in sorted_keys:
            if keys_to_include is None or key in keys_to_include:
                value = data[key]
                encoded_value = urllib.parse.quote(str(value), safe='')
                query_string += f'{key}={encoded_value}&'
        return query_string.rstrip('&')

    def cal_hash(self, input_string: str) -> str:
        _7032f5 = 0x15051505
        _cc1055 = _7032f5
        length = len(input_string)
        _19094e = length - 1

        while _19094e > 0:
            _7032f5 = 0x7fffffff & (_7032f5 ^ ord(input_string[_19094e]) << (length - _19094e) % 30)
            _cc1055 = 0x7fffffff & (_cc1055 ^ ord(input_string[_19094e - 1]) << _19094e % 30)
            _19094e -= 2

        return hex(_7032f5 + _cc1055)[2:].lower()

    def process_reading(self) -> None:
        self.logger.info(f"用户 {self.user_id} - process_reading start...")
        num = 1
        data = self.config.data.copy()

        result = sc_send(self.config.token, f"用户 {self.user_id} 自动阅读脚本开始运行！")
        self.logger.info(result)

        while num <= self.config.max_times:
            self.logger.info(f"用户 {self.user_id} - 第{num}次，共阅读{num * 0.5}分钟")
            
            # 更新数据
            current_time = int(time.time())
            data['ct'] = current_time
            data['ts'] = int(current_time * 1000)
            data['rn'] = random.randint(0, 1000)
            data['sg'] = hashlib.sha256(
                ("" + str(data['ts']) + str(data['rn']) + self.key).encode()
            ).hexdigest()
            data['s'] = self.cal_hash(self.encode_data(data))

            try:
                response = requests.post(
                    self.url,
                    headers=self.config.headers,
                    cookies=self.config.cookies,
                    data=json.dumps(data, separators=(',', ':'))
                )
                res_data = response.json()
                self.logger.info(f"用户 {self.user_id} 响应: {res_data}")

                if 'succ' in res_data:
                    self.logger.info(f"用户 {self.user_id} 数据格式正确，阅读进度有效！")
                    num += 1
                    time.sleep(random.randint(25, 55))
                else:
                    self.logger.warning(f"用户 {self.user_id} 数据格式问题,尝试初始化cookie值")
                    self.config.cookies['wr_skey'] = get_wr_skey(self.config.headers, self.config.cookies)
                    num -= 1

            except Exception as e:
                self.logger.error(f"用户 {self.user_id} 发生错误: {str(e)}")
                time.sleep(60)  # 发生错误时等待1分钟再试

            if num == self.config.max_times:
                result = sc_send(self.config.token, f"用户 {self.user_id} 自动阅读脚本运行已完成！")
                self.logger.info(result)
                break

            data.pop('s', None)


    def start(self) -> None:
        """启动工作线程"""
        self.scheduler.start(
            task=self.process_reading,
            task_name=f"WeRead-{self.user_id}"
        )

    def stop(self) -> None:
        """停止工作线程"""
        self.scheduler.stop()