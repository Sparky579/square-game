@echo off
echo 启动方格游戏后端服务器...
cd backend
pip install -r requirements.txt
python app.py
pause 