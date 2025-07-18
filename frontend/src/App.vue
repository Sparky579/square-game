<template>
  <div class="app">
    <!-- 游戏菜单（主菜单、等待、结束界面） -->
    <GameMenu
      v-if="gameState.currentScreen !== 'playing'"
      :current-screen="gameState.currentScreen"
      :room-id="gameState.roomId"
      :player-id="gameState.playerId"
      :winner="gameState.gameData?.winner"
      :final-scores="finalScores"
      :message="gameState.message"
      :max-players="maxPlayers"
      :current-players-count="currentPlayersCount"
      @create-room="createRoom"
      @join-room="joinRoom"
      @restart-game="restartGame"
      @back-to-menu="backToMenu"
      @update-player-name="updatePlayerName"
      @update-room-id="updateRoomId"
      @update-room-type="updateRoomType"
    />

    <!-- 游戏界面 -->
    <div v-if="gameState.currentScreen === 'playing' || gameState.currentScreen === 'finished'" class="game-container">
      <div class="game-header">
        <h1>方格游戏</h1>
        <div class="game-status">
          <span v-if="gameState.currentScreen === 'playing'">
            当前回合: 玩家{{ currentPlayer }} 
            <span v-if="isMyTurn" class="my-turn">(您的回合)</span>
            <span class="players-info">({{ maxPlayers }}人游戏)</span>
          </span>
          <span v-if="gameState.currentScreen === 'finished'" class="game-finished">
            🎉 游戏结束！
            <span v-if="gameState.gameData?.winner && gameState.gameData.winner !== 'tie'">
              玩家{{ gameState.gameData.winner }}获胜！
            </span>
            <span v-else-if="gameState.gameData?.winner === 'tie'">
              平局！
            </span>
          </span>
        </div>
        <div v-if="gameState.message.text" :class="'message ' + gameState.message.type">
          {{ gameState.message.text }}
        </div>
      </div>

      <div class="main-content">
        <!-- 游戏棋盘 -->
        <GameBoard
          :game-data="gameState.gameData"
          :valid-positions="gameState.validPositions"
          :selected-piece="gameState.selectedPiece"
          :preview-position="previewPosition"
          :preview-coords="previewCoords"
          :preview-valid="previewValid"
          @place-piece="placePiece"
          @show-preview="showPreview"
          @hide-preview="hidePreview"
        />

        <!-- 方块面板 -->
        <PiecePanel
          :my-pieces="myPieces"
          :selected-piece="gameState.selectedPiece"
          :player-id="gameState.playerId"
          :is-my-turn="isMyTurn"
          :rotation="gameState.rotation"
          :flip="gameState.flip"
          :game-state="gameState.currentScreen"
          @select-piece="selectPiece"
          @rotate-piece="rotatePiece"
          @flip-piece="flipPiece"
          @restart-game="restartGame"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted, onUnmounted, ref } from 'vue'
import { io } from 'socket.io-client'
import GameMenu from './components/GameMenu.vue'
import GameBoard from './components/GameBoard.vue'
import PiecePanel from './components/PiecePanel.vue'
import { getTransformedPiece, PIECES } from './utils/pieces.js'
import { config } from './config.js'

// 游戏状态
const gameState = reactive({
  currentScreen: 'menu', // menu, waiting, playing, finished
  socket: null,
  roomId: '',
  playerId: null,
  playerName: '',
  roomType: 2, // 房间类型：2人或4人
  gameData: null,
  selectedPiece: null,
  validPositions: [],
  rotation: 0,
  flip: false,
  message: { text: '', type: '' },
  // 房间状态
  roomInfo: {
    currentPlayersCount: 0,
    maxPlayers: 2
  }
})

// 预览状态
const previewPosition = ref(null)
const previewCoords = ref(null)
const previewValid = ref(false) // 新增：用于标记预览位置是否有效

// 计算属性
const currentPlayer = computed(() => {
  return gameState.gameData?.current_player
})

