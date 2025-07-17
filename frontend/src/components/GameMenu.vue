<template>
  <div class="menu-overlay">
    <div class="menu-content">
      <h1 class="menu-title">方格游戏</h1>
      
      <!-- 主菜单 -->
      <div v-if="currentScreen === 'menu'">
        <div class="input-group">
          <label>玩家名称:</label>
          <input 
            v-model="playerName" 
            type="text" 
            placeholder="输入您的名称"
            @keyup.enter="quickJoin"
          >
        </div>
        <div class="input-group">
          <label>房间号:</label>
          <input 
            v-model="roomId" 
            type="text" 
            placeholder="输入房间号或留空创建新房间"
            @keyup.enter="quickJoin"
          >
        </div>
        
        <!-- 房间类型选择器 -->
        <div class="input-group">
          <label>房间类型:</label>
          <div class="room-type-selector">
            <label class="radio-option">
              <input type="radio" v-model="roomType" value="2" />
              <span class="radio-label">
                <div class="room-type-title">2人对战</div>
                <div class="room-type-desc">14x14棋盘，经典对决</div>
              </span>
            </label>
            <label class="radio-option">
              <input type="radio" v-model="roomType" value="4" />
              <span class="radio-label">
                <div class="room-type-title">4人混战</div>
                <div class="room-type-desc">20x20棋盘，多人竞技</div>
              </span>
            </label>
          </div>
        </div>
        
        <div class="control-buttons">
          <button @click="createRoom" class="btn btn-primary">创建房间</button>
          <button @click="joinRoom" class="btn btn-success">加入房间</button>
        </div>
        <div class="game-rules">
          <h3>游戏规则简介</h3>
          <ul>
            <li v-if="roomType === '2'">双人对战，轮流放置方块</li>
            <li v-if="roomType === '4'">四人混战，轮流放置方块</li>
            <li>第一个方块必须触及角落位置</li>
            <li>后续方块只能角对角接触，不能边对边接触</li>
            <li>剩余方块数最少的玩家获胜</li>
          </ul>
        </div>
      </div>
      
      <!-- 等待界面 -->
      <div v-if="currentScreen === 'waiting'">
        <h2 class="menu-title">等待其他玩家加入...</h2>
        <div class="waiting-info">
          <p><strong>房间号:</strong> {{ roomId }}</p>
          <p><strong>房间类型:</strong> {{ maxPlayers }}人游戏</p>
          <p><strong>当前玩家:</strong> {{ currentPlayersCount }}/{{ maxPlayers }}</p>
          <p>分享房间号给朋友，让他们加入游戏！</p>
        </div>
        <div class="loading-animation">
          <div class="spinner"></div>
        </div>
        <button @click="backToMenu" class="btn btn-secondary">返回主菜单</button>
      </div>
      
      <!-- 游戏结束界面 -->
      <div v-if="currentScreen === 'finished'">
        <h2 class="menu-title">游戏结束!</h2>
        <div class="game-result">
          <div v-if="winner === 'tie'" class="result-tie">
            <h3>🤝 平局!</h3>
            <p>多位玩家实力相当！</p>
          </div>
          <div v-else class="result-winner">
            <h3>🎉 玩家{{ winner }}获胜!</h3>
            <p v-if="winner == playerId">恭喜您获得胜利！</p>
            <p v-else>再接再厉，下次一定能赢！</p>
          </div>
          
          <div v-if="finalScores" class="final-scores">
            <h4>最终得分（剩余方块数）</h4>
            <div v-for="(score, playerId) in finalScores" :key="playerId" class="score-item">
              <span>玩家{{ playerId }}: {{ score }} 格</span>
            </div>
          </div>
        </div>
        
        <div class="control-buttons">
          <button @click="restartGame" class="btn btn-success">重新开始</button>
          <button @click="backToMenu" class="btn btn-primary">返回主菜单</button>
        </div>
      </div>
      
      <!-- 消息显示 -->
      <div v-if="message.text" :class="'message ' + message.type">
        {{ message.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  currentScreen: String,
  roomId: String,
  playerId: Number,
  winner: [String, Number],
  finalScores: Object,
  message: Object,
  maxPlayers: {
    type: Number,
    default: 2
  },
  currentPlayersCount: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['create-room', 'join-room', 'restart-game', 'back-to-menu', 'update-player-name', 'update-room-id', 'update-room-type'])

const playerName = ref('')
const roomId = ref(props.roomId || '')
const roomType = ref('2') // 默认选择2人游戏

// 监听外部roomId变化
watch(() => props.roomId, (newVal) => {
  roomId.value = newVal
})

// 更新数据
watch(playerName, (newVal) => {
  emit('update-player-name', newVal)
})

watch(roomId, (newVal) => {
  emit('update-room-id', newVal)
})

watch(roomType, (newVal) => {
  emit('update-room-type', parseInt(newVal))
})

// 创建房间
const createRoom = () => {
  if (!playerName.value.trim()) {
    return
  }
  emit('create-room', parseInt(roomType.value))
}

// 加入房间
const joinRoom = () => {
  if (!playerName.value.trim()) {
    return
  }
  emit('join-room')
}

// 快速加入（回车键）
const quickJoin = () => {
  if (roomId.value.trim()) {
    joinRoom()
  } else {
    createRoom()
  }
}

// 重新开始
const restartGame = () => {
  emit('restart-game')
}

// 返回主菜单
const backToMenu = () => {
  emit('back-to-menu')
}
</script>

<style scoped>
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.menu-content {
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.menu-title {
  font-size: 2.2em;
  margin-bottom: 25px;
  color: #333;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  color: #666;
  font-weight: 500;
}

.input-group input[type="text"] {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s ease;
}

.input-group input[type="text"]:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 10px rgba(0, 123, 255, 0.1);
}

.room-type-selector {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-option {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 15px;
  border: 2px solid #ddd;
  border-radius: 10px;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.radio-option:hover {
  border-color: #007bff;
  background: #e3f2fd;
}

.radio-option input[type="radio"] {
  margin-right: 12px;
  transform: scale(1.2);
}

.radio-option input[type="radio"]:checked + .radio-label {
  color: #007bff;
}

.radio-option:has(input[type="radio"]:checked) {
  border-color: #007bff;
  background: #e3f2fd;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.2);
}

.radio-label {
  text-align: left;
  flex: 1;
}

.room-type-title {
  font-weight: bold;
  font-size: 1.1em;
  margin-bottom: 4px;
}

.room-type-desc {
  font-size: 0.9em;
  color: #666;
}

.control-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
  margin: 25px 0;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 120px;
}

.btn-primary {
  background: linear-gradient(45deg, #007bff, #0056b3);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
}

.btn-secondary {
  background: linear-gradient(45deg, #6c757d, #545b62);
  color: white;
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(108, 117, 125, 0.3);
}

.btn-success {
  background: linear-gradient(45deg, #28a745, #1e7e34);
  color: white;
}

.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
}

.game-rules {
  margin-top: 30px;
  text-align: left;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #007bff;
}

.game-rules h3 {
  margin-bottom: 15px;
  color: #333;
}

.game-rules ul {
  list-style: none;
  padding: 0;
}

.game-rules li {
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
  color: #666;
}

.game-rules li::before {
  content: "▸";
  position: absolute;
  left: 0;
  color: #007bff;
  font-weight: bold;
}

.waiting-info {
  margin: 25px 0;
}

.waiting-info p {
  margin: 10px 0;
  font-size: 1.1em;
}

.loading-animation {
  margin: 30px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.game-result {
  margin: 25px 0;
}

.result-tie, .result-winner {
  margin-bottom: 20px;
}

.result-tie h3 {
  color: #ffc107;
  font-size: 1.8em;
  margin-bottom: 10px;
}

.result-winner h3 {
  color: #28a745;
  font-size: 1.8em;
  margin-bottom: 10px;
}

.final-scores {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin: 20px 0;
}

.final-scores h4 {
  margin-bottom: 15px;
  color: #333;
}

.score-item {
  margin: 8px 0;
  padding: 8px;
  background: white;
  border-radius: 5px;
  font-weight: 500;
}

.message {
  padding: 15px;
  margin: 15px 0;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.message.info {
  background-color: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}
</style> 