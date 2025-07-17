# 方格游戏 (Blokus)

一个基于Vue.js和Flask的在线双人方格游戏（角斗士棋），支持实时对战。

## 游戏规则

1. **玩家设置**: 两名玩家，分别从左上角(0,0)和右下角(13,13)开始
2. **方块**: 每个玩家拥有1-5格的所有不同形状方块组合
3. **放置规则**: 
   - 第一个方块必须包含自己的起始角落
   - 后续方块必须与自己已放置的方块角对角接触
   - 不能与自己的方块边对边接触
   - 可以旋转和翻转方块
4. **胜负判断**: 当无法再放置方块时游戏结束，剩余方块数少的玩家获胜

## 项目结构

```
square/
├── backend/              # Flask后端
│   ├── app.py           # 主应用文件
│   ├── game_logic.py    # 游戏逻辑
│   ├── pieces.py        # 方块定义
│   └── requirements.txt # Python依赖
├── frontend/            # Vue.js前端
│   ├── src/             # 源代码
│   │   ├── components/  # Vue组件
│   │   │   ├── GameBoard.vue    # 游戏棋盘组件
│   │   │   ├── PiecePanel.vue   # 方块面板组件
│   │   │   └── GameMenu.vue     # 游戏菜单组件
│   │   ├── utils/       # 工具函数
│   │   │   └── pieces.js        # 方块定义和变换逻辑
│   │   ├── App.vue      # 主应用组件
│   │   └── main.js      # 应用入口
│   ├── index.html       # HTML模板
│   ├── vite.config.js   # Vite配置
│   └── package.json     # 前端依赖
├── start_backend.bat    # Windows后端启动脚本
├── start_frontend.bat   # Windows前端启动脚本
└── README.md           # 项目说明
```

## 安装和运行

### 后端 (Flask)

1. 进入后端目录：
```bash
cd backend
```

2. 安装Python依赖：
```bash
pip install -r requirements.txt
```

3. 运行Flask服务器：
```bash
python app.py
```

服务器将在 http://localhost:5000 启动

### 前端 (Vue.js + Vite)

1. 进入前端目录：
```bash
cd frontend
```

2. 安装Node.js依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```

前端将在 http://localhost:3000 可访问

## 快速启动 (Windows)

1. **启动后端**: 双击 `start_backend.bat`
2. **启动前端**: 双击 `start_frontend.bat`
3. **开始游戏**: 
   - 打开浏览器访问 http://localhost:3000
   - 创建房间或加入现有房间
   - 等待第二个玩家加入即可开始对战

## 游戏功能

### ✅ 已实现功能
- **双人实时对战**: WebSocket实时通信
- **房间创建和加入**: 房间号分享系统
- **完整的游戏规则验证**: 角对角接触、边对边禁止
- **方块旋转和翻转**: 支持90°旋转和镜像翻转
- **有效位置高亮显示**: 智能提示可放置位置
- **方块预览功能**: 鼠标悬停显示放置预览
- **游戏状态实时同步**: 即时更新棋盘状态
- **胜负判断**: 自动计算剩余方块数并判定胜负
- **美观的用户界面**: 现代化组件化设计
- **组件化架构**: 清晰的代码结构和可维护性

### 🎨 界面特色
- **游戏菜单**: 主菜单、等待室、结束界面
- **游戏棋盘**: 14×14网格，星标角落，实时预览
- **方块面板**: 清晰的方块显示，状态指示
- **响应式设计**: 适配不同屏幕尺寸

### 🛠️ 技术特色
- **前端**: Vue 3 + Composition API + Vite
- **后端**: Flask + Socket.IO + 完整游戏逻辑
- **通信**: WebSocket实时双向通信
- **状态管理**: 响应式游戏状态同步
- **模块化**: 组件化开发，代码清晰

## API接口

### REST API
- `GET /api/health` - 健康检查
- `POST /api/create-room` - 创建游戏房间
- `GET /api/room/<room_id>` - 获取房间信息

### WebSocket事件
- `join_room` - 加入房间
- `place_piece` - 放置方块
- `get_valid_positions` - 获取有效位置
- `game_updated` - 游戏状态更新
- `game_over` - 游戏结束

## 开发指南

### 前端开发
```bash
cd frontend
npm run dev    # 开发服务器
npm run build  # 构建生产版本
npm run preview # 预览构建结果
```

### 后端开发
```bash
cd backend
python app.py  # 启动开发服务器
```

## 注意事项

- 确保Node.js版本 >= 16
- 确保Python版本 >= 3.8
- 后端端口5000，前端端口3000
- 游戏需要两个玩家才能开始
- 建议使用现代浏览器以获得最佳体验

## 开发计划

未来可能的改进：
- [ ] 添加AI对手
- [ ] 增加观战模式
- [ ] 添加游戏回放功能
- [ ] 支持更多玩家（标准Blokus为4人游戏）
- [ ] 增加排行榜和统计功能
- [ ] 添加音效和动画
- [ ] 移动端适配优化 