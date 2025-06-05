from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from bson import ObjectId
from models.user import User
from config import Config

auth_bp = Blueprint('auth', __name__)

def initialize_auth_routes(app, db):
    user_manager = User(db)
    
    @auth_bp.route('/api/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')

            # Validate input
            if not all([name, email, password, confirm_password]):
                return jsonify({'error': 'All fields are required'}), 400

            if password != confirm_password:
                return jsonify({'error': 'Passwords do not match'}), 400

            # Check if user already exists
            if user_manager.find_user_by_email(email):
                return jsonify({'error': 'Email already registered'}), 409

            # Hash password and create user
            password_hash = generate_password_hash(password)
            user_id = user_manager.create_user(name, email, password_hash)

            # Generate JWT token
            access_token = create_access_token(str(user_id))

            return jsonify({
                'message': 'User registered successfully',
                'access_token': access_token,
                'user': {
                    'id': str(user_id),
                    'name': name,
                    'email': email
                }
            }), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @auth_bp.route('/api/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return jsonify({'error': 'Email and password are required'}), 400

            user = user_manager.find_user_by_email(email)
            if not user or not check_password_hash(user['password'], password):
                return jsonify({'error': 'Invalid credentials'}), 401

            # Generate JWT token
            access_token = create_access_token(str(user['_id']))

            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': {
                    'id': str(user['_id']),
                    'name': user['name'],
                    'email': user['email']
                }
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def create_access_token(user_id):
        payload = {
            'sub': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

    app.register_blueprint(auth_bp)