const isMyTurn = computed(() => {
  return gameState.gameData?.current_player === gameState.playerId
})

const myPieces = computed(() => {
  if (!gameState.gameData || !gameState.playerId) return []
  return gameState.gameData.players[gameState.playerId]?.pieces || []
})

const finalScores = computed(() => {
  if (!gameState.gameData) return null
  // 计算最终分数
  const scores = {}
  Object.keys(gameState.gameData.players).forEach(playerId => {
    const pieces = gameState.gameData.players[playerId].pieces || []
    // 计算剩余方块的总格数
    let totalSquares = 0
    pieces.forEach(pieceId => {
      const piece = PIECES[pieceId]
      if (piece) {
        totalSquares += piece.coords.length
      }
    })
    scores[playerId] = totalSquares
  })
  return scores
})

// 获取当前玩家数量
const currentPlayersCount = computed(() => {
  // 如果游戏已开始，从gameData获取
  if (gameState.gameData && gameState.gameData.players) {
    return Object.keys(gameState.gameData.players).length
  }
  // 否则从roomInfo获取
  return gameState.roomInfo.currentPlayersCount
})

// 获取最大玩家数
const maxPlayers = computed(() => {
  if (gameState.gameData?.max_players) {
    return gameState.gameData.max_players
  }
  return gameState.roomInfo.maxPlayers
})

// Socket.IO 连接
const connectSocket = () => {
  const serverUrl = config.getSocketUrl()
  console.log('连接到服务器:', serverUrl)
  
  // Socket.IO配置选项
  const socketOptions = {
    // 传输方式配置
    transports: ['polling', 'websocket'], // 优先使用polling，避免WebSocket的证书问题
    upgrade: true,
    
    // 连接配置
    timeout: 20000,
    forceNew: true,
    autoConnect: true,
    
    // 轮询配置
    polling: {
      extraHeaders: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
      }
    },
    
    // 重连配置
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    maxReconnectionAttempts: 5,
    randomizationFactor: 0.5
  }
  
  // 如果是HTTPS，添加额外的处理
  if (config.server.useSSL) {
    console.log('使用HTTPS连接，配置自签名证书支持')
    // 注意：这些选项主要用于Node.js环境，浏览器中会被忽略
    Object.assign(socketOptions, {
      rejectUnauthorized: false,
      secure: true,
      // 强制使用polling传输，因为WebSocket在自签名证书下可能有问题
      transports: ['polling']
    })
  }
  
  gameState.socket = io(serverUrl, socketOptions)

  gameState.socket.on('connect', () => {
    console.log('已连接到服务器')
  })

  gameState.socket.on('joined_room', (data) => {
    gameState.playerId = data.player_id
    gameState.currentScreen = 'waiting'
    // 更新房间信息
    gameState.roomInfo.currentPlayersCount = data.players_count
    gameState.roomInfo.maxPlayers = data.max_players
    showMessage(`已加入房间 ${data.room_id}`, 'success')
  })

  gameState.socket.on('player_joined', (data) => {
    // 更新房间信息
    gameState.roomInfo.currentPlayersCount = data.players_count
    gameState.roomInfo.maxPlayers = data.max_players
    showMessage(`${data.player_name} 加入了房间`, 'info')
  })

  gameState.socket.on('game_started', (data) => {
    gameState.gameData = data.game_state
    gameState.currentScreen = 'playing'
    showMessage('游戏开始！', 'success')
  })

  gameState.socket.on('game_updated', (data) => {
    gameState.gameData = data.game_state
    gameState.validPositions = []
    gameState.selectedPiece = null
    previewPosition.value = null
    previewCoords.value = null
    previewValid.value = false // 清除有效性标记
  })

  gameState.socket.on('game_over', (data) => {
    gameState.gameData = { ...gameState.gameData, winner: data.winner }
    gameState.currentScreen = 'finished'
    showMessage(data.message, 'info')
  })

  gameState.socket.on('valid_positions', (data) => {
    console.log('收到valid_positions:', data)
    gameState.validPositions = data.positions
    console.log('设置validPositions:', gameState.validPositions)
    // 如果有预览位置，更新预览
    if (previewPosition.value) {
      updatePreview(previewPosition.value[0], previewPosition.value[1])
    }
  })

  gameState.socket.on('error', (data) => {
    showMessage(data.message, 'error')
  })

  gameState.socket.on('move_error', (data) => {
    showMessage(data.message, 'error')
  })

  gameState.socket.on('player_left', (data) => {
    // 更新房间信息
    gameState.roomInfo.currentPlayersCount = data.players_count
    gameState.roomInfo.maxPlayers = data.max_players
    showMessage(data.message, 'info')
  })
}

