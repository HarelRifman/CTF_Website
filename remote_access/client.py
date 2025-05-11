# netcat_client.py

#!/usr/bin/env python3
import socket
import sys
import threading
import argparse
import struct
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


def parse_arguments():
    parser = argparse.ArgumentParser(description='Secure Netcat Client')
    parser.add_argument('host', help='The host to connect to')
    parser.add_argument('port', type=int, help='The port to connect to')
    parser.add_argument('-t', '--timeout', type=int, default=1800,
                        help='Connection timeout in seconds (default: 1800)')
    return parser.parse_args()


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


class NetcatClient:
    def __init__(self, host, port, timeout=1800):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.running = False
        self.secure_channel = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            print(f"[*] Connecting to {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))
            print(f"[+] Connected to {self.host}:{self.port}")

            # Step 1: Receive server public key
            pubkey_len = struct.unpack('>I', self.socket.recv(4))[0]
            server_pubkey = self.socket.recv(pubkey_len)
            rsa_key = RSA.import_key(server_pubkey)
            cipher_rsa = PKCS1_OAEP.new(rsa_key)

            # Step 2: Generate AES session key, send it encrypted
            aes_key = get_random_bytes(32)
            encrypted_key = cipher_rsa.encrypt(aes_key)
            self.socket.sendall(struct.pack('>I', len(encrypted_key)) + encrypted_key)

            # Step 3: Setup AES secure channel
            self.secure_channel = SecureChannel(self.socket, aes_key)
            return True

        except Exception as e:
            print(f"[!] Connection error: {e}")
            return False

    def receive_data(self):
        try:
            while self.running:
                data = self.secure_channel.recv()
                if not data:
                    print("\n[!] Connection closed by server")
                    self.running = False
                    break
                sys.stdout.write(data.decode('utf-8', errors='replace'))
                sys.stdout.flush()
        except Exception as e:
            if self.running:
                print(f"\n[!] Error receiving data: {e}")
                self.running = False

    def send_data(self):
        try:
            while self.running:
                try:
                    user_input = input()
                    if not self.running:
                        break
                    self.secure_channel.send((user_input + '\n').encode())
                except EOFError:
                    self.running = False
                    break
        except Exception as e:
            if self.running:
                print(f"\n[!] Error sending data: {e}")
                self.running = False

    def start(self):
        if not self.connect():
            return False

        self.running = True
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.daemon = True
        receive_thread.start()

        try:
            self.send_data()
        except KeyboardInterrupt:
            print("\n[*] Keyboard interrupt detected, exiting...")
        finally:
            self.stop()

        return True

    def stop(self):
        self.running = False
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.socket.close()
            print("[*] Connection closed")


def main():
    args = parse_arguments()
    client = NetcatClient(args.host, args.port, args.timeout)

    try:
        client.start()
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        if client.running:
            client.stop()


if __name__ == "__main__":
    main()
