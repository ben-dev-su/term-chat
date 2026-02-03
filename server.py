import socket
import threading
from constants import HOST, PORT


class Server:
    def __init__(self) -> None:
        self.__clients: list[socket.socket] = []
        self.__client_messages = []
        return None

    def handle_clients(self) -> None:
        return None

    def handle_client_connection(self, client_socket, client_addr):
        while True:
            try:
                received_message = client_socket.recv(1024).decode()

                # https://docs.python.org/3/library/socket.html#socket.socket.recvmsg
                # A returned empty bytes object indicates that the client/server has disconnected
                if not received_message:
                    print(f"Connection from: {str(client_addr)} closed")
                    break

                print(f"[{client_addr}]: ", received_message)
                for client in self.__clients:
                    client.send(received_message.encode())

            except Exception as e:
                print("[Server Exception (Error client handling)]:", e)
                client_socket.close()
                print(f"Connection from: {str(client_addr)} closed")
                break

        if client_socket in self.__clients:
            self.__clients.remove(client_socket)

    def start(self) -> None:
        with socket.socket() as stream:
            try:
                stream.bind((HOST, PORT))
                stream.listen(5)
                print(f"Server running on {HOST}:{PORT}")

                while True:
                    print("Waiting for connection...")
                    client_socket, client_addr = stream.accept()
                    print(f"Connected to client: {client_addr}")

                    self.__clients.append(client_socket)
                    client_thread = threading.Thread(
                        target=self.handle_client_connection,
                        args=(client_socket, client_addr),
                    )

                    client_thread.start()

            except Exception as e:
                print(e)
                for client in self.__clients:
                    client.close()


if __name__ == "__main__":
    _ = Server().start()
