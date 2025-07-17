#!/bin/bash

# 激活虚拟环境（如果使用的话）
# source venv/bin/activate

# 切换到backend目录
cd "$(dirname "$0")"

# 使用gunicorn启动应用
echo "正在使用Gunicorn启动Square游戏后端..."
gunicorn --config gunicorn.conf.py app:socketio 