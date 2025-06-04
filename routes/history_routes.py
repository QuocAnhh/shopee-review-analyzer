from flask import Blueprint, request, jsonify
from flask_cors import CORS  # Thêm CORS
from bson import ObjectId
from datetime import datetime
from models.chat_history import ChatHistory
from utils.security import verify_token
from functools import wraps

history_bp = Blueprint('history', __name__)

# Cấu hình CORS cho blueprint (nếu frontend và backend chạy trên domain/port khác nhau)
CORS(history_bp, resources={r"/api/*": {"origins": "*"}})  # Thay * bằng URL frontend nếu cần

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(f"Received token: {token}")  # Thêm log để debug
        if not token or not token.startswith('Bearer '):
            print("Invalid token format")  # Log lỗi
            return jsonify({'error': 'Invalid token format'}), 401
            
        payload = verify_token(token[7:])
        print(f"Token payload: {payload}")  # Log payload
        if not payload:
            print("Invalid or expired token")  # Log lỗi
            return jsonify({'error': 'Invalid or expired token'}), 401
            
        return f(payload['sub'], *args, **kwargs)
    return decorated

def initialize_history_routes(app, db):
    chat_history = ChatHistory(db)

    @history_bp.route('/api/chats', methods=['GET'])
    @token_required
    def get_chat_history(user_id):
        """Get user's chat history list"""
        print(f"Fetching history for user_id: {user_id}")  # Thêm log
        try:
            chats = chat_history.get_chat_history(user_id)
            
            formatted_chats = []
            for chat in chats:
                last_msg = chat['messages'][-1]['content'] if chat['messages'] else ''
                preview = (last_msg[:60] + '...') if len(last_msg) > 60 else last_msg
                
                formatted_chats.append({
                    'id': str(chat['_id']),
                    'title': chat['title'],
                    'preview': preview,
                    'created_at': chat['created_at'].isoformat(),
                    'updated_at': chat['updated_at'].isoformat(),
                    'is_active': chat.get('is_active', False),
                    'message_count': len(chat['messages'])
                })

            return jsonify({'chats': formatted_chats}), 200
        except Exception as e:
            print(f"Error in get_chat_history: {str(e)}")  # Log lỗi
            return jsonify({'error': str(e)}), 500

    @history_bp.route('/api/chats/new', methods=['POST'])
    @token_required
    def create_new_chat(user_id):
        """Create a new chat session"""
        print(f"Creating new chat for user_id: {user_id}")  # Thêm log
        try:
            data = request.get_json()
            chat_id = chat_history.create_new_chat(
                user_id,
                initial_message=data.get('initial_message')
            )
            
            chat_history.set_active_chat(user_id, chat_id)
            
            return jsonify({
                'chat_id': chat_id,
                'message': 'New chat created successfully'
            }), 201
        except Exception as e:
            print(f"Error in create_new_chat: {str(e)}")  # Log lỗi
            return jsonify({'error': str(e)}), 500

    @history_bp.route('/api/chats/active', methods=['GET', 'PUT'])
    @token_required
    def active_chat(user_id):
        """Get or update the active chat"""
        print(f"Handling active chat for user_id: {user_id}, method: {request.method}")  # Thêm log
        try:
            if request.method == 'GET':
                chat = chat_history.get_active_chat(user_id)
                if not chat:
                    return jsonify({'error': 'No active chat found'}), 404
                
                return jsonify({
                    'id': str(chat['_id']),
                    'title': chat['title'],
                    'messages': chat['messages'],
                    'created_at': chat['created_at'].isoformat(),
                    'updated_at': chat['updated_at'].isoformat(),
                    'model': chat.get('model', 'default')
                }), 200
                
            elif request.method == 'PUT':
                data = request.get_json()
                if not data or 'messages' not in data:
                    return jsonify({'error': 'Messages are required'}), 400
                
                chat = chat_history.get_active_chat(user_id)
                if not chat:
                    return jsonify({'error': 'No active chat to update'}), 404
                
                success = chat_history.update_chat(
                    str(chat['_id']),
                    user_id,
                    data['messages'],
                    data.get('title')
                )
                
                if not success:
                    return jsonify({'error': 'Failed to update chat'}), 500
                
                return jsonify({'message': 'Chat updated successfully'}), 200

        except Exception as e:
            print(f"Error in active_chat: {str(e)}")  # Log lỗi
            return jsonify({'error': str(e)}), 500

    @history_bp.route('/api/chats/<chat_id>', methods=['GET', 'PUT', 'DELETE'])
    @token_required
    def manage_chat(user_id, chat_id):
        """Manage individual chat sessions"""
        print(f"Managing chat_id: {chat_id} for user_id: {user_id}, method: {request.method}")  # Thêm log
        try:
            if request.method == 'GET':
                chat = chat_history.get_chat(chat_id, user_id)
                if not chat:
                    return jsonify({'error': 'Chat not found'}), 404
                
                return jsonify({
                    'id': str(chat['_id']),
                    'title': chat['title'],
                    'messages': chat['messages'],
                    'created_at': chat['created_at'].isoformat(),
                    'updated_at': chat['updated_at'].isoformat()
                }), 200
                
            elif request.method == 'PUT':
                data = request.get_json()
                if data.get('set_active', False):
                    success = chat_history.set_active_chat(user_id, chat_id)
                    if not success:
                        return jsonify({'error': 'Failed to activate chat'}), 500
                    return jsonify({'message': 'Chat activated successfully'}), 200
                
                elif data.get('new_title'):
                    success = chat_history.rename_chat(chat_id, user_id, data['new_title'])
                    if not success:
                        return jsonify({'error': 'Failed to rename chat'}), 500
                    return jsonify({'message': 'Chat renamed successfully'}), 200
                
                return jsonify({'error': 'Invalid action'}), 400
                
            elif request.method == 'DELETE':
                success = chat_history.delete_chat(chat_id, user_id)
                if not success:
                    return jsonify({'error': 'Chat not found'}), 404
                
                return jsonify({'message': 'Chat deleted successfully'}), 200

        except Exception as e:
            print(f"Error in manage_chat: {str(e)}")  # Log lỗi
            return jsonify({'error': str(e)}), 500

    app.register_blueprint(history_bp)