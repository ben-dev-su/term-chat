import socket
import threading
from constants import HOST, PORT


class Client:
    def __init__(self) -> None:
        return None

    def recv_messages(self, client_socket) -> None:
        while True:
            data = client_socket.recv(1024).decode()
            print(data)

    def start(self) -> None:
        with socket.socket() as client_socket:
            print("try connecting")
            try:
                client_socket.connect((socket.gethostname(), PORT))
                print("connected")
            except Exception as e:
                print(e)

            client_thread = threading.Thread(
                target=self.recv_messages, args=(client_socket,)
            )
            client_thread.start()

            while True:
                message = input("> ")
                client_socket.sendall(message.encode())

            client_socket.socket.close()


if __name__ == "__main__":
    _ = Client().start()
