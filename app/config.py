import os


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SESSION_TYPE = 'filesystem'
    CHALLENGES_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'challenges')

    # Client session timeout in seconds (1 hour)
    CLIENT_TIMEOUT = 3600

    # Client cleanup interval in seconds (5 minutes)
    CLEANUP_INTERVAL = 300