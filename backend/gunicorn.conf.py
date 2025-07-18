# Gunicorn配置文件
import multiprocessing
import os

# 服务器socket
bind = "0.0.0.0:5000"
backlog = 2048

# SSL配置 - 如果证书文件存在则启用HTTPS
cert_file = "cert.pem"
key_file = "key.pem"
if os.path.exists(cert_file) and os.path.exists(key_file):
    certfile = cert_file
    keyfile = key_file
    print("Gunicorn: 启用HTTPS模式")
else:
    print("Gunicorn: 证书文件不存在，使用HTTP模式")

# Worker进程
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "eventlet"
worker_connections = 1000
timeout = 30
keepalive = 2

# 重启
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# 日志
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 进程名
proc_name = "square_game_backend"

# 用户和组（如果需要）
# user = "www-data"
# group = "www-data"

# 临时目录
tmp_upload_dir = None 