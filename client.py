import socket
from constants import HOST, PORT


class Client:
    def __init__(self) -> None:
        return None

    def start(self) -> None:

        with socket.socket() as client:
            print("try connecting")
            try:
                client.connect((socket.gethostname(), PORT))

                print("connected")
            except Exception as e:
                print(e)

            message = input("> ")
            while True:
                client.sendall(message.encode())
                data = client.recv(1024).decode()
                print("from server: ", data)
                message = input("> ")

            client.socket.close()
