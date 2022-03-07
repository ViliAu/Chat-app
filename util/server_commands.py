import util.server_messaging as server_messaging
import util.server_client as server_client
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
    msg = "Available commands:"
    for command in COMMANDS.keys():
        msg += " -" + command  
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
    

# Commands
COMMANDS = {
    "help": help,
    "disconnect": disconnect,
    "pm": private_message
}