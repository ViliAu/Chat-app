import socket
import threading

# Socket settings
HOST = "127.0.0.1"
PORT = 6666

# Client settings
ENCODING = "utf-8"

def setup_client():
    # Choosing Nickname
    nickname = input("Choose your nickname: ")

    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))

        send_thread = threading.Thread(target=send, args=(client,))
        send_thread.daemon = True
        #recv_thread = threading.Thread(target=recv, args=(client, nickname,))

        send_thread.start()
        #recv_thread.start()
        recv(client, nickname)

    except:
        print("Couldn't connect to server!")

def send(client):
    while True:
        try:
            message = input('')
            client.send(message.encode(ENCODING))
        except KeyboardInterrupt:
            # Close client with keyboard interrupt
            print("Closing client")
            client.close()
            break
        except:
            # Close Connection When Error
            print("An error occured!")
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
        except KeyboardInterrupt:
            # Close client with keyboard interrupt
            print("Closing client")
            client.close()
            break
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

if __name__ == "__main__":
    setup_client()