import socket
import threading

# Socket settings
HOST = "127.0.0.1"
PORT = 6666

# Client settings
ENCODING = "utf-8"

def setup_client():
    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_adr = input("Give an ip-address to join: ")
    try:
        client.connect((host_adr, PORT))
    except:
        print("Couldn't connect to server. Closing client.")
        return

    try:
        # Choosing Nickname
        nickname = input("Choose your nickname: ")

        send_thread = threading.Thread(target=send, args=(client,))
        send_thread.daemon = True

        send_thread.start()
        recv(client, nickname)
    except:
        pass

def send(client):
    while True:
        try:
            message = input('')
            client.send(message.encode(ENCODING))
        except:
            # Close Connection When Error
            print("Closing client")
            client.close()
            break

def recv(client, nickname):
    while(True):
        try:
            message = client.recv(1024).decode(ENCODING)
            if message == 'NAME':
                client.send(nickname.encode(ENCODING))
            elif message == 'INVALID_NAME':
                print('The nickname is already taken.')
                break
            elif message == 'DISCONNECT':
                break
            else:
                print(message)
        except:
            # Close Connection When Error or keyboardinterrupt
            print("Closing client.")
            client.close()
            break

if __name__ == "__main__":
    setup_client()