import socket
import threading
from constants import HOST, PORT


class Server:
    def __init__(self) -> None:
        self.clients: list[socket.socket] = []
        self.client_messages: list[str] = []
        return None

    def handle_client_connection(
        self, client_socket: socket.socket, client_addr: socket._RetAddress
    ) -> None:
        while True:
            try:
                client_message: str = client_socket.recv(1024).decode()

                # https://docs.python.org/3/library/socket.html#socket.socket.recvmsg
                # A returned empty bytes object indicates that the client/server has disconnected
                if not client_message:
                    print(f"Connection from: {str(client_addr)} closed")
                    break

                # TODO: Use logging
                print(f"[{client_addr}]: ", client_message)

                self.broadcast_message(client_message)

            except Exception as e:
                print("[Server Exception (Error client handling)]:", e)
                client_socket.close()
                print(f"Connection from: {str(client_addr)} closed")
                break

        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def broadcast_message(self, message: str) -> None:
        for client in self.clients:
            client.send(message.encode())

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

                    self.clients.append(client_socket)
                    client_thread = threading.Thread(
                        target=self.handle_client_connection,
                        args=(client_socket, client_addr),
                    )

                    client_thread.start()

            except Exception as e:
                print(e)
                for client in self.clients:
                    client.close()


if __name__ == "__main__":
    _ = Server().start()