// 显示消息
const showMessage = (text, type = 'info') => {
  gameState.message = { text, type }
  setTimeout(() => {
    gameState.message = { text: '', type: '' }
  }, 3000)
}

// 创建房间
const createRoom = async (roomType = 2) => {
  try {
    gameState.roomType = roomType
    // 设置房间信息
    gameState.roomInfo.maxPlayers = roomType
    gameState.roomInfo.currentPlayersCount = 0
    
    const apiUrl = `${config.getApiUrl()}/create-room`
    console.log('创建房间请求URL:', apiUrl)
    
    // 配置fetch选项以处理自签名证书
    const fetchOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ max_players: roomType })
    }
    
    // 如果是HTTPS，添加额外配置（主要用于开发环境）
    if (config.server.useSSL) {
      console.log('使用HTTPS API请求')
      // 注意：在浏览器中，无法直接设置SSL选项，需要手动信任证书
    }
    
    const response = await fetch(apiUrl, fetchOptions)
    const data = await response.json()
    if (data.error) {
      showMessage(data.error, 'error')
      return
    }
    gameState.roomId = data.room_id
    joinRoom()
  } catch (error) {
    showMessage('创建房间失败', 'error')
  }
}

// 加入房间
const joinRoom = () => {
  if (!gameState.roomId || !gameState.playerName) {
    showMessage('请输入房间号和玩家名称', 'error')
    return
  }

  gameState.socket.emit('join_room', {
    room_id: gameState.roomId,
    player_name: gameState.playerName
  })
}

// 选择方块
const selectPiece = (pieceId) => {
  if (!isMyTurn.value || !myPieces.value.includes(pieceId)) return
  
  gameState.selectedPiece = pieceId
  gameState.rotation = 0
  gameState.flip = false
  hidePreview() // 清除之前的预览
  getValidPositions()
}

// 获取有效位置
const getValidPositions = () => {
  if (!gameState.selectedPiece) return

  gameState.socket.emit('get_valid_positions', {
    piece_id: gameState.selectedPiece,
    rotation: gameState.rotation,
    flip: gameState.flip
  })
}

// 旋转方块
const rotatePiece = () => {
  gameState.rotation = (gameState.rotation + 90) % 360
  getValidPositions()
  // 如果当前有预览位置，更新预览显示
  if (previewPosition.value) {
    updatePreview(previewPosition.value[0], previewPosition.value[1])
  }
}

// 翻转方块
const flipPiece = () => {
  gameState.flip = !gameState.flip
  getValidPositions()
  // 如果当前有预览位置，更新预览显示
  if (previewPosition.value) {
    updatePreview(previewPosition.value[0], previewPosition.value[1])
  }
}

// 更新预览
const updatePreview = (x, y) => {
  if (!gameState.selectedPiece || !isMyTurn.value) return
  
  console.log('updatePreview 调用，位置:', x, y)
  console.log('当前validPositions:', gameState.validPositions)
  
  const isValidPosition = gameState.validPositions.some(pos => pos[0] === x && pos[1] === y)
  console.log('isValidPosition:', isValidPosition)
  
  // 设置预览位置和坐标，不管是否有效
  previewPosition.value = [x, y]
  // 获取变换后的方块坐标用于预览
  const transformedCoords = getTransformedPiece(
    gameState.selectedPiece, 
    gameState.rotation, 
    gameState.flip
  )
  previewCoords.value = transformedCoords || []
  
  // 添加有效性标记
  previewValid.value = isValidPosition
  
  console.log('设置预览:', previewPosition.value, previewCoords.value, '有效:', previewValid.value)
}

