# Obfuscated SSH Service - Client

This project establishes an SSH connection using obfuscation and monitors network traffic. It includes features such as handling SIGINT for graceful disconnection and statistics on data sent/received over the network.

If you are looking for **Obfuscated SSH Service - Server**, go to [https://github.com/teal33t/obfuscated-openssh-tunnel](https://github.com/teal33t/obfuscated-openssh-tunnel) 

## Features

- **SSH Connection**: Connects to a remote server using SSH with specified configurations.
- **Obfuscation**: Supports keyword obfuscation for SSH traffic.
- **SOCKS Proxy**: Supports configuring a SOCKS proxy.
- **Traffic Monitoring**: Monitors network traffic (upload and download speeds as well as total data transferred).
- **Graceful Disconnect**: Handles SIGINT signals to terminate the connection gracefully.
- **Statistics Reset**: Resets traffic statistics when a new connection is established.

## Prerequisites

- Python 3.x
- `sshpass`
- `psutil`

## Configuration

Configure your SSH connection settings in a `config.ini` file. The `config.ini` should be structured as follows:

```ini
[SSH]
PORT = 8443
OBFUSCATE_KEYWORD = your-keyword-on-obfuscated-server
SOCKS_PROXY = 0.0.0.0:1080
USER = your-username-on-obfuscated-server
SERVER = your-ip
KEY = ~/.ssh/id_rsa
PASSWORD = your-password-on-obfuscated-server
```

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/teal33t/obfuscated-ssh-client.git
    cd obfuscated-ssh-client
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

    **Debian/Ubuntu:**

    ```bash
    apt-add-repository ppa:zinglau/obfuscated-openssh 
    apt update 
    apt install -y ssh #install obfuscated-openssh 
    apt install sshpass #install sshpass
    ```
    
## Usage

1. **Update Configuration**

    Ensure the `config.ini` file contains the correct settings for your SSH connection.

2. **Run the Script**

    ```bash
    python client.py
    ```

3. **Traffic Monitoring**

    Once connected, the script will display upload and download speeds, total data sent and received, and elapsed time.

## Handling Interruptions

- The script gracefully handles SIGINT signals, ensuring the SSH connection is properly terminated before exiting.


## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgements

- Thanks to the contributors of `psutil` and `sshpass` for their great tools.
- Inspired by various open-source projects for secure SSH connections.