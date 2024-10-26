# 使用官方 Python 镜像作为基础镜像
FROM python:3.10.15

# 设置工作目录
WORKDIR /app

# 将当前目录下所有内容复制到容器的 /app 目录
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 指定要运行的 Python 脚本
CMD ["python", "main.py"]

