from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
import uuid
import json
from datetime import datetime
from game_logic import Game, GameRoom

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app, origins=["*"])
# 对于生产环境，使用eventlet作为async_mode
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# 游戏房间管理
rooms = {}
players = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "服务器运行正常"})

@app.route('/api/create-room', methods=['POST'])
def create_room():
    data = request.get_json() or {}
    max_players = data.get('max_players', 2)  # 默认2人游戏
    
    # 验证max_players参数
    if max_players not in [2, 4]:
        return jsonify({"error": "max_players must be 2 or 4"}), 400
    
    room_id = str(uuid.uuid4())[:8]
    room = GameRoom(room_id, max_players)
    rooms[room_id] = room
    return jsonify({
        "room_id": room_id, 
        "max_players": max_players,
        "message": f"房间创建成功（{max_players}人游戏）"
    })

@app.route('/api/room/<room_id>', methods=['GET'])
def get_room(room_id):
    if room_id not in rooms:
        return jsonify({"error": "房间不存在"}), 404
    
    room = rooms[room_id]
    return jsonify({
        "room_id": room_id,
        "players": len(room.players),
        "max_players": room.max_players,
        "status": room.status,
        "current_player": room.current_player
    })

@socketio.on('connect')
def on_connect():
    print(f'客户端连接: {request.sid}')

@socketio.on('disconnect')
def on_disconnect():
    print(f'客户端断开连接: {request.sid}')
    # 清理玩家数据
    if request.sid in players:
        player_data = players[request.sid]
        room_id = player_data.get('room_id')
        if room_id and room_id in rooms:
            room = rooms[room_id]
            room.remove_player(request.sid)
            emit('player_left', {
                'message': '有玩家离开了游戏',
                'players_count': len(room.players),
                'max_players': room.max_players
            }, room=room_id)
            
            if len(room.players) == 0:
                del rooms[room_id]
        
        del players[request.sid]

@socketio.on('join_room')
def on_join_room(data):
    room_id = data['room_id']
    player_name = data.get('player_name', f'玩家{request.sid[:6]}')
    
    if room_id not in rooms:
        emit('error', {'message': '房间不存在'})
        return
    
    room = rooms[room_id]
    
    if len(room.players) >= room.max_players:
        emit('error', {'message': '房间已满'})
        return
    
    join_room(room_id)
    player_id = room.add_player(request.sid, player_name)
    
    if player_id is None:
        emit('error', {'message': '无法加入房间'})
        return
    
    players[request.sid] = {
        'room_id': room_id,
        'player_id': player_id,
        'player_name': player_name
    }
    
    emit('joined_room', {
        'room_id': room_id,
        'player_id': player_id,
        'player_name': player_name,
        'players_count': len(room.players),
        'max_players': room.max_players
    })
    
    # 通知房间内其他玩家
    emit('player_joined', {
        'player_name': player_name,
        'players_count': len(room.players),
        'max_players': room.max_players,
        'can_start': room.can_start_game()
    }, room=room_id, include_self=False)
    
    # 如果房间满了，开始游戏
    if room.can_start_game():
        room.start_game()
        emit('game_started', {
            'game_state': room.get_game_state(),
            'message': '游戏开始！'
        }, room=room_id)

@socketio.on('place_piece')
def on_place_piece(data):
    if request.sid not in players:
        emit('error', {'message': '未加入房间'})
        return
    
    player_data = players[request.sid]
    room_id = player_data['room_id']
    player_id = player_data['player_id']
    
    if room_id not in rooms:
        emit('error', {'message': '房间不存在'})
        return
    
    room = rooms[room_id]
    
    try:
        result = room.place_piece(
            request.sid,  # 传递socket_id而不是player_id
            data['piece_id'],
            data['position'],
            data.get('rotation', 0),
            data.get('flip', False)
        )
        
        if result['success']:
            # 通知所有玩家棋盘状态更新
            emit('game_updated', {
                'game_state': room.get_game_state(),
                'last_move': {
                    'player_id': player_id,
                    'piece_id': data['piece_id'],
                    'position': data['position']
                }
            }, room=room_id)
            
            # 检查游戏是否结束
            if room.is_game_over():
                winner = room.get_winner()
                emit('game_over', {
                    'winner': winner,
                    'final_scores': room.get_scores(),
                    'message': f'游戏结束！{"平局" if winner == "tie" else f"玩家{winner}获胜！"}'
                }, room=room_id)
        else:
            emit('move_error', {'message': result['message']})
            
    except Exception as e:
        emit('error', {'message': f'放置方块时出错: {str(e)}'})

@socketio.on('get_valid_positions')
def on_get_valid_positions(data):
    print(f"收到get_valid_positions请求: {data}")
    
    if request.sid not in players:
        print(f"错误：request.sid {request.sid} 不在players中")
        print(f"当前players: {players}")
        emit('error', {'message': '未加入房间'})
        return
    
    player_data = players[request.sid]
    room_id = player_data['room_id']
    player_id = player_data['player_id']
    
    print(f"玩家数据: {player_data}")
    print(f"房间ID: {room_id}, 玩家ID: {player_id}")
    
    if room_id not in rooms:
        print(f"错误：房间 {room_id} 不存在")
        print(f"当前rooms: {list(rooms.keys())}")
        emit('error', {'message': '房间不存在'})
        return
    
    room = rooms[room_id]
    print(f"找到房间，状态: {room.status}")
    
    try:
        valid_positions = room.get_valid_positions(
            request.sid,  # 传递socket_id而不是player_id
            data['piece_id'],
            data.get('rotation', 0),
            data.get('flip', False)
        )
        
        print(f"计算出的有效位置: {valid_positions}")
        
        emit('valid_positions', {
            'piece_id': data['piece_id'],
            'positions': valid_positions
        })
        
    except Exception as e:
        print(f"获取有效位置时出错: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': f'获取有效位置时出错: {str(e)}'})

if __name__ == '__main__':
    # 开发环境直接运行
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
else:
    # 生产环境，gunicorn会直接使用socketio对象
    pass 