# CTF Shell Server

A secure remote shell server for CTF challenges that provides encrypted access to a sandboxed bash environment.

## How It Works

The server creates a bridge between remote clients and a local bash shell using PTY (Pseudo Terminal):

```
CLIENT MACHINE           NETWORK           SERVER MACHINE
┌─────────────┐                          ┌──────────────────────┐
│   Terminal  │ ←→ [encrypted socket] ←→ │ Server Parent Process│
│  (your SSH  │                          │         ↕            │
│   client)   │                          │   [PTY Master fd]    │
└─────────────┘                          │         ↕            │
                                         │   [PTY Slave]        │
                                         │         ↕            │
                                         │   Bash Child Process │
                                         │  (runs commands in   │
                                         │   challenge_dir)     │
                                         └──────────────────────┘
```

## Process Flow

1. **Server Setup**: Listens on `0.0.0.0:4444` for connections
2. **Client Connection**: Each client gets its own thread
3. **Encryption**: RSA + AES encryption established
4. **PTY Creation**: `pty.fork()` creates two processes:
   - **Child Process**: Becomes bash shell in challenge directory
   - **Parent Process**: Handles client ↔ shell communication
5. **Data Bridge**: Server parent process uses `select()` to monitor:
   - Client socket for commands → writes to PTY → bash receives
   - PTY for bash output → sends back to client

## Key Components

- **PTY Master**: File descriptor held by server parent process
- **PTY Slave**: Connected to bash child process  
- **SecureChannel**: AES-encrypted communication with client
- **Challenge Directory**: Sandboxed environment for CTF files

## Usage

```bash
python3 netcat_server.py
```

Clients can connect using netcat or custom clients that implement the encryption protocol.

## Security Features

- RSA + AES encryption for all communications
- Sandboxed bash environment
- No profile/rc files loaded
- Controlled working directory
- 30-minute session timeout
