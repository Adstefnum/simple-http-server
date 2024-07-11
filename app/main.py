# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221))

    while True:
        client_socket, addr = server_socket.accept()

        data = client_socket.recv(1024)

        response = "HTTP/1.1 200 OK\r\n\r\n"

        client_socket.send(response.encode("utf-8"))
        server_socket.close()


if __name__ == "__main__":
    main()
