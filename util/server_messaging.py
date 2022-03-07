import util.server_channels as server_channels

ENCODING = 'utf-8'

# Messaging procedures
def broadcast(message: str):
    for channel in server_channels.channels.values():
        broadcast_channel(channel, message)

def broadcast_channel(channel, message: str):
    for client in channel:
        message_client(client.client, message)

def message_client(client, message: str):
    client.send(message.encode(ENCODING))