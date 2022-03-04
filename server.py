import socket
import threading
import traceback
import util.server_commands as server_commands
import util.server_messaging as server_messaging

HOST = "127.0.0.1"
PORT = 6666

# Channels
channels = {"main": []}

# Client class
class Client:
    def __init__(self, client, name, channel):
        self.client = client
        self.name = name
        self.channel = channel

    def change_channel(self, channel_name):
        pass

    def connect(self):
        server_messaging.broadcast(f"{self.name} joined!".encode('ascii'), channels)
        self.client.send('Connected to server! Type -help for available commands'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle_client_msgs, args=(self,))
        thread.daemon = True
        thread.start()

    def disconnect(self):
        channels[self.channel].remove(self)
        self.client.close()
        print(f"{self.name} left!")
        server_messaging.broadcast(f'{self.name} left!'.encode('ascii'), channels)

# Starting Server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Starting server on port {PORT}")

    # Server initialized -> start listening on another thread
    thread = threading.thread(target=accept_clients, args=(server_socket,))
    thread.daemon = True
    thread.start()

    # Start server cmd loop

def handle_server(thread: threading.Thread):
    while True:
        try:
            cmd = input('')
        except KeyboardInterrupt:
            server_messaging.broadcast("Server stopped.".encode('ascii'))
            print("Stopping the server.")

# Waits for clients and accepts them
def accept_clients(server_socket):
    while True:
        try:
            # Accept Connection
            client, address = server_socket.accept()
            print(f"{(str(address))} connected.")

            # Handle nickname
            # TODO: Custom msgs for server to simulate rpc
            client.send('NICKNAME'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')

            # Add client to the main channel
            clientObj = Client(client, nickname, "main")
            channels["main"].append(clientObj)

            # Broadcast, and handle client messages
            clientObj.connect()
        except KeyboardInterrupt:
            print("Stopping server")
            break

def handle_client_msgs(client):
    while True:
        try:
            message = client.client.recv(1024).decode('ascii')
            if (message.startswith('-')):
                server_messaging.broadcast_channel(channels[client.channel], message.encode('ascii'))
            else:
                server_commands.parse_command(message, client)
        except:
            # Client disconnects or crashes
            traceback.print_exc()
            client.disconnect()
            break

if __name__ == "__main__":
    start_server()