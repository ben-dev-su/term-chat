import socket
import os
import threading
from constants import HOST, PORT


class Client:
    def __init__(self) -> None:
        self.__from_server_client_messages = []
        self.__user_name = ""
        return None

    def recv_messages(self, client_socket) -> None:
        while True:
            data = client_socket.recv(1024).decode()

            if data:
                self.__from_server_client_messages.append(data)
                # print(data)
                os.system("clear")
                for msg_rec in self.__from_server_client_messages:
                    print(msg_rec)
                # print("> ")

    def handle_input(self, client_socket):
        try:
            while True:
                message = input()
                if message:
                    client_socket.send(f"{self.__user_name}: {message}".encode())
        except OSError as os_error:
            print(f"Conncetion lost {os_error}")

    def start(self) -> None:
        with socket.socket() as client_socket:
            print("try connecting")
            try:
                client_socket.connect((socket.gethostname(), PORT))
                print("connected")
            except Exception as e:
                print(e)

            self.__user_name = input("Gebe deinen Name ein: ")

            client_socket.send(self.__user_name.encode())

            client_thread = threading.Thread(
                target=self.recv_messages, args=(client_socket,)
            )

            input_thread = threading.Thread(
                target=self.handle_input, args=(client_socket,)
            )
            input_thread.start()
            client_thread.start()
            input_thread.join()
            client_thread.join()


if __name__ == "__main__":
    _ = Client().start()
