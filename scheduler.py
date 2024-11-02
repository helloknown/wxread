from datetime import datetime, timedelta
import time
import pytz
import random
import threading
from typing import Callable, Optional
from config import UserConfig
import logging

class TaskScheduler:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self._schedule_lock = threading.Lock()

    def get_next_run_time(self, start_time: str) -> datetime:
        """解析 start_time，并返回下次运行的时间"""
        # 获取当前日期和指定的时间
        tz_beijing = pytz.timezone("Asia/Shanghai")
        today = datetime.now(tz_beijing)
        run_time = datetime.strptime(start_time, "%H%M").replace(
            year=today.year, month=today.month, day=today.day, tzinfo=tz_beijing
        )

        # 如果时间已过，则设定为明天的该时间
        if run_time <= today:
            run_time += timedelta(days=1)

        # 添加随机延迟（0-30分钟）
        run_time += timedelta(minutes=random.randint(0, 30))
        return run_time

    def calculate_sleep_duration(self, next_run: datetime) -> float:
        """计算距离下次运行需要等待的秒数"""
        tz_beijing = pytz.timezone("Asia/Shanghai")
        now = datetime.now(tz_beijing)
        return max(0, (next_run - now).total_seconds())

    def run_scheduler(self, task: Callable, task_name: str, config: UserConfig) -> None:
        """运行调度器的主循环"""
        while self.running:
            try:
                # 获取下次运行时间
                next_run = self.get_next_run_time(config.start_time)
                sleep_duration = self.calculate_sleep_duration(next_run)
                
                self.logger.info(
                    f"任务 [{task_name}] 将在 {next_run.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"开始执行，等待时间：{sleep_duration / 3600:.2f} 小时"
                )
                
                if sleep_duration > 0:
                    # 使用较小的时间间隔循环检查，使得能够及时响应停止信号
                    while sleep_duration > 0 and self.running:
                        time.sleep(min(60, sleep_duration))
                        sleep_duration -= 60

                if self.running:
                    self.logger.info(f"开始执行任务 [{task_name}]")
                    task()
                    self.logger.info(f"任务 [{task_name}] 执行完成")

            except Exception as e:
                self.logger.error(f"任务 [{task_name}] 执行出错: {str(e)}")
                time.sleep(60)  # 发生错误时等待1分钟再继续

    def start(self, task: Callable, task_name: str, config: UserConfig) -> None:
        """启动调度器"""
        with self._schedule_lock:
            if not self.running:
                self.running = True
                self.thread = threading.Thread(
                    target=self.run_scheduler,
                    args=(task, task_name, config),
                    name=f"Scheduler-{task_name}"
                )
                self.thread.daemon = True
                self.thread.start()
                self.logger.info(f"调度器已启动，任务名称：{task_name}")

    def stop(self) -> None:
        """停止调度器"""
        with self._schedule_lock:
            if self.running:
                self.running = False
                if self.thread and self.thread.is_alive():
                    self.thread.join(timeout=5.0)
                self.logger.info("调度器已停止")
