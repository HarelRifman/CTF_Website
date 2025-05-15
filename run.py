# run.py
import threading
import sys
import os

from app import create_app

def listen_for_exit():
    """
    Safely listen for exit command with proper error handling
    """
    try:
        while True:
            try:
                # Use sys.stdin.readline() instead of input() for more robust input
                key = sys.stdin.readline().strip().lower()
                if key in ['q', 'quit', 'exit']:
                    print("\nReceiving exit command. Shutting down...")
                    os._exit(0)  # Force immediate exit
            except Exception as e:
                print(f"Error in exit listener: {e}")
                break
    except Exception as e:
        print(f"Unexpected error in exit listener: {e}")

def main():
    # Create Flask app
    app = create_app()

    # Setup exit thread
    exit_thread = threading.Thread(target=listen_for_exit, daemon=True)
    exit_thread.start()

    # Run the Flask development server
    try:
        app.run(debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        os._exit(1)

if __name__ == '__main__':
    main()