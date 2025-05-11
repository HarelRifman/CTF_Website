# netcat_server.py

#!/usr/bin/env python3
import socket
import threading
import os
import pty
import select
import termios
import signal
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import struct

# Configuration
HOST = '0.0.0.0'
PORT = 4444
TIMEOUT = 1800

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
CHALLENGE_DIR = os.path.join(BASE_DIR, 'challenges')

class SecurePtyServer:
    def __init__(self, host, port, challenge_dir):
        self.host = host
        self.port = port
        self.challenge_dir = challenge_dir
        self.server_socket = None
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey().export_key()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"[+] CTF Shell Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"[+] Connection from {client_address[0]}:{client_address[1]}")
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("[+] Server shutting down...")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket, address):
        try:
            # Step 1: Send public RSA key
            client_socket.sendall(struct.pack('>I', len(self.public_key)) + self.public_key)

            # Step 2: Receive encrypted AES key
            aes_key_len = struct.unpack('>I', client_socket.recv(4))[0]
            encrypted_key = client_socket.recv(aes_key_len)
            cipher_rsa = PKCS1_OAEP.new(self.private_key)
            aes_key = cipher_rsa.decrypt(encrypted_key)

            # Step 3: Now secure communications with AES
            aes_cipher = SecureChannel(client_socket, aes_key)

            welcome_msg = """
            ========================================
            Welcome to the Reverse Engineering CTF!
            ========================================
            
            You are now in a shell environment.
            Your goal is to analyze and reverse engineer it to find the flag.
            
            Use your tools to crack the file.
            
            Good luck!
            
            """
            aes_cipher.send(welcome_msg.encode())

            # PTY shell
            child_pid, fd = pty.fork()

            if child_pid == 0:
                os.chdir(self.challenge_dir)
                sys.stdin = open('/dev/null', 'r')
                sys.stdout = open('/dev/null', 'w')
                sys.stderr = open('/dev/null', 'w')
                os.execvp("/bin/bash", ["/bin/bash", "--noprofile", "--norc"])
            else:
                client_socket.setblocking(False)
                new_attr = termios.tcgetattr(fd)
                new_attr[3] = new_attr[3] & ~termios.ECHO
                termios.tcsetattr(fd, termios.TCSANOW, new_attr)

                while True:
                    r, _, _ = select.select([client_socket, fd], [], [], 0.1)
                    if client_socket in r:
                        try:
                            encrypted_data = aes_cipher.recv()
                            if not encrypted_data:
                                break
                            os.write(fd, encrypted_data)
                        except:
                            break
                    if fd in r:
                        try:
                            data = os.read(fd, 1024)
                            if not data:
                                break
                            aes_cipher.send(data)
                        except:
                            break

        except Exception as e:
            print(f"[!] Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"[+] Connection from {address[0]}:{address[1]} closed")

class SecureChannel:
    def __init__(self, sock, key):
        self.sock = sock
        self.key = key

    def send(self, data):
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        packet = cipher.nonce + tag + ciphertext
        self.sock.sendall(struct.pack('>I', len(packet)) + packet)

    def recv(self):
        raw_len = self._recv_exact(4)
        if not raw_len:
            return None
        packet_len = struct.unpack('>I', raw_len)[0]
        packet = self._recv_exact(packet_len)
        if not packet:
            return None
        nonce, tag, ciphertext = packet[:16], packet[16:32], packet[32:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data

    def _recv_exact(self, n):
        data = b''
        while len(data) < n:
            more = self.sock.recv(n - len(data))
            if not more:
                return None
            data += more
        return data

if __name__ == "__main__":
    print("[+] Starting CTF shell server...")
    server = SecurePtyServer(HOST, PORT, CHALLENGE_DIR)
    server.start()