import errno
import os
import socket
import threading

from constants import HOST, PORT


class Client:
    def __init__(self) -> None:
        self.from_server_client_messages: list[str] = []
        self.__user_name: str = ""
        self.lock: threading.Lock = threading.Lock()

    def recv_messages(self, client_socket: socket.socket) -> None:
        try:
            while True:
                try:
                    data: bytes = client_socket.recv(1024)
                except OSError:
                    print("Unexpected Network Error While Receiving Data")
                    break

                # A returned empty bytes object indicates that the client/server has disconnected
                if not data:
                    print("Connection closed by the server")
                    break

                try:
                    message: str = data.decode()
                except UnicodeDecodeError:
                    print("Decoding Error")
                    continue

                with self.lock:
                    self.from_server_client_messages.append(message)

                self.render_messages()

        except Exception as e:
            print(f"Fatal Client error: {e}")
        finally:
            try:
                client_socket.close()
            except Exception:
                pass

    # TODO: use ANSI to draw to the screen
    def render_messages(self) -> None:
        with self.lock:
            messages_copy: list[str] = self.from_server_client_messages[:]

        # TODO: use subprocess
        os.system("clear")
        for msg_recv in messages_copy:
            print(msg_recv)

    # TODO:create message with metadata
    def transform_message(self, message: str) -> str:
        return f"{self.__user_name}: {message}"

    def handle_input(self, client_socket: socket.socket, message: str) -> bool:
        try:
            data: bytes = message.encode()
        except UnicodeEncodeError:
            print("Unexpected Encoding error")
            return True

        try:
            client_socket.sendall(data)
            return True
        except OSError as e:
            if e.errno == errno.ECONNABORTED:
                print("Client aborted the connection")
                return False
            elif e.errno == errno.ECONNRESET:
                print("Client closed the connection")
                return False
            elif e.errno == errno.EPIPE:
                print("Broken Pipe. Client disconnected")
                return False
            else:
                print(f"Unexpected Network Error {e}")
                return False

        except Exception as e:
            print(f"Unexpected Network Error {e}")
            return False

    def start(self) -> None:

        self.__user_name = input("Gebe deinen Name ein: ")

        with socket.socket() as client_socket:
            print("try connecting")
            try:
                client_socket.connect((socket.gethostname(), PORT))
                # BUG: wont print; because the message is not saved and the screen is being cleared
                print(f"Connected as {self.__user_name}")

                # TODO: Wait for ACK from server bevor starting the recv thread
                client_socket.sendall(self.__user_name.encode())

                recv_thread: threading.Thread = threading.Thread(
                    target=self.recv_messages, args=(client_socket,), daemon=True
                )

                # TODO: Wait for ACK from server bevor starting the recv thread
                recv_thread.start()

                try:
                    while True:
                        message: str = input()
                        if not self.handle_input(client_socket, message):
                            break

                except Exception as e:
                    print(f"Unknown Error: {e}")

            except KeyboardInterrupt:
                print("\nDisconnecting")
            except Exception as e:
                print(f"Connection Error: {e}")


if __name__ == "__main__":
    _ = Client().start()
