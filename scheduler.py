from datetime import datetime, timedelta
import time
import pytz
import random
import threading
from typing import Callable, Optional
import logging

class TaskScheduler:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self._schedule_lock = threading.Lock()

    def _get_next_run_time(self) -> datetime:
        """计算下次运行时间"""
        # 当前时间转换为北京时间 (UTC+8)
        tz_beijing = pytz.timezone("Asia/Shanghai")
        now = datetime.now(tz_beijing)
        # 设置下一次启动时间为次日6点
        next_start_time = tz_beijing.localize(datetime(now.year, now.month, now.day, 6, 30))
        # 如果当前时间已经过了6点，计划在下一个6点启动
        if now.hour >= 6 and now.minute >= 30:
            next_start_time += timedelta(days=1)
            
        # 添加随机延迟（0-30分钟）
        next_start_time += timedelta(minutes=random.randint(0, 30))
        return next_start_time

    def _calculate_sleep_duration(self, next_run: datetime) -> float:
        """计算距离下次运行需要等待的秒数"""
        tz_beijing = pytz.timezone("Asia/Shanghai")
        now = datetime.now(tz_beijing)
        return max(0, (next_run - now).total_seconds())

    def _run_scheduler(self, task: Callable, task_name: str) -> None:
        """运行调度器的主循环"""
        while self.running:
            try:
                if self.running:
                    self.logger.info(f"开始执行任务 [{task_name}]")
                    task()
                    self.logger.info(f"任务 [{task_name}] 执行完成")

                # 获取下次运行时间
                next_run = self._get_next_run_time()
                sleep_duration = self._calculate_sleep_duration(next_run)
                
                self.logger.info(
                    f"任务 [{task_name}] 将在 {next_run.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"开始执行，等待时间：{sleep_duration / 3600:.2f} 小时"
                )
                
                if sleep_duration > 0:
                    # 使用较小的时间间隔循环检查，使得能够及时响应停止信号
                    while sleep_duration > 0 and self.running:
                        time.sleep(min(60, sleep_duration))  # 最多睡眠60秒
                        sleep_duration -= 60

            except Exception as e:
                self.logger.error(f"任务 [{task_name}] 执行出错: {str(e)}")
                time.sleep(60)  # 发生错误时等待1分钟再继续

    def start(self, task: Callable, task_name: str) -> None:
        """启动调度器"""
        with self._schedule_lock:
            if not self.running:
                self.running = True
                self.thread = threading.Thread(
                    target=self._run_scheduler,
                    args=(task, task_name),
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
