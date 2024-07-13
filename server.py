import socket
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

host = '127.0.0.1'
port = 9000
addr = (host, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.listen()

clients = []
client_names = []

def broadcast_msg(message):
    for client in clients:
        client.send(message)

def handle_clients(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast_msg(message)
        except Exception as e:
            logger.error(f"Error handling client: {e}")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            client_name = client_names[index]
            broadcast_msg(f"{client_name} left the chat".encode('ascii'))
            client_names.remove(client_name)
            break

def receive():
    while True:
        try:
            client, address = server.accept()
            logger.info(f"Connected with {str(address)}")
    
            client.send('NAME'.encode('ascii'))
            client_name = client.recv(1024).decode('ascii')
            client_names.append(client_name)
            clients.append(client)
    
            logger.info(f"Name of the client is {client_name}!")
            broadcast_msg(f"{client_name} joined the chat!".encode('ascii'))
            client.send("Connected to the server!".encode('ascii'))
    
            thread = threading.Thread(target=handle_clients, args=(client,))
            thread.start()
        except Exception as e:
            logger.error(f"Error accepting client connection: {e}")

logger.info("Server is listening ...")
receive()