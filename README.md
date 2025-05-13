# Cybersecurity Challenge Platform

A web-based platform for cybersecurity challenges with remote access capabilities

## Project Structure

```
project_root/
├── app
│   ├── __init__.py
│   ├── api.py
│   ├── auth.py
│   ├── challenges.py
│   ├── config.py
│   └── templates
│       ├── auth
│       │   ├── signin.html
│       │   └── signup.html
│       └── main
│           └── dashboard.html
├── upload_challenges.py
├── challenges
│   ├── buffer_overflow.zip
│   ├── caesar_cipher.txt
│   ├── hidden_treasure.png
│   ├── reverse_me.bin
│   └── web_basics.zip
├── firebase_handler.py
├── remote_access
│   ├── client.py
│   └── server.py
└── run.py
```

## Setup Instructions

### 1. Create and Activate Virtual Environment

It's recommended to use a virtual environment to manage dependencies. This keeps your project dependencies isolated from your system packages.

#### On Linux/macOS:

```bash
# Navigate to your project directory
cd path/to/project_root

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

When activated successfully, your terminal prompt will change to show the virtual environment name in parentheses, like this:
```
(venv) username@hostname:~/project_root$
```

To deactivate the virtual environment when you're done working:
```bash
deactivate
```

#### On Windows:

```bash
# Navigate to your project directory
cd path\to\project_root

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

When activated successfully, your command prompt will be prefixed with `(venv)`:
```
(venv) C:\path\to\project_root>
```

To deactivate the virtual environment when you're done working:
```bash
deactivate
```

### 2. Install Web Application Dependencies

Once your virtual environment is activated, install the required packages:

#### On both Linux/macOS and Windows:

```bash
pip install flask firebase-admin flask-wtf
```

If you encounter any permission issues:
- On Linux/macOS: Try using `pip3` instead of `pip`
- On Windows: Ensure you're running Command Prompt as Administrator if necessary

You can verify the packages were installed correctly by running:
```bash
pip list
```

### 3. Configure Firebase Database

The application uses Firebase as its database. You need to set up a Firebase project and configure it:

1. Create a project at [Firebase Console](https://console.firebase.google.com/):
   - Click "Add project"
   - Follow the setup wizard to create your project
   - Enable Firestore Database when prompted

2. Generate a private key:
   - Go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file securely

3. Place the downloaded JSON file in your project root and name it `firebase-credentials.json`

4. Ensure that the `databaseURL` in the `firebase_handler.py` file is correctly set to the URL of your Firebase database. It should look something like:
   ```python
   databaseURL = "https://your-project-id.firebaseio.com"
   ```
   
**Important**: The credentials file contains sensitive information and should not be committed to version control. Make sure to add it to your `.gitignore` file:

```bash
# Add to .gitignore
firebase-credentials.json
```
### 4. Creating the challenges 
Run the `upload_challenges.py` in the same folder to upload the challenges information to your data base 


### 5. Running the Web Application

With your virtual environment activated, start the web application:

#### On Linux/macOS:
```bash
python3 run.py
```

#### On Windows:
```bash
python run.py
```

The application will be available at `http://localhost:5000` by default. Open this URL in your web browser to access the platform.

## Remote Access Setup

The project includes a remote access server and client for challenges that require direct system interaction.

### Setting up the Server

1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal)

2. Install the required cryptography library:
   ```bash
   pip install pycryptodome
   ```

3. Start the server:
   ```bash
   # Navigate to the remote_access directory
   cd remote_access
   
   # Start the server
   python server.py
   ```
On linux of course use `python3` instead of `python` command

The server will start listening on port 4444 by default. You should see a confirmation message in the terminal.

### Setting up the Client

1. Make sure your virtual environment is activated

2. Install the required cryptography library:
   ```bash
   pip install pycryptodome
   ```

3. Connect to the server:
   ```bash
   cd remote_access
   python client.py server_ip 4444
   ```
   
Replace `server_ip` with the actual IP address of your server. For local testing, you can use `127.0.0.1`.

Example:
```bash
# For local testing
python client.py 127.0.0.1 4444

# For remote server
python client.py 192.168.1.100 4444
```

## Available Challenges

The platform includes various cybersecurity challenges:

- **Buffer Overflow Exploitation**: Practice exploiting buffer overflow vulnerabilities
- **Caesar Cipher Decryption**: Decode messages encrypted with the classic Caesar cipher
- **Hidden Data in Images**: Discover steganography techniques to find hidden information
- **Binary Reverse Engineering**: Analyze and reverse engineer compiled binaries
- **Web Application Security**: Learn the basics of web application vulnerabilities

Access these challenges through the web interface after signing in. Each challenge comes with detailed instructions and hints.

## Development

To modify the application or add new challenges, refer to the modular structure:

- `app/auth.py`: Authentication functionality
- `app/challenges.py`: Challenge management
- `app/api.py`: API endpoints
- `remote_access/`: Remote challenge server components

### Adding New Challenges

To add a new challenge:

1. Create the challenge content in the `challenges/` directory
2. Update the challenge database in Firebase
3. Modify `app/challenges.py` to include the new challenge details

## Troubleshooting

### Virtual Environment Issues

- **Linux/macOS**: If you encounter permission issues when creating the virtual environment:
  ```bash
  sudo apt-get install python3-venv  # For Debian/Ubuntu
  # or
  sudo dnf install python3-venv  # For Fedora
  ```

- **Windows**: If `venv` is not recognized:
  - Ensure Python is added to your PATH during installation
  - Try using the full path: `C:\Python39\python.exe -m venv venv`

### Firebase Configuration

- Double-check that your Firebase configuration file path is correctly set in `firebase_handler.py`
- Verify Firebase rules allow read/write access for your application

### Connection Issues

- For remote access connection issues:
  - Check firewall settings and ensure the server port (4444) is open
  - Verify that the client and server are on the same network or properly port-forwarded
  - Try disabling any VPN services temporarily

### Package Installation Problems

- If you see "Command not found" errors, ensure your virtual environment is activated
- Update pip with `pip install --upgrade pip` before installing packages
- On Windows, you might need to install the Visual C++ Build Tools for some packages

If you continue to experience issues, please check the project's issue tracker or contact the maintainers.
