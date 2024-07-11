# Uncomment this to pass the first stage
import socket
import re


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221))

    while True:
        client_socket, addr = server_socket.accept()

        data = client_socket.recv(1024)
        data_breadkdown  = data.decode("utf-8").split(" ")

        if data_breadkdown[1] == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"

        elif re.match(r"/[a-z]+/[a-z]+", data_breadkdown[1]):
            param = data_breadkdown[1].split("/")[2].strip()
            print(param)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(param)}\r\n\r\n{param}"

        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        client_socket.send(response.encode("utf-8"))
        server_socket.close()


if __name__ == "__main__":
    main()
