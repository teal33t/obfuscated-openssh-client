import subprocess
import os
import signal
import time
import psutil
import configparser
import sys
import atexit

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        'SSH_PORT': config.get('SSH', 'PORT'),
        'OBFUSCATE_KEYWORD': config.get('SSH', 'OBFUSCATE_KEYWORD'),
        'SOCKS_PROXY': config.get('SSH', 'SOCKS_PROXY'),
        'SSH_USER': config.get('SSH', 'USER'),
        'SSH_SERVER': config.get('SSH', 'SERVER'),
        'SSH_KEY': os.path.expanduser(config.get('SSH', 'KEY')),
        'PASSWORD': config.get('SSH', 'PASSWORD')
    }

def handle_sigint(sig, frame):
    print("\nSignal received, disconnecting...")
    exit_gracefully()

def exit_gracefully():
    if 'ssh_process' in globals() and ssh_process.poll() is None:
        ssh_process.terminate()
    print("Disconnected successfully.")
    sys.exit(0)

@atexit.register
def on_exit():
    exit_gracefully()

def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"  # in the rare case of extremely large size

def monitor_io(process):
    reset_statistics()  # Reset statistics when a new SSH connection is established

    prev_bytes_sent = prev_bytes_recv = 0
    total_bytes_sent = total_bytes_recv = 0
    start_time = time.time()

    while process.poll() is None:
        try:
            time.sleep(1)
            net_io = psutil.net_io_counters()
            bytes_sent, bytes_recv = net_io.bytes_sent, net_io.bytes_recv

            upload_speed = bytes_sent - prev_bytes_sent
            download_speed = bytes_recv - prev_bytes_recv

            total_bytes_sent += upload_speed
            total_bytes_recv += download_speed

            elapsed_time = time.time() - start_time

            sys.stdout.write(
                f"\rCurrent ↑ {format_bytes(upload_speed)}/s | ↓ {format_bytes(download_speed)}/s | "
                f"Total ↑ {format_bytes(total_bytes_sent)} | ↓ {format_bytes(total_bytes_recv)} | "
                f"Time {int(elapsed_time)}s"
            )
            sys.stdout.flush()

            prev_bytes_sent, prev_bytes_recv = bytes_sent, bytes_recv

        except KeyboardInterrupt:
            handle_sigint(signal.SIGINT, None)

def reset_statistics():
    global prev_bytes_sent, prev_bytes_recv, total_bytes_sent, total_bytes_recv, start_time
    prev_bytes_sent = prev_bytes_recv = 0
    total_bytes_sent = total_bytes_recv = 0
    start_time = time.time()

def connect_ssh(config):
    ssh_command = [
        'sshpass', '-p', config['PASSWORD'], 'ssh', '-p', config['SSH_PORT'],
        '-o', f'ObfuscateKeyword={config["OBFUSCATE_KEYWORD"]}',
        '-o', 'LogLevel=QUIET',
        '-o', 'StrictHostKeyChecking=no',
        '-D', config['SOCKS_PROXY'],
        '-i', config['SSH_KEY'],
        f'{config["SSH_USER"]}@{config["SSH_SERVER"]}'
    ]

    try:
        process = subprocess.Popen(ssh_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Connected to {config['SSH_SERVER']}")
        return process
    except subprocess.CalledProcessError:
        print("SSH connection failed")
        exit_gracefully()
    except KeyboardInterrupt:
        handle_sigint(signal.SIGINT, None)

def main():
    global ssh_process
    config = load_config()

    signal.signal(signal.SIGINT, handle_sigint)

    ssh_process = connect_ssh(config)
    if ssh_process:
        monitor_io(ssh_process)

if __name__ == "__main__":
    main()