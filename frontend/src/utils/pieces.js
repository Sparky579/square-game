// 方块定义 - 与后端保持一致
export const PIECES = {
  'piece_1': {
    name: '单格',
    coords: [[0, 0]]
  },
  'piece_2': {
    name: '双格',
    coords: [[0, 0], [1, 0]]
  },
  'piece_3_line': {
    name: '三格直线',
    coords: [[0, 0], [1, 0], [2, 0]]
  },
  'piece_3_l': {
    name: '三格L形',
    coords: [[0, 0], [1, 0], [0, 1]]
  },
  'piece_4_line': {
    name: '四格直线',
    coords: [[0, 0], [1, 0], [2, 0], [3, 0]]
  },
  'piece_4_square': {
    name: '四格方形',
    coords: [[0, 0], [1, 0], [0, 1], [1, 1]]
  },
  'piece_4_l': {
    name: '四格L形',
    coords: [[0, 0], [1, 0], [2, 0], [0, 1]]
  },
  'piece_4_t': {
    name: '四格T形',
    coords: [[0, 0], [1, 0], [2, 0], [1, 1]]
  },
  'piece_4_z': {
    name: '四格Z形',
    coords: [[0, 0], [1, 0], [1, 1], [2, 1]]
  },
  'piece_5_line': {
    name: '五格直线',
    coords: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
  },
  'piece_5_l': {
    name: '五格L形',
    coords: [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1]]
  },
  'piece_5_t': {
    name: '五格T形',
    coords: [[0, 0], [1, 0], [2, 0], [1, 1], [1, 2]]
  },
  'piece_5_plus': {
    name: '五格十字',
    coords: [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]]
  },
  'piece_5_u': {
    name: '五格U形',
    coords: [[0, 0], [2, 0], [0, 1], [1, 1], [2, 1]]
  },
  'piece_5_n': {
    name: '五格N形',
    coords: [[0, 1], [1, 1], [1, 0], [2, 0], [3, 0]]
  },
  'piece_5_y': {
    name: '五格Y形',
    coords: [[0, 1], [1, 0], [1, 1], [2, 1], [3, 1]]
  },
  'piece_5_p': {
    name: '五格P形',
    coords: [[0, 0], [1, 0], [0, 1], [1, 1], [0, 2]]
  },
  'piece_5_w': {
    name: '五格W形',
    coords: [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2]]
  },
  'piece_5_z': {
    name: '五格Z形',
    coords: [[0, 0], [1, 0], [1, 1], [1, 2], [2, 2]]
  },
  'piece_5_v': {
    name: '五格V形',
    coords: [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
  },
  'piece_5_f': {
    name: '五格F形',
    coords: [[1, 0], [2, 0], [0, 1], [1, 1], [1, 2]]
  }
}

// 旋转方块
export function rotatePiece(coords, rotation) {
  if (rotation === 0) return coords
  
  let result = coords
  const rotations = rotation / 90
  
  for (let i = 0; i < rotations; i++) {
    result = result.map(([x, y]) => [-y, x])
  }
  
  return result
}

// 翻转方块
export function flipPiece(coords, flip = false) {
  if (!flip) return coords
  return coords.map(([x, y]) => [-x, y])
}

// 规范化坐标（确保最小坐标为0,0）
export function normalizeCoords(coords) {
  const minX = Math.min(...coords.map(([x]) => x))
  const minY = Math.min(...coords.map(([, y]) => y))
  
  return coords.map(([x, y]) => [x - minX, y - minY])
}

// 获取变换后的方块坐标
export function getTransformedPiece(pieceId, rotation = 0, flip = false) {
  const piece = PIECES[pieceId]
  if (!piece) return null
  
  let coords = [...piece.coords]
  
  // 应用翻转
  if (flip) {
    coords = flipPiece(coords, true)
  }
  
  // 应用旋转
  coords = rotatePiece(coords, rotation)
  
  // 规范化坐标
  coords = normalizeCoords(coords)
  
  return coords
}

// 获取方块边界
export function getPieceBounds(coords) {
  const minX = Math.min(...coords.map(([x]) => x))
  const maxX = Math.max(...coords.map(([x]) => x))
  const minY = Math.min(...coords.map(([, y]) => y))
  const maxY = Math.max(...coords.map(([, y]) => y))
  
  return {
    minX, maxX, minY, maxY,
    width: maxX - minX + 1,
    height: maxY - minY + 1
  }
} 