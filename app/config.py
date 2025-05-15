import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SESSION_TYPE = 'filesystem'
    
    # Get the absolute path of the project root directory
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Set challenges folder to the challenges directory in the project root
    CHALLENGES_FOLDER = os.path.join(BASE_DIR, 'challenges')

    # Client session timeout in seconds (1 hour)
    CLIENT_TIMEOUT = 3600

    # Client cleanup interval in seconds (5 minutes)
    CLEANUP_INTERVAL = 300
