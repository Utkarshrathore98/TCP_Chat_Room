import socket
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client_name = input("Enter client name: ")

host = '127.0.0.1'
port = 9000
addr = (host, port)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(addr)
    logger.info(f"Connected to server at {host}:{port}")
except ConnectionRefusedError:
    logger.error(f"Connection to {host}:{port} refused. Is the server running?")
    exit()

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NAME':
                client.send(client_name.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            client.close()
            break

def write():
    while True:
        try:
            message = f"{client_name}: {input('')}"
            client.send(message.encode('ascii'))
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()