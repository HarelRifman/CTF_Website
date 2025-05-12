#!/usr/bin/env python3
"""
Script to upload cybersecurity challenges to Firebase database.
This script should be run from the project root directory.
"""

import sys
import os

# Import the FirebaseHandler class from the firebase_handler module
try:
    from firebase_handler import FirebaseHandler
except ImportError:
    print("Error: firebase_handler.py not found in the current directory.")
    print("Please run this script from the project root directory.")
    sys.exit(1)

def upload_challenges():
    """Upload the predefined challenges to Firebase."""
    # Initialize the FirebaseHandler with the 'challenges' reference
    firebase = FirebaseHandler('challenges')
    
    challenges = {
        "try-trace-me": {
            "id": "trace-me",
            "name": "Try Trace Me",
            "description": "Can you uncover the flag hidden in the binary by tracing its execution?",
            "category": "Reverse Engineering",
            "difficulty": "Easy",
            "points": 100,
            "file": "try_trace_me.zip", 
            "flag": "CTF{ltrace_rules}",
            "hint": "Sometimes watching what a program calls tells you more than what it says."
        },
        "crypto-caesar": {
            "id": "crypto-caesar",
            "name": "Caesar's Secret",
            "description": "Julius Caesar used this cipher to communicate with his generals. Can you crack it?",
            "category": "Cryptography",
            "difficulty": "Easy",
            "points": 100,
            "file": "caesar_cipher.txt",
            "flag": "CTF{et_tu_brute}",
            "hint": "The key is a rotation between 1 and 25."
        }, 
        "forensics-hidden": {
            "id": "forensics-hidden",
            "name": "Hidden Treasure",
            "description": "There's something hidden in this image. Can you find it?",
            "category": "Forensics",
            "difficulty": "Medium",
            "points": 200,
            "file": "hidden_treasure.png",
            "flag": "CTF{steganography_101}",
            "hint": "Sometimes data is hidden in the hex of a file."
        },
        "pwn-buffer": {
            "id": "pwn-buffer",
            "name": "Buffer Overflow",
            "description": "Exploit this simple program to get the flag. (you need to do it using the server)",
            "category": "Pwn",
            "difficulty": "Hard",
            "points": 300,
            "file": "buffer_overflow.zip",
            "flag": "CTF{stack_smashing_detected}",
            "hint": "Try to control the instruction pointer by overflowing the buffer."
        },
        "reverse-engineering": {
            "id": "reverse-engineering",
            "name": "Reverse Me",
            "description": "Reverse engineer this binary to find the flag.",
            "category": "Reverse Engineering",
            "difficulty": "Hard",
            "points": 350,
            "file": "reverse_me.bin",
            "flag": "CTF{disassembly_required}",
            "hint": "Follow the execution flow and look for string comparisons."
        }
    }
    
    # Count successful uploads
    success_count = 0
    
    # Upload each challenge
    for challenge_id, challenge_data in challenges.items():
        print(f"Uploading challenge: {challenge_data['name']}...")
        if firebase.add_record(challenge_id, challenge_data):
            success_count += 1
            print(f"✓ {challenge_data['name']} uploaded successfully")
        else:
            print(f"✗ Failed to upload {challenge_data['name']}")
    
    # Print summary
    print("\nUpload Summary:")
    print(f"Total challenges: {len(challenges)}")
    print(f"Successfully uploaded: {success_count}")
    print(f"Failed: {len(challenges) - success_count}")
    
    if success_count == len(challenges):
        print("\nAll challenges were uploaded successfully!")
    
def verify_database():
    """Verify that challenges were uploaded correctly."""
    firebase = FirebaseHandler('challenges')
    
    # Get all challenges from the database
    challenges = firebase.get_all_records()
    
    if not challenges:
        print("No challenges found in the database.")
        return
    
    print("\nVerifying database records:")
    print(f"Total challenges in database: {len(challenges)}")
    
    for challenge_id, challenge_data in challenges.items():
        print(f"- {challenge_data.get('name', 'Unknown Challenge')}")

def main():
    """Main function to run the script."""
    print("Cybersecurity Challenge Platform - Firebase Challenge Uploader")
    print("="*60)
    
    # Verify firebase-credentials.json exists
    if not os.path.exists('firebase-credentials.json'):
        print("Error: firebase-credentials.json not found in the current directory.")
        print("Please place your Firebase credentials file in the project root.")
        sys.exit(1)
    
    # Menu for user interaction
    print("\nSelect an option:")
    print("1. Upload challenges to Firebase")
    print("2. Verify database records")
    print("3. Upload and verify")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == '1':
        upload_challenges()
    elif choice == '2':
        verify_database()
    elif choice == '3':
        upload_challenges()
        verify_database()
    elif choice == '4':
        print("Exiting program.")
        sys.exit(0)
    else:
        print("Invalid choice. Please run the script again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
