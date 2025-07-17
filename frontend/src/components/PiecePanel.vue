<template>
  <div class="pieces-panel">
    <div class="player-section">
      <div :class="'player-header player' + playerId + ' ' + (isMyTurn ? 'current' : '')">
        您的方块 (玩家{{ playerId }})
      </div>
      <div class="pieces-grid">
        <div 
          v-for="pieceId in myPieces" 
          :key="pieceId"
          :class="'piece-item ' + (selectedPiece === pieceId ? 'selected' : '')"
          @click="selectPiece(pieceId)"
        >
          <div class="piece-display">
            <div class="piece-grid" :style="getPieceGridStyle(pieceId)">
              <div 
                v-for="cell in getPieceCells(pieceId)" 
                :key="'piece-' + cell.x + '-' + cell.y"
                class="piece-cell"
                :style="{ gridColumn: cell.x + 1, gridRow: cell.y + 1 }"
              >
              </div>
            </div>
          </div>
          <div class="piece-name">{{ PIECES[pieceId]?.name }}</div>
        </div>
      </div>
    </div>

    <div v-if="selectedPiece && gameState !== 'finished'" class="controls">
      <div class="control-group">
        <label>选中方块: {{ PIECES[selectedPiece]?.name }}</label>
      </div>
      <div class="control-group">
        <label>变换操作:</label>
        <div class="control-buttons">
          <button @click="rotatePiece" class="btn btn-primary" :disabled="!isMyTurn">旋转</button>
          <button @click="flipPiece" class="btn btn-secondary" :disabled="!isMyTurn">翻转</button>
        </div>
      </div>
      <div class="control-group">
        <label>当前状态:</label>
        <div class="status-info">
          旋转: {{ rotation }}° | 翻转: {{ flip ? '是' : '否' }}
        </div>
      </div>
    </div>

    <div v-if="gameState === 'finished'" class="controls">
      <div class="game-result">
        <h3>游戏结束</h3>
        <p>查看终局盘面，点击下方按钮重新开始游戏</p>
      </div>
      <button @click="restartGame" class="btn btn-success">重新开始</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { PIECES, getPieceBounds, getTransformedPiece } from '../utils/pieces.js'

const props = defineProps({
  myPieces: Array,
  selectedPiece: String,
  playerId: Number,
  isMyTurn: Boolean,
  rotation: Number,
  flip: Boolean,
  gameState: String
})

const emit = defineEmits(['select-piece', 'rotate-piece', 'flip-piece', 'restart-game'])

// 选择方块
const selectPiece = (pieceId) => {
  emit('select-piece', pieceId)
}

// 旋转方块
const rotatePiece = () => {
  emit('rotate-piece')
}

// 翻转方块
const flipPiece = () => {
  emit('flip-piece')
}

// 重新开始
const restartGame = () => {
  emit('restart-game')
}

// 获取方块网格样式
const getPieceGridStyle = (pieceId) => {
  const piece = PIECES[pieceId]
  if (!piece) return {}
  
  // 如果是选中的方块，使用变换后的坐标
  let coords = piece.coords
  if (pieceId === props.selectedPiece) {
    const transformedCoords = getTransformedPiece(pieceId, props.rotation, props.flip)
    if (transformedCoords) {
      coords = transformedCoords
    }
  }
  
  const bounds = getPieceBounds(coords)
  
  return {
    gridTemplateColumns: `repeat(${bounds.width}, 14px)`,
    gridTemplateRows: `repeat(${bounds.height}, 14px)`,
    gap: '1px',
    width: `${bounds.width * 14 + (bounds.width - 1)}px`,
    height: `${bounds.height * 14 + (bounds.height - 1)}px`
  }
}

// 获取方块格子
const getPieceCells = (pieceId) => {
  const piece = PIECES[pieceId]
  if (!piece) return []
  
  // 如果是选中的方块，使用变换后的坐标
  let coords = piece.coords
  if (pieceId === props.selectedPiece) {
    const transformedCoords = getTransformedPiece(pieceId, props.rotation, props.flip)
    if (transformedCoords) {
      coords = transformedCoords
    }
  }
  
  return coords.map(([x, y]) => ({ x, y }))
}
</script>

<style scoped>
.pieces-panel {
  width: 450px;
  background-color: #f8f9fa;
  border-left: 1px solid #dee2e6;
  padding: 20px;
  overflow-y: auto;
  max-height: 100vh;
}

.player-section {
  margin-bottom: 30px;
}

.player-header {
  background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%);
  color: #333;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 15px;
  text-align: center;
  font-weight: bold;
}

.player-header.current {
  background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* 根据玩家ID调整头部颜色 */
.player-header.player1 {
  background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%);
}

.player-header.player2 {
  background: linear-gradient(90deg, #4ecdc4 0%, #44a08d 100%);
  color: white;
}

.player-header.player3 {
  background: linear-gradient(90deg, #45b7d1 0%, #96c93d 100%);
  color: white;
}

.player-header.player4 {
  background: linear-gradient(90deg, #96ceb4 0%, #ffecd2 100%);
}

.player-header.current {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transform: scale(1.02);
}

.pieces-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
  gap: 12px;
}

.piece-item {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.piece-item:hover {
  border-color: #007bff;
  transform: scale(1.05);
}

.piece-item.selected {
  border-color: #28a745;
  background-color: #e8f5e8;
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.piece-display {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  margin-bottom: 8px;
}

.piece-grid {
  display: grid;
  background-color: transparent;
}

.piece-cell {
  background-color: #007bff;
  border-radius: 2px;
  width: 14px;
  height: 14px;
}

.piece-name {
  font-size: 0.8em;
  color: #666;
  font-weight: 500;
}

.controls {
  background: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  margin-top: 20px;
}

.control-group {
  margin-bottom: 15px;
}

.control-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.control-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9em;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 80px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: translateY(-1px);
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
  transform: translateY(-1px);
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #1e7e34;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.game-result {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  margin-bottom: 15px;
}

.game-result h3 {
  margin: 0 0 10px 0;
  font-size: 1.5em;
}

.game-result p {
  margin: 0;
  opacity: 0.9;
}

.status-info {
  font-size: 0.9em;
  color: #666;
  background: #f8f9fa;
  padding: 8px 12px;
  border-radius: 5px;
  text-align: center;
}
</style> 