import threading
import util.server_messaging as server_messaging
import util.server_channels as server_channels
import util.server_commands as server_commands

# Client class
class Client:
    def __init__(self, client, name, channel):
        self.client = client
        self.name = name
        self.channel = channel

    def change_channel(self, channel_name):
        pass

    def connect(self):
        server_messaging.message_client(self.client, 'Connected to server! Type -help for available commands')

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle_client_msgs, args=(self,))
        thread.daemon = True
        thread.start()

    def disconnect(self):
        try:
            server_channels.channels[self.channel].remove(self)
            server_messaging.message_client(self.client, "DISCONNECT")
            self.client.close()
            print(f"{self.name} left!")
            server_messaging.broadcast(server_channels.channels, f'{self.name} left!')
        except:
            pass

def find_client(name: str):
    for channel in server_channels.channels.values():
        for client in channel:
            if client.name == name:
                return client
    return None

def handle_client_msgs(client: Client):
    while True:
        try:
            message = client.client.recv(1024).decode('utf-8')
            print(f"[{client.channel}] {client.name}: {message}")
            if (message.startswith('-')):
                server_commands.parse_command(message, client)
            else:
                server_messaging.broadcast_channel(server_channels.channels[client.channel], f"[{client.channel}] {client.name}: {message}")
        except:
            # Client disconnects with keyboardinterrupt or crashes
            client.disconnect()
            break