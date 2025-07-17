@echo off

REM 激活虚拟环境（如果使用的话）
REM call venv\Scripts\activate

REM 切换到backend目录
cd /d "%~dp0"

REM 使用gunicorn启动应用
echo 正在使用Gunicorn启动Square游戏后端...
gunicorn --config gunicorn.conf.py app:socketio

pause 