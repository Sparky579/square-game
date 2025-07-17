from pieces import PIECES, get_transformed_piece, get_player_pieces
import copy

class Game:
    def __init__(self, max_players=2):
        self.max_players = max_players
        self.board_size = 20 if max_players == 4 else 14
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.players = {}
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
    def add_player(self, player_id, player_num):
        """添加玩家"""
        self.players[player_num] = {
            'id': player_id,
            'pieces': get_player_pieces().copy(),
            'placed_pieces': [],
            'score': 0,
            'first_move': True
        }
    
    def is_valid_position(self, piece_coords, board_x, board_y, player_num):
        """检查方块是否可以放置在指定位置"""
        placed_positions = []
        
        # 检查每个方块格子是否在棋盘内且为空
        for dx, dy in piece_coords:
            x, y = board_x + dx, board_y + dy
            if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
                return False, "超出棋盘边界"
            if self.board[y][x] != 0:
                return False, "位置已被占用"
            placed_positions.append((x, y))
        
        # 检查边对边接触（不允许）
        for x, y in placed_positions:
            # 检查四个相邻位置
            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[ny][nx] == player_num:
                        return False, "不能与自己的方块边对边接触"
        
        # 对于第一次放置的特殊规则
        if self.players[player_num]['first_move']:
            # 根据玩家数量和玩家编号确定起始位置
            if self.max_players == 2:
                # 2人游戏：玩家1从左上角，玩家2从右下角
                if player_num == 1:
                    if (0, 0) not in placed_positions:
                        return False, "第一个方块必须包含左上角位置(0,0)"
                elif player_num == 2:
                    if (self.board_size-1, self.board_size-1) not in placed_positions:
                        return False, "第一个方块必须包含右下角位置"
            else:
                # 4人游戏：玩家分别从四个角开始
                corner_positions = {
                    1: (0, 0),  # 左上角
                    2: (self.board_size-1, 0),  # 右上角
                    3: (self.board_size-1, self.board_size-1),  # 右下角
                    4: (0, self.board_size-1)   # 左下角
                }
                required_corner = corner_positions.get(player_num)
                if required_corner and required_corner not in placed_positions:
                    return False, f"第一个方块必须包含角落位置{required_corner}"
        else:
            # 非第一次放置：必须与自己的方块角对角接触
            corner_touch = False
            for x, y in placed_positions:
                # 检查四个对角位置
                for nx, ny in [(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[ny][nx] == player_num:
                            corner_touch = True
                            break
                if corner_touch:
                    break
            
            if not corner_touch:
                return False, "必须与自己的方块角对角接触"
        
        return True, "可以放置"
    
    def place_piece(self, player_num, piece_id, board_x, board_y, rotation=0, flip=False):
        """在棋盘上放置方块"""
        if self.game_over:
            return {"success": False, "message": "游戏已结束"}
        
        if self.current_player != player_num:
            return {"success": False, "message": "不是您的回合"}
        
        if player_num not in self.players:
            return {"success": False, "message": "玩家不存在"}
        
        if piece_id not in self.players[player_num]['pieces']:
            return {"success": False, "message": "方块已使用或不存在"}
        
        # 获取变换后的方块坐标
        piece_coords = get_transformed_piece(piece_id, rotation, flip)
        if piece_coords is None:
            return {"success": False, "message": "无效的方块"}
        
        # 检查是否可以放置
        valid, message = self.is_valid_position(piece_coords, board_x, board_y, player_num)
        if not valid:
            return {"success": False, "message": message}
        
        # 放置方块
        for dx, dy in piece_coords:
            x, y = board_x + dx, board_y + dy
            self.board[y][x] = player_num
        
        # 更新玩家状态
        self.players[player_num]['pieces'].remove(piece_id)
        self.players[player_num]['placed_pieces'].append({
            'piece_id': piece_id,
            'position': (board_x, board_y),
            'rotation': rotation,
            'flip': flip,
            'coords': piece_coords
        })
        self.players[player_num]['first_move'] = False
        
        # 切换到下一个玩家
        self.switch_player()
        
        # 检查游戏是否结束
        self.check_game_over()
        
        return {"success": True, "message": "方块放置成功"}
    
    def switch_player(self):
        """切换当前玩家"""
        # 循环到下一个玩家
        current_index = self.current_player - 1
        next_index = (current_index + 1) % self.max_players
        self.current_player = next_index + 1
    
    def can_player_place_any_piece(self, player_num):
        """检查玩家是否还能放置任何方块"""
        if player_num not in self.players:
            return False
        
        remaining_pieces = self.players[player_num]['pieces']
        
        for piece_id in remaining_pieces:
            # 尝试所有可能的变换
            for rotation in [0, 90, 180, 270]:
                for flip in [False, True]:
                    piece_coords = get_transformed_piece(piece_id, rotation, flip)
                    if piece_coords is None:
                        continue
                    
                    # 尝试棋盘上的每个位置
                    for board_x in range(self.board_size):
                        for board_y in range(self.board_size):
                            valid, _ = self.is_valid_position(piece_coords, board_x, board_y, player_num)
                            if valid:
                                return True
        
        return False
    
    def check_game_over(self):
        """检查游戏是否结束"""
        # 检查所有玩家是否都无法放置方块
        players_can_play = {}
        all_finished = True
        
        for player_num in self.players:
            can_play = self.can_player_place_any_piece(player_num)
            players_can_play[player_num] = can_play
            if can_play:
                all_finished = False
        
        # 如果所有玩家都无法放置方块，游戏结束
        if all_finished:
            self.game_over = True
            self.determine_winner()
            return
        
        # 如果当前玩家无法放置方块，跳过其回合
        if not players_can_play.get(self.current_player, False):
            # 寻找下一个可以放置方块的玩家
            attempts = 0
            while attempts < self.max_players:
                self.switch_player()
                attempts += 1
                if players_can_play.get(self.current_player, False):
                    break
            
            # 如果循环一遍后仍然没有玩家能放置方块，游戏结束
            if attempts >= self.max_players:
                self.game_over = True
                self.determine_winner()
    
    def determine_winner(self):
        """确定获胜者"""
        # 计算每个玩家剩余的方块数
        player_scores = {}
        for player_num, player_data in self.players.items():
            remaining = sum(PIECES[piece_id]['size'] for piece_id in player_data['pieces'])
            player_scores[player_num] = remaining
        
        # 找出剩余方块数最少的玩家
        min_remaining = min(player_scores.values())
        winners = [player_num for player_num, score in player_scores.items() if score == min_remaining]
        
        if len(winners) == 1:
            self.winner = winners[0]
        else:
            self.winner = "tie"
    
    def get_valid_positions(self, player_num, piece_id, rotation=0, flip=False):
        """获取方块的所有有效放置位置"""
        print(f"Game.get_valid_positions: player_num={player_num}, piece_id={piece_id}, rotation={rotation}, flip={flip}")
        valid_positions = []
        
        piece_coords = get_transformed_piece(piece_id, rotation, flip)
        print(f"变换后的方块坐标: {piece_coords}")
        if piece_coords is None:
            print("方块坐标为None，返回空列表")
            return valid_positions
        
        print(f"检查棋盘大小: {self.board_size}x{self.board_size}")
        print(f"玩家{player_num}的first_move状态: {self.players.get(player_num, {}).get('first_move', 'Unknown')}")
        
        for board_x in range(self.board_size):
            for board_y in range(self.board_size):
                valid, message = self.is_valid_position(piece_coords, board_x, board_y, player_num)
                if valid:
                    valid_positions.append((board_x, board_y))
                elif board_x == 0 and board_y == 0:  # 只为(0,0)位置打印调试信息
                    print(f"位置(0,0)无效: {message}")
        
        print(f"找到{len(valid_positions)}个有效位置: {valid_positions[:10]}...")  # 只显示前10个
        return valid_positions
    
    def get_game_state(self):
        """获取当前游戏状态"""
        return {
            'board': self.board,
            'board_size': self.board_size,
            'max_players': self.max_players,
            'current_player': self.current_player,
            'players': {
                str(player_num): {
                    'pieces': player_data['pieces'],
                    'placed_pieces': player_data['placed_pieces'],
                    'score': len(player_data['placed_pieces'])
                }
                for player_num, player_data in self.players.items()
            },
            'game_over': self.game_over,
            'winner': self.winner
        }
    
    def get_scores(self):
        """获取玩家分数（剩余方块数）"""
        scores = {}
        for player_num, player_data in self.players.items():
            remaining_pieces = sum(PIECES[piece_id]['size'] for piece_id in player_data['pieces'])
            scores[str(player_num)] = remaining_pieces
        return scores


class GameRoom:
    def __init__(self, room_id, max_players=2):
        self.room_id = room_id
        self.max_players = max_players
        self.players = {}  # socket_id -> player_data
        self.game = None
        self.status = "waiting"  # waiting, playing, finished
        self.current_player = None
        
    def add_player(self, socket_id, player_name):
        """添加玩家到房间"""
        if len(self.players) >= self.max_players:
            return None
        
        player_num = len(self.players) + 1
        self.players[socket_id] = {
            'player_num': player_num,
            'player_name': player_name,
            'socket_id': socket_id
        }
        return player_num
    
    def remove_player(self, socket_id):
        """从房间移除玩家"""
        if socket_id in self.players:
            del self.players[socket_id]
    
    def start_game(self):
        """开始游戏"""
        if len(self.players) == self.max_players:
            self.game = Game(self.max_players)
            for socket_id, player_data in self.players.items():
                self.game.add_player(socket_id, player_data['player_num'])
            self.status = "playing"
            self.current_player = 1
    
    def can_start_game(self):
        """检查是否可以开始游戏"""
        return len(self.players) == self.max_players
    
    def place_piece(self, player_id, piece_id, position, rotation=0, flip=False):
        """放置方块"""
        if self.game is None:
            return {"success": False, "message": "游戏未开始"}
        
        # 找到玩家编号
        player_num = None
        for socket_id, player_data in self.players.items():
            if socket_id == player_id:
                player_num = player_data['player_num']
                break
        
        if player_num is None:
            return {"success": False, "message": "玩家不在房间中"}
        
        board_x, board_y = position
        result = self.game.place_piece(player_num, piece_id, board_x, board_y, rotation, flip)
        
        if result['success']:
            self.current_player = self.game.current_player
            if self.game.game_over:
                self.status = "finished"
        
        return result
    
    def get_valid_positions(self, player_id, piece_id, rotation=0, flip=False):
        """获取有效位置"""
        print(f"GameRoom.get_valid_positions: player_id={player_id}, piece_id={piece_id}")
        
        if self.game is None:
            print("游戏未开始")
            return []
        
        # 找到玩家编号
        player_num = None
        print(f"当前房间玩家: {self.players}")
        
        if player_id in self.players:
            player_num = self.players[player_id]['player_num']
            print(f"找到玩家 {player_id}，player_num: {player_num}")
        else:
            print(f"未找到玩家 {player_id}")
            return []
        
        result = self.game.get_valid_positions(player_num, piece_id, rotation, flip)
        print(f"游戏逻辑返回的有效位置: {result}")
        return result
    
    def is_game_over(self):
        """检查游戏是否结束"""
        return self.game is not None and self.game.game_over
    
    def get_winner(self):
        """获取获胜者"""
        if self.game is not None:
            return self.game.winner
        return None
    
    def get_scores(self):
        """获取分数"""
        if self.game is not None:
            return self.game.get_scores()
        return {}
    
    def get_game_state(self):
        """获取游戏状态"""
        if self.game is None:
            return None
        
        game_state = self.game.get_game_state()
        # 添加房间信息
        game_state['room_id'] = self.room_id
        game_state['players_info'] = {
            str(player_data['player_num']): {
                'name': player_data['player_name'],
                'socket_id': player_data['socket_id']
            }
            for player_data in self.players.values()
        }
        
        return game_state 