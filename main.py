# main.py
import os
import time
from pathlib import Path
from config import load_config
from weread_worker import WeReadWorker

def main():
    # 创建日志目录
    Path("logs").mkdir(exist_ok=True)
    
    # 获取所有用户配置文件
    user_configs = []
    user_dir = Path("users")
    for config_file in user_dir.glob("*.json"):
        try:
            config = load_config(str(config_file))
            user_configs.append((config, config_file.stem))
        except Exception as e:
            print(f"Error loading config {config_file}: {e}")
            continue

    # 创建并启动所有工作线程
    workers = []
    for config, user_id in user_configs:
        worker = WeReadWorker(config, user_id)
        worker.start()
        workers.append(worker)

    try:
        # 保持主线程运行
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("正在停止所有工作线程...")
        for worker in workers:
            worker.stop()


if __name__ == "__main__":
    main()