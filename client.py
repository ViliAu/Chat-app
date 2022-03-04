import socket
import threading

# Socket settings
HOST = "127.0.0.1"
PORT = 6666

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send():
    while True:
        try:
            message = input('')
            #message = f'{nickname}: {body}'
            client.send(message.encode('ascii'))
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def recv():
    while(True):
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

if __name__ == "__main__":
    # Setup lient here and pass it to threads

    send_thread = threading.Thread(target=send)
    recv_thread = threading.Thread(target=recv)

    send_thread.start()
    recv_thread.start()