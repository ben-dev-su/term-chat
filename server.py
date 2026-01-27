import socket
import threading
from constants import HOST, PORT


class Server:
    def __init__(self) -> None:
        self.__clients = []
        return None

    def handle_clients(self) -> None:
        return None

    def handle_client_connection(self, client_conn, client_addr):
        print("Connection from: ", str(client_addr))
        while True:
            data = client_conn.recv(1024).decode()
            if not data:
                print(f"Connection from: {str(client_addr)} closed.")
                break

            print("from connected user: ", data)
            for client_socket in self.__clients:
                _ = client_socket.send(data.encode())
            # data = input("> ")

        client_conn.close()

    def start(self) -> None:
        with socket.socket() as stream:
            try:
                print(f"try binding socket {HOST} on {PORT}")
                stream.bind((HOST, PORT))
                stream.listen()
                print(f"listening on {HOST} on {PORT}")
            except Exception as e:
                print(e)

            while True:
                client_socket, client_addr = stream.accept()
                self.__clients.append(client_socket)
                client_thread = threading.Thread(
                    target=self.handle_client_connection,
                    args=(client_socket, client_addr),
                )
                client_thread.start()


if __name__ == "__main__":
    _ = Server().start()
