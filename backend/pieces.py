# 方块形状定义
# 每个方块用相对坐标表示，(0,0)为基准点

PIECES = {
    # 1格方块
    'piece_1': {
        'name': '单格',
        'size': 1,
        'shapes': [
            [(0, 0)]
        ]
    },
    
    # 2格方块
    'piece_2': {
        'name': '双格',
        'size': 2,
        'shapes': [
            [(0, 0), (1, 0)]
        ]
    },
    
    # 3格方块
    'piece_3_line': {
        'name': '三格直线',
        'size': 3,
        'shapes': [
            [(0, 0), (1, 0), (2, 0)]
        ]
    },
    'piece_3_l': {
        'name': '三格L形',
        'size': 3,
        'shapes': [
            [(0, 0), (1, 0), (0, 1)]
        ]
    },
    
    # 4格方块
    'piece_4_line': {
        'name': '四格直线',
        'size': 4,
        'shapes': [
            [(0, 0), (1, 0), (2, 0), (3, 0)]
        ]
    },
    'piece_4_square': {
        'name': '四格方形',
        'size': 4,
        'shapes': [
            [(0, 0), (1, 0), (0, 1), (1, 1)]
        ]
    },
    'piece_4_l': {
        'name': '四格L形',
        'size': 4,
        'shapes': [
            [(0, 0), (1, 0), (2, 0), (0, 1)]
        ]
    },
    'piece_4_t': {
        'name': '四格T形',
        'size': 4,
        'shapes': [
            [(0, 0), (1, 0), (2, 0), (1, 1)]
        ]
    },
    'piece_4_z': {
        'name': '四格Z形',
        'size': 4,
        'shapes': [
            [(0, 0), (1, 0), (1, 1), (2, 1)]
        ]
    },
    
    # 5格方块
    'piece_5_line': {
        'name': '五格直线',
        'size': 5,
        'shapes': [
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        ]
    },
    'piece_5_l': {
        'name': '五格L形',
        'size': 5,
        'shapes': [
            [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1)]
        ]
    },
    'piece_5_t': {
        'name': '五格T形',
        'size': 5,
        'shapes': [
            [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)]
        ]
    },
    'piece_5_plus': {
        'name': '五格十字',
        'size': 5,
        'shapes': [
            [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
        ]
    },
    'piece_5_u': {
        'name': '五格U形',
        'size': 5,
        'shapes': [
            [(0, 0), (2, 0), (0, 1), (1, 1), (2, 1)]
        ]
    },
    'piece_5_n': {
        'name': '五格N形',
        'size': 5,
        'shapes': [
            [(0, 1), (1, 1), (1, 0), (2, 0), (3, 0)]
        ]
    },
    'piece_5_y': {
        'name': '五格Y形',
        'size': 5,
        'shapes': [
            [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)]
        ]
    },
    'piece_5_p': {
        'name': '五格P形',
        'size': 5,
        'shapes': [
            [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]
        ]
    },
    'piece_5_w': {
        'name': '五格W形',
        'size': 5,
        'shapes': [
            [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
        ]
    },
    'piece_5_z': {
        'name': '五格Z形',
        'size': 5,
        'shapes': [
            [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]
        ]
    },
    'piece_5_v': {
        'name': '五格V形',
        'size': 5,
        'shapes': [
            [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        ]
    },
    'piece_5_f': {
        'name': '五格F形',
        'size': 5,
        'shapes': [
            [(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)]
        ]
    }
}

def rotate_piece(piece_coords, rotation):
    """
    旋转方块
    rotation: 0, 90, 180, 270 度
    """
    if rotation == 0:
        return piece_coords
    elif rotation == 90:
        return [(-y, x) for x, y in piece_coords]
    elif rotation == 180:
        return [(-x, -y) for x, y in piece_coords]
    elif rotation == 270:
        return [(y, -x) for x, y in piece_coords]
    else:
        return piece_coords

def flip_piece(piece_coords, flip_horizontal=True):
    """
    翻转方块
    flip_horizontal: 是否水平翻转，False为垂直翻转
    """
    if flip_horizontal:
        return [(-x, y) for x, y in piece_coords]
    else:
        return [(x, -y) for x, y in piece_coords]

def normalize_piece(piece_coords):
    """
    将方块坐标规范化，确保最小坐标为(0,0)
    """
    min_x = min(x for x, y in piece_coords)
    min_y = min(y for x, y in piece_coords)
    return [(x - min_x, y - min_y) for x, y in piece_coords]

def get_transformed_piece(piece_id, rotation=0, flip=False):
    """
    获取变换后的方块坐标
    """
    if piece_id not in PIECES:
        return None
    
    base_coords = PIECES[piece_id]['shapes'][0].copy()
    
    # 应用翻转
    if flip:
        base_coords = flip_piece(base_coords)
    
    # 应用旋转
    base_coords = rotate_piece(base_coords, rotation)
    
    # 规范化坐标
    base_coords = normalize_piece(base_coords)
    
    return base_coords

def get_piece_bounds(piece_coords):
    """
    获取方块的边界
    """
    min_x = min(x for x, y in piece_coords)
    max_x = max(x for x, y in piece_coords)
    min_y = min(y for x, y in piece_coords)
    max_y = max(y for x, y in piece_coords)
    return min_x, max_x, min_y, max_y

# 获取所有方块ID列表
def get_all_piece_ids():
    return list(PIECES.keys())

# 获取每个玩家的初始方块
def get_player_pieces():
    return get_all_piece_ids() 

# 测试函数
if __name__ == "__main__":
    print("测试五格Z形方块:")
    z_piece = PIECES['piece_5_z']
    print(f"名称: {z_piece['name']}")
    print(f"坐标: {z_piece['shapes'][0]}")
    
    # 测试变换
    transformed = get_transformed_piece('piece_5_z', 0, False)
    print(f"变换后坐标: {transformed}")
    
    print("\n测试单格方块:")
    single_piece = PIECES['piece_1']
    print(f"名称: {single_piece['name']}")
    print(f"坐标: {single_piece['shapes'][0]}")
    
    transformed_single = get_transformed_piece('piece_1', 0, False)
    print(f"变换后坐标: {transformed_single}") 