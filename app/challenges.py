from flask import Blueprint, jsonify, send_file, current_app, request
import os
from firebase_handler import FirebaseHandler
from app.api import clients, get_client_by_id

challenges_bp = Blueprint('challenges', __name__, url_prefix='/api/challenge')

@challenges_bp.route('/<challenge_id>/download')
def download_challenge(challenge_id):
    client_id = request.args.get('client_id')
    client = get_client_by_id(client_id)

    if not client:
        return jsonify({
            'success': False,
            'error': 'Invalid client ID',
            'client_id': client_id,
            'registered_clients': list(clients.keys())
        }), 400

    challenge_handler = FirebaseHandler("challenges")
    challenge = challenge_handler.get_record(challenge_id)

    if not challenge:
        return jsonify({'success': False, 'error': 'Challenge not found'}), 404

    file_path = os.path.join(current_app.config['CHALLENGES_FOLDER'], challenge['file'])

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=challenge['file'])
    else:
        return jsonify({'success': False, 'error': 'Challenge file not found'}), 404
