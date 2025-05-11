import signal
import threading
import os
from app import create_app


def listen_for_exit():
    """Thread function to listen for exit command"""
    while True:
        key = input().strip().lower()
        if key == 'q':
            print("Quitting...")
            # Send a keyboard interrupt to exit gracefully
            os.kill(os.getpid(), signal.SIGINT)


if __name__ == '__main__':
    # Start the exit listener thread
    threading.Thread(target=listen_for_exit, daemon=True).start()
    app = create_app()
    # Run the Flask application
    app.run(debug=True)