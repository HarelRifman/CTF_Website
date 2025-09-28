# Cybersecurity Challenge Platform

A web-based platform for cybersecurity challenges with remote access capabilities

## 🌐 Live Website

**The platform is now live and accessible at: [https://ctf-website-1.onrender.com/](https://ctf-website-1.onrender.com/)**

Sign up for an account and start solving cybersecurity challenges immediately!

## 📁 Project Structure

```
CTF_Website/
├── app/                          # Main Flask application
│   ├── __init__.py              # Flask app initialization
│   ├── api.py                   # API endpoints
│   ├── auth.py                  # Authentication system
│   ├── challenges.py            # Challenge management
│   ├── config.py                # Configuration settings
│   ├── static/images/           # Static assets
│   │   ├── background.png       # Background image
│   │   └── logo.png            # CTF logo
│   └── templates/               # HTML templates
│       ├── auth/                # Authentication pages
│       │   ├── signin.html      # Sign in page
│       │   └── signup.html      # Sign up page
│       └── main/                # Main application pages
│           └── dashboard.html   # User dashboard
├── challenges/                  # Challenge files and resources
│   ├── buffer_overflow/         # Buffer overflow challenges
│   │   ├── chall               # Compiled binary
│   │   └── chall.c             # Source code
│   ├── buffer_overflow.zip     # Challenge archive
│   ├── caesar_cipher.txt       # Cryptography challenge
│   ├── hidden_treasure.png     # Steganography challenge
│   ├── reverse_me.out          # Reverse engineering binary
│   └── try_trace_me            # Tracing challenge
├── remote_access/              # Remote access platform
│   ├── client.py               # Client application
│   ├── server.py               # Server application
│   └── README.md               # Remote access documentation
├── firebase_handler.py         # Firebase database handler
├── requirements.txt            # Python dependencies
├── run.py                     # Application entry point
├── upload_challenges.py       # Challenge upload utility
└── README.md                  # This file
```

## 🚀 Quick Start

Visit [https://ctf-website-1.onrender.com/](https://ctf-website-1.onrender.com/) to start solving challenges immediately! No installation required.

## 🔧 Remote Access Platform

For advanced cybersecurity challenges that require direct system interaction, we provide a secure remote access platform. This allows participants to connect to dedicated challenge environments and practice real-world penetration testing scenarios.

### ✨ Features

- **🔐 Encrypted Communication**: All data transmission is secured using AES encryption
- **🛡️ Isolated Environment**: Each challenge runs in a sandboxed environment
- **📊 Real-time Monitoring**: Track progress and attempts in real-time
- **🎯 Challenge-specific Tools**: Pre-installed tools and utilities for each challenge type
- **🌐 Cross-platform Support**: Works on Windows, macOS, and Linux

### 🚀 Quick Setup

#### Prerequisites

- Python 3.7 or higher
- Virtual environment (recommended)

#### Server Setup

1. **Create and activate a virtual environment:**

   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate it
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install dependencies:**

   ```bash
   pip install pycryptodome
   ```

3. **Start the server:**

   ```bash
   cd remote_access
   python3 server.py  # Linux/macOS
   # or
   python server.py   # Windows
   ```

   The server will start on port 4444 by default. You'll see a confirmation message when it's ready.

#### Client Connection

1. **Install dependencies (if not already done):**

   ```bash
   pip install pycryptodome
   ```

2. **Connect to the server:**

   ```bash
   cd remote_access
   python3 client.py <server_ip> 4444
   ```

   **Examples:**

   ```bash
   # Local testing
   python3 client.py 127.0.0.1 4444

   # Remote server
   python3 client.py 192.168.1.100 4444
   ```

### 🎮 Usage

Once connected, you'll have access to:

- **Interactive shell** for command execution
- **File system access** within the challenge environment
- **Pre-installed tools** like `nmap`, `gdb`, `strings`, etc.
- **Challenge-specific files** and resources

### 🔒 Security Features

- **Session-based authentication** prevents unauthorized access
- **Command logging** for educational purposes
- **Resource limits** to prevent system abuse
- **Automatic session timeout** for security

### 📚 Available Challenge Types

- **Buffer Overflow Exploitation**: Practice stack-based buffer overflows
- **Binary Reverse Engineering**: Analyze and exploit compiled binaries
- **Network Penetration Testing**: Test network security configurations
- **Web Application Security**: Find and exploit web vulnerabilities
- **Cryptography Challenges**: Break various encryption schemes

## 🎯 Available Challenges

The platform includes a diverse range of cybersecurity challenges:

- **🔓 Buffer Overflow Exploitation**: Practice exploiting buffer overflow vulnerabilities in C programs
- **🔐 Caesar Cipher Decryption**: Decode messages encrypted with the classic Caesar cipher
- **🖼️ Hidden Data in Images**: Discover steganography techniques to find hidden information
- **🔍 Binary Reverse Engineering**: Analyze and reverse engineer compiled binaries
- **🌐 Web Application Security**: Learn the basics of web application vulnerabilities
- **📊 Network Penetration Testing**: Test network security configurations
- **🔢 Cryptography Challenges**: Break various encryption schemes

Access these challenges through the web interface after signing in. Each challenge comes with detailed instructions, hints, and progressive difficulty levels.

## 🛠️ Development

This project is open source and welcomes contributions! The codebase is organized for easy maintenance and extension:

### Key Components

- **`app/auth.py`**: User authentication and session management
- **`app/challenges.py`**: Challenge logic and scoring system
- **`app/api.py`**: API endpoints
- **`remote_access/`**: Secure remote challenge environment
- **`firebase_handler.py`**: Database operations and user data management

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Adding New Challenges

To add a new challenge:

1. Create the challenge content in the `challenges/` directory
2. Update the challenge database using `upload_challenges.py`
3. Modify `app/challenges.py` to include the new challenge details
4. Test the challenge thoroughly before deployment
