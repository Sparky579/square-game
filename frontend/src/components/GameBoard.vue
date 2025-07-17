<template>
  <div class="board-section">
    <div class="game-board" :style="getBoardStyle()">
      <div v-for="y in boardSize" :key="'row-' + y" style="display: contents;">
        <div 
          v-for="x in boardSize" 
          :key="'cell-' + x + '-' + y" 
          :class="getCellClass(x-1, y-1)"
          @click="placePiece(x-1, y-1)"
          @mouseenter="showPreview(x-1, y-1)"
          @mouseleave="hidePreview"
        >
          <!-- 预览方块 -->
          <div v-if="isPreviewCell(x-1, y-1)" :class="getPreviewClass()"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  gameData: Object,
  validPositions: Array,
  selectedPiece: String,
  previewPosition: Array,
  previewCoords: Array,
  previewValid: Boolean
})

const emit = defineEmits(['place-piece', 'show-preview', 'hide-preview'])

// 计算棋盘大小
const boardSize = computed(() => {
  return props.gameData?.board_size || 14
})

// 计算棋盘样式
const getBoardStyle = () => {
  const size = boardSize.value
  const cellSize = size === 20 ? 26 : 32 // 4人游戏用较小的格子
  return {
    gridTemplateColumns: `repeat(${size}, ${cellSize}px)`,
    gridTemplateRows: `repeat(${size}, ${cellSize}px)`
  }
}

// 获取棋盘格子类名
const getCellClass = (x, y) => {
  const classes = ['board-cell']
  
  // 玩家方块颜色
  const cellValue = props.gameData?.board?.[y]?.[x]
  if (cellValue === 1) classes.push('player1')
  if (cellValue === 2) classes.push('player2')
  if (cellValue === 3) classes.push('player3')
  if (cellValue === 4) classes.push('player4')
  
  const isValidPos = props.validPositions?.some(pos => pos[0] === x && pos[1] === y)
  if (isValidPos) classes.push('valid-position')
  
  // 根据游戏人数添加角落标记
  const maxPlayers = props.gameData?.max_players || 2
  if (maxPlayers === 2) {
    // 2人游戏：左上角和右下角
    if ((x === 0 && y === 0) || (x === boardSize.value - 1 && y === boardSize.value - 1)) {
      classes.push('corner-start')
    }
  } else if (maxPlayers === 4) {
    // 4人游戏：四个角落
    if ((x === 0 && y === 0) || 
        (x === boardSize.value - 1 && y === 0) ||
        (x === boardSize.value - 1 && y === boardSize.value - 1) ||
        (x === 0 && y === boardSize.value - 1)) {
      classes.push('corner-start')
    }
  }
  
  return classes.join(' ')
}

// 检查是否是预览格子
const isPreviewCell = (x, y) => {
  if (!props.previewPosition || !props.previewCoords) return false
  
  const [px, py] = props.previewPosition
  return props.previewCoords.some(([dx, dy]) => px + dx === x && py + dy === y)
}

// 获取预览方块的类名
const getPreviewClass = () => {
  if (props.previewValid) {
    return 'preview-piece valid-preview'
  } else {
    return 'preview-piece invalid-preview'
  }
}

// 放置方块
const placePiece = (x, y) => {
  emit('place-piece', x, y)
}

// 显示预览
const showPreview = (x, y) => {
  emit('show-preview', x, y)
}

// 隐藏预览
const hidePreview = () => {
  emit('hide-preview')
}
</script>

<style scoped>
.board-section {
  flex: 1;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.game-board {
  display: grid;
  gap: 1px;
  background-color: #333;
  border: 3px solid #333;
  border-radius: 8px;
}

.board-cell {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.board-cell:hover {
  background-color: #e0e0e0;
}

.board-cell.player1 {
  background-color: #ff6b6b;
}

.board-cell.player2 {
  background-color: #4ecdc4;
}

.board-cell.player3 {
  background-color: #45b7d1;
}

.board-cell.player4 {
  background-color: #96ceb4;
}

.board-cell.valid-position {
  background-color: #95e1d3 !important;
  box-shadow: inset 0 0 10px rgba(0, 200, 0, 0.5);
}

.board-cell.corner-start::after {
  content: "★";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #ffd700;
  font-size: 16px;
}

.preview-piece {
  position: absolute;
  top: 2px;
  left: 2px;
  width: calc(100% - 4px);
  height: calc(100% - 4px);
  background-color: rgba(76, 175, 80, 0.7);
  border: 2px solid #4caf50;
  border-radius: 3px;
  pointer-events: none;
  z-index: 10;
}

.preview-piece.valid-preview {
  background-color: rgba(76, 175, 80, 0.7);
  border: 2px solid #4caf50;
}

.preview-piece.invalid-preview {
  background-color: rgba(255, 107, 107, 0.7);
  border: 2px solid #ff6b6b;
}
</style> 