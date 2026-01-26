import socket
from constants import HOST, PORT


class Server:
    def __init__(self) -> None:
        return None

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
                conn, addr = stream.accept()
                print("Connection from: ", str(addr))

                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        print(f"Connection from: {str(addr)} closed.")
                        break

                    print("from connected user: ", data)
                    data = input("> ")
                    _ = conn.send(data.encode())

                conn.close()
