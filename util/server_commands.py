import util.server_messaging as server_messaging
import util.server_client as server_client
import util.server_channels as server_channels
import traceback

# Split command and arguments
def parse_command(message: str, client):
    # Remove the hyphen, and slice the command to command and args
    message = message[1:]
    args = message.split()
    cmd = args.pop(0)
    try:
        COMMANDS[cmd](client, args)
    except:
        server_messaging.message_client(client.client, "Command doesn't exist. Type -help for help.")
        traceback.print_exc()

def help(client, args):
    msg = ""
    if len(args) == 0:
        msg = "Available commands:"
        for command in COMMANDS.keys():
            msg += f" -{command},"
            msg = msg[:-1]
    else:
        try:
            msg = COMMAND_HELP[args[0]]
        except:
            msg = "Command not found. Type -help for a list of commands."
    server_messaging.message_client(client.client, msg)

def disconnect(client, args):
    client.disconnect()

def private_message(client, args):
    if len(args) < 2:
        server_messaging.message_client(client.client, "Usage: -pm [recipient] [message]")
        return
    rec_name = args.pop(0)
    recipient = server_client.find_client(rec_name)
    if recipient == None:
        server_messaging.message_client(client.client, f"User {rec_name} not found!")
    else:
        server_messaging.message_client(recipient.client, f"(whisper) {client.name}: {' '.join(args)}")

def list_users(client, args):
    msg = f"No users found!"
    users = []
    if len(args) > 0:
        users = server_channels.get_user_list(args[0])
    else:
        users = server_channels.get_user_list()
    if len(users) > 0:
        msg = ", ".join(users)
    server_messaging.message_client(client.client, f"Users online: {msg}")

    
def change_channel(client, args):
    if len(args) == 0:
        chList = "Available channels:"
        for channel in server_channels.channels.keys():
            chList += f" {channel},"
        server_messaging.message_client(client.client, chList[:-1])
        return
    server_channels.change_channel(client, args[0])

def broadcast_message(client, args):
    if (len(args) == 0):
        server_messaging.message_client(client, "Usage: -broadcast [message]")
        return
    server_messaging.broadcast(f"(broadcast) {client.name}: {' '.join(args)}")

    
# Commands
COMMANDS = {
    "help": help,
    "disconnect": disconnect,
    "pm": private_message,
    "list": list_users,
    "ch": change_channel,
    "broadcast": broadcast_message
}

COMMAND_HELP = {
    "help": "Displays help for various commands. Usage: -help ([command])",
    "disconnect": "Disconects the client from the server. Usage: -disconnect",
    "pm": "Sends a private message to a user regardless of their channel. Usage: -pm [recipient] [message]",
    "list": "Lists all users if no arguments are passed. Lists users on the passed channel. Usage: -list ([channel])",
    "ch": "Change to a different channel. Lists available channels if no arguments are given. Usage: -ch ([channel])",
    "broadcast": "Broadcast a message across all cahnnels. Usage: -broadcast [message]"
}