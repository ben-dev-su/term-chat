import errno
import socket
import sys
import threading
from constants import HOST, PORT


class Server:
    def __init__(self) -> None:
        self.clients: list[socket.socket] = []
        self.client_messages: list[str] = []
        self.client_threads: list[threading.Thread] = []
        self.lock: threading.Lock = threading.Lock()

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
                if not client_socket._closed:
                    client_socket.close()
                    print(f"Connection from: {str(client_addr)} closed")
                    break

        if client_socket in self.clients:
            with self.lock:
                self.clients.remove(client_socket)

    def broadcast_message(self, message: str) -> None:
        with self.lock:
            for client in self.clients:
                client.send(message.encode())

    def graceful_server_shutdown(self) -> None:
        print("Shutting down")
        with self.lock:
            clients_to_close: list[socket.socket] = self.clients[:]
            self.clients.clear()

        for client in clients_to_close:
            try:
                if not client._closed:
                    client.shutdown(socket.SHUT_WR)
                    client.close()
            except Exception as e:
                print("Error closing connection:", e)
        print("All connections closed")
        sys.exit(0)

    def start(self) -> None:
        with socket.socket() as stream:
            try:
                stream.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                stream.bind((HOST, PORT))
                stream.listen(5)
                print(f"Server running on {HOST}:{PORT}")
                while True:
                    try:
                        print("Waiting for connection...")
                        client_socket, client_addr = stream.accept()
                        print(f"Connected to client: {client_addr}")

                        with self.lock:
                            self.clients.append(client_socket)

                        client_thread = threading.Thread(
                            target=self.handle_client_connection,
                            args=(client_socket, client_addr),
                        )
                        client_thread.daemon = True
                        client_thread.start()

                    except OSError as e:
                        if e.errno == errno.ECONNABORTED:
                            print("Client aborted the connection")
                        elif e.errno == errno.ECONNRESET:
                            print("Client closed the connection")
                        elif e.errno == errno.EPIPE:
                            print("Broken Pipe. Client disconnected")
                        else:
                            print(f"Unexpected Network Error {e}")

                        continue

                    except Exception as e:
                        print(f"Unexpected Network Error {e}")

            except KeyboardInterrupt:
                self.graceful_server_shutdown()
            except OSError as e:
                if e.errno == errno.EADDRINUSE:
                    print("Address in use")
            except Exception as e:
                print(f"Unexpected Network Error {e}")


if __name__ == "__main__":
    _ = Server().start()
