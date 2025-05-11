from flask import Blueprint, jsonify, send_file, current_app, request
import os
from firebase_handler import FirebaseHandler
# Import clients dictionary directly to avoid circular imports
from app.api import clients

# Create blueprint
challenges_bp = Blueprint('challenges', __name__, url_prefix='/challenges')


@challenges_bp.route('/<challenge_id>/download')
def download_challenge(challenge_id):
    client_id = request.args.get('client_id')
    client = clients.get(client_id)

    if not client:
        return jsonify({'success': False, 'error': 'Invalid client ID'})

    # Get challenge from Firebase
    challenge_handler = FirebaseHandler("challenges")
    challenge = challenge_handler.get_record(challenge_id)

    if not challenge:
        return jsonify({'success': False, 'error': 'Challenge not found'})

    file_path = os.path.join(current_app.config['CHALLENGES_FOLDER'], challenge['file'])

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=challenge['file'])
    else:
        return jsonify({'success': False, 'error': 'Challenge file not found'})

# Note: The API routes for challenges are defined in api.py
# This file is kept for future challenge-specific routes that aren't API endpoints