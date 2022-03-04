# Messaging procedures
def broadcast(message, channels):
    for channel in channels.values():
        broadcast_channel(channel, message)

def broadcast_channel(channel, message):
    for client in channel:
        message_client(client, message)

def message_client(client, message):
    client.client.send(message)