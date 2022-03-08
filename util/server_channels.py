# Channels
channels = {"main": []}

def get_user_list(channel_name = None):
    user_list = []
    if channel_name != None:
        if channel_name in channels:
            for user in channels[channel_name]:
                user_list.append(user.name)
    else:
        for channel in channels.values():
            for user in channel:
                user_list.append(user.name)
    return user_list

def change_channel(client, new_channel):
    for key, channel in channels.items():
        for chan_client in channel:
            if chan_client == client:
                channel.remove(chan_client)
                # Check if the channel is empty and not main. If it is, delete it.
                if len(channel) == 0 and key != 'main':
                    channels.pop(key)
                break
        else:
            continue
        break
    
    # Create channel if it doesn't exist
    if (new_channel not in channels):
        channels[new_channel] = []
    channels[new_channel].append(client)
    client.channel = new_channel
                
    