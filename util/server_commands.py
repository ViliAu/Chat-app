import util.server_messaging as server_messaging

# First check if the msg starts with '-' if not, return it as is
def parse_command(message: str, client):
    # if it starts, splice the message to get arguments
    args = message.split()
    cmd = args.pop[0]
    print(cmd, args[0])

def disconnect():
    pass

# Commands
COMMANDS = {
    "disconnect": disconnect
}