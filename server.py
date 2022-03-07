import socket
import threading
import traceback
import util.server_commands as server_commands
import util.server_messaging as server_messaging
import util.server_channels as server_channels
import util.server_client as server_client

HOST = "127.0.0.1"
PORT = 6666

# Starting Server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Starting server on port {PORT}")

    # Server initialized -> start listening on another thread
    thread = threading.Thread(target=wait_for_clients, args=(server_socket,))
    thread.daemon = True
    thread.start()

    # Start server cmd loop
    handle_server()

def handle_server():
    while True:
        try:
            cmd = input('')
        except KeyboardInterrupt:
            server_messaging.broadcast("Server stopped.")
            print("Stopping the server.")
            break

# Waits for clients and accepts them
def wait_for_clients(server_socket: socket.socket):
    while True:
        try:
            # Accept Connection
            client, address = server_socket.accept()
            print(f"{(str(address))} connected.")

            # Handle nickname
            server_messaging.message_client(client, 'NAME')
            nickname = client.recv(1024).decode(server_messaging.ENCODING)
            server_messaging.broadcast(f"{nickname} joined!")

            # Add client to the main channel
            clientObj = server_client.Client(client, nickname, "main")
            server_channels.channels["main"].append(clientObj)

            # Broadcast, and handle client messages
            clientObj.connect()
        except KeyboardInterrupt:
            print("Stopping server")
            break

if __name__ == "__main__":
    start_server()