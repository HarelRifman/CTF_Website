from flask import Flask
import os


def create_app():
    app = Flask(__name__,
                template_folder='templates')
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['CHALLENGES_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'challenges')

    # Create necessary folders
    os.makedirs(app.config['CHALLENGES_FOLDER'], exist_ok=True)

    # Import and register blueprints
    from app.auth import auth_bp
    from app.challenges import challenges_bp
    from app.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(api_bp)

    # Initialize clients dict to be used across modules
    from app.api import init_clients, cleanup_old_clients
    init_clients()

    # Use Flask 2.x way of handling startup functions
    with app.app_context():
        # This runs once during initialization but within the app context
        from threading import Thread
        cleanup_thread = Thread(target=cleanup_old_clients, daemon=True)
        cleanup_thread.start()

    return app