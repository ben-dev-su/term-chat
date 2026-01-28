import socket
import threading
from constants import HOST, PORT


class Server:
    def __init__(self) -> None:
        self.__clients = []
        self.__client_messages = []
        return None

    def handle_clients(self) -> None:
        return None

    def handle_client_connection(self, client_conn, client_addr):
        while True:
            received_message = client_conn.recv(1024).decode()
            if not received_message:
                print(f"Connection from: {str(client_addr)} closed")
                # TODO remove client for __clients
                break

            print(f"[{client_addr}]: ", received_message)
            for client_socket in self.__clients:
                client_socket.send(received_message.encode())

        client_conn.close()

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
                    client_thread.join()

            except Exception as e:
                print(e)


if __name__ == "__main__":
    _ = Server().start()
