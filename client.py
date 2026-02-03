import socket
import os
import threading
from constants import HOST, PORT


class Client:
    def __init__(self) -> None:
        self.__from_server_client_messages = []
        self.__user_name = ""
        return None

    def recv_messages(self, client_socket: socket.socket) -> None:
        while True:
            try:
                message = client_socket.recv(1024).decode()

                # A returned empty bytes object indicates that the client/server has disconnected
                if not message:
                    print("Connection closed by the server")
                    client_socket.close()
                    break

                self.__from_server_client_messages.append(message)
                os.system("clear")
                for msg_rec in self.__from_server_client_messages:
                    print(msg_rec)

            except Exception as e:
                print(f"Client Exception. Error receiving message:", e)
                client_socket.close()
                print("Client connection closed.")
                break

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

            except KeyboardInterrupt as e:
                print("Keyboard  bla")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    _ = Client().start()
