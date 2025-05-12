from flask import Blueprint, request, jsonify, current_app
import uuid
import time
import threading
from firebase_handler import FirebaseHandler

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Store connected clients
clients = {}


def init_clients():
    """Initialize clients dictionary"""
    global clients
    clients = {}


def get_client_by_id(client_id):
    """Helper function to get client by ID"""
    return clients.get(client_id)


def cleanup_old_clients():
    """Cleanup old clients periodically"""
    from flask import current_app

    # Default values in case we're outside app context
    client_timeout = 3600  # 1 hour
    cleanup_interval = 300  # 5 minutes

    try:
        # Try to get values from config if in app context
        client_timeout = current_app.config.get('CLIENT_TIMEOUT', client_timeout)
        cleanup_interval = current_app.config.get('CLEANUP_INTERVAL', cleanup_interval)
    except RuntimeError:
        # We're outside app context, use defaults
        pass

    current_time = time.time()
    to_remove = []

    for client_id, client in clients.items():
        if current_time - client['connected_at'] > client_timeout:
            to_remove.append(client_id)

    for client_id in to_remove:
        del clients[client_id]

    # Schedule next cleanup
    threading.Timer(cleanup_interval, cleanup_old_clients).start()


# Client connection management
@api_bp.route('/connect', methods=['POST'])
def connect():
    data = request.json
    username = data.get('username', 'Anonymous')
    client_id = str(uuid.uuid4())

    clients[client_id] = {
        'username': username,
        'messages': [],
        'connected_at': time.time()
    }

    return jsonify({'success': True, 'client_id': client_id})


@api_bp.route('/poll', methods=['POST'])
def poll():
    data = request.json
    client_id = data.get('client_id')

    if client_id not in clients:
        return jsonify({'success': False, 'error': 'Invalid client ID'})

    messages = clients[client_id]['messages']
    clients[client_id]['messages'] = []

    return jsonify({'success': True, 'messages': messages})


# Challenge related API endpoints
@api_bp.route('/challenges')
def get_challenges():
    client_id = request.args.get('client_id')

    if client_id not in clients:
        return jsonify({'success': False, 'error': 'Invalid client ID'})

    username = clients[client_id]['username']

    # Get user data from Firebase
    user_handler = FirebaseHandler("users")
    user_data = user_handler.get_record(username)
    user_solved = user_data.get('solved_challenges', []) if user_data else []

    # Get challenges from Firebase
    challenge_handler = FirebaseHandler("challenges")
    all_challenges = challenge_handler.get_all_records()

    challenge_list = []
    for challenge_id, challenge in all_challenges.items():
        challenge_data = {
            'id': challenge_id,
            'name': challenge['name'],
            'category': challenge['category'],
            'difficulty': challenge['difficulty'],
            'points': challenge['points'],
            'solved': challenge_id in user_solved
        }
        challenge_list.append(challenge_data)

    return jsonify({'success': True, 'challenges': challenge_list})


@api_bp.route('/challenge/<challenge_id>')
def get_challenge(challenge_id):
    client_id = request.args.get('client_id')

    if client_id not in clients:
        return jsonify({'success': False, 'error': 'Invalid client ID'})

    # Get challenge from Firebase
    challenge_handler = FirebaseHandler("challenges")
    challenge = challenge_handler.get_record(challenge_id)

    if not challenge:
        return jsonify({'success': False, 'error': 'Challenge not found'})

    username = clients[client_id]['username']

    # Get user data from Firebase
    user_handler = FirebaseHandler("users")
    user_data = user_handler.get_record(username)
    user_solved = user_data.get('solved_challenges', []) if user_data else []

    challenge_data = {
        'id': challenge_id,
        'name': challenge['name'],
        'description': challenge['description'],
        'category': challenge['category'],
        'difficulty': challenge['difficulty'],
        'points': challenge['points'],
        'solved': challenge_id in user_solved
    }

    return jsonify({'success': True, 'challenge': challenge_data})


@api_bp.route('/challenge/<challenge_id>/hint')
def get_challenge_hint(challenge_id):
    client_id = request.args.get('client_id')

    if client_id not in clients:
        return jsonify({'success': False, 'error': 'Invalid client ID'})

    # Get challenge from Firebase
    challenge_handler = FirebaseHandler("challenges")
    challenge = challenge_handler.get_record(challenge_id)

    if not challenge:
        return jsonify({'success': False, 'error': 'Challenge not found'})

    return jsonify({'success': True, 'hint': challenge['hint']})


# Flag submission endpoint
@api_bp.route('/flag/submit', methods=['POST'])
def submit_flag():
    data = request.json
    client_id = data.get('client_id')
    challenge_id = data.get('challenge_id')
    flag = data.get('flag', '').strip()

    if client_id not in clients:
        return jsonify({'success': False, 'error': 'Invalid client ID'})

    # Get challenge from Firebase
    challenge_handler = FirebaseHandler("challenges")
    challenge = challenge_handler.get_record(challenge_id)

    if not challenge:
        return jsonify({'success': False, 'message': 'Challenge not found'})

    username = clients[client_id]['username']

    # Get user data from Firebase
    user_handler = FirebaseHandler("users")
    user_data = user_handler.get_record(username)

    if not user_data:
        return jsonify({'success': False, 'message': 'User not found'})

    user_solved = user_data.get('solved_challenges', [])
    user_score = user_data.get('score', 0)

    # Check if already solved
    if challenge_id in user_solved:
        return jsonify({'success': False, 'message': 'You have already solved this challenge'})

    # Check the flag
    if flag == challenge['flag']:
        # Update user data in Firebase
        user_score += challenge['points']
        user_solved.append(challenge_id)

        user_handler.update_record(username, {
            "score": user_score,
            "solved_challenges": user_solved
        })

        # Notify client
        clients[client_id]['messages'].append({
            'type': 'FlagCorrect',
            'data': {
                'challenge_id': challenge_id,
                'points': challenge['points']
            }
        })

        # Notify all clients about score update
        for cid in clients:
            clients[cid]['messages'].append({
                'type': 'ScoreUpdate',
                'data': None
            })

        return jsonify({
            'success': True,
            'message': f'Correct flag! You earned {challenge["points"]} points!'
        })
    else:
        # Notify client
        clients[client_id]['messages'].append({
            'type': 'FlagIncorrect',
            'data': {
                'challenge_id': challenge_id,
                'message': 'Incorrect flag'
            }
        })

        return jsonify({
            'success': False,
            'message': 'Incorrect flag'
        })


# Scoreboard endpoint
@api_bp.route('/scoreboard')
def get_scoreboard():
    client_id = request.args.get('client_id')

    if client_id not in clients:
        return jsonify({'success': False, 'error': 'Invalid client ID'})

    # Get all users from Firebase
    user_handler = FirebaseHandler("users")
    all_users = user_handler.get_all_records()

    # Build scoreboard data
    scoreboard = []
    for username, user_data in all_users.items():
        score = user_data.get('score', 0)
        solved = user_data.get('solved_challenges', [])
        scoreboard.append({
            'username': username,
            'score': score,
            'solved': len(solved)
        })

    # Sort by score (descending)
    scoreboard.sort(key=lambda x: (-x['score'], x['username']))

    return jsonify({'success': True, 'scoreboard': scoreboard})