// 显示预览
const showPreview = (x, y) => {
  updatePreview(x, y)
}

// 隐藏预览
const hidePreview = () => {
  previewPosition.value = null
  previewCoords.value = null
  previewValid.value = false // 隐藏时也清除有效性标记
}

// 放置方块
const placePiece = (x, y) => {
  if (!gameState.selectedPiece || !isMyTurn.value) return
  
  const isValidPosition = gameState.validPositions.some(pos => pos[0] === x && pos[1] === y)
  if (!isValidPosition) {
    showMessage('无效的放置位置', 'error')
    return
  }

  gameState.socket.emit('place_piece', {
    piece_id: gameState.selectedPiece,
    position: [x, y],
    rotation: gameState.rotation,
    flip: gameState.flip
  })
}

// 重新开始
const restartGame = () => {
  gameState.currentScreen = 'menu'
  gameState.gameData = null
  gameState.selectedPiece = null
  gameState.validPositions = []
  gameState.roomId = ''
  gameState.playerId = null
  // 重置房间信息
  gameState.roomInfo.currentPlayersCount = 0
  gameState.roomInfo.maxPlayers = 2
  previewPosition.value = null
  previewCoords.value = null
  previewValid.value = false // 重新开始时也清除有效性标记
  if (gameState.socket) {
    gameState.socket.disconnect()
  }
  connectSocket()
}

// 返回主菜单
const backToMenu = () => {
  restartGame()
}

// 更新玩家名称
const updatePlayerName = (name) => {
  gameState.playerName = name
}

// 更新房间号
const updateRoomId = (roomId) => {
  gameState.roomId = roomId
}

// 更新房间类型
const updateRoomType = (roomType) => {
  gameState.roomType = roomType
}

// 生命周期
onMounted(() => {
  connectSocket()
})

onUnmounted(() => {
  if (gameState.socket) {
    gameState.socket.disconnect()
  }
})
</script>

<style scoped>
.app {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.game-container {
  max-width: 1400px;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  height: 90vh;
  display: flex;
  flex-direction: column;
}

.game-header {
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  padding: 20px;
  text-align: center;
  flex-shrink: 0;
}

.game-header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
}

.game-status {
  font-size: 1.2em;
  margin-bottom: 10px;
}

.my-turn {
  color: #ffeb3b;
  font-weight: bold;
}

.players-info {
  color: #ffffff;
  opacity: 0.8;
  margin-left: 10px;
}

.game-finished {
  color: #4CAF50; /* 绿色，表示游戏结束 */
  font-weight: bold;
  font-size: 1.2em;
}

.main-content {
  display: flex;
  flex: 1;
  min-height: 0;
}

.main-content .board-section {
  flex: 0 0 50%; /* 固定棋盘区域宽度为500px */
}

.main-content .pieces-panel {
  flex: 1; /* 方格面板占据剩余空间 */
}

.message {
  padding: 10px 20px;
  margin: 10px auto;
  border-radius: 5px;
  max-width: 400px;
  font-weight: 500;
}

.message.success {
  background-color: rgba(212, 237, 218, 0.9);
  color: #155724;
  border: 1px solid rgba(195, 230, 203, 0.9);
}

.message.error {
  background-color: rgba(248, 215, 218, 0.9);
  color: #721c24;
  border: 1px solid rgba(245, 198, 203, 0.9);
}

.message.info {
  background-color: rgba(209, 236, 241, 0.9);
  color: #0c5460;
  border: 1px solid rgba(190, 229, 235, 0.9);
}
</style> 