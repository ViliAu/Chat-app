import socket
import threading

HOST = "127.0.0.1"
PORT = 6666

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
#channels = {"name": []}

# Starting Server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    # Server initialized -> start listening to clients
    accept_clients()

# Receiving / Listening Function
def accept_clients(server_socket):
    while True:
        # Accept Connection
        client, address = server_socket.accept()
        print(f"{(str(address))} connected.")

        # Handle nickname
        # TODO: Custom msgs for server to simulate rpc
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clients.append(client)
        nicknames.append(nickname)

        # Broadcast nickname join
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle_client_msgs, args=(client,))
        thread.start()

def broadcast(message):
    for client in clients:
        client.send(message)    

def handle_client_msgs(client):
    while True:
        try:
            # Broadcasting Messages
            # TODO: Handle commands
            message = client.recv(1024)
            broadcast(message)
        except:
            # Client disconnects
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

if __name__ == "__main__":
    start_server()