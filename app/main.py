# Uncomment this to pass the first stage
import socket
import re


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    response = "HTTP/1.1 404 Not Found\r\n\r\n"
    server_socket = socket.create_server(("localhost", 4221))

    while True:
        client_socket, addr = server_socket.accept()

        data = client_socket.recv(1024)
        data_breakdown  = data.decode("utf-8").split("\r\n")
        request_data = data_breakdown[0].split(" ")

        if request_data[1] == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"

        elif re.match(r"/[a-z]+", request_data[1]):
            path_data = request_data[1].split("/")
            path = path_data[1].strip()

            if path == "user-agent":
                user_agent_string = next((s for s in data_breakdown if re.match(r"User-Agent: (.*)", s)), None)
                user_agent = user_agent_string.split(" ")[1].strip()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"

            if len(path_data) > 2:
                param = path_data[2].strip()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(param)}\r\n\r\n{param}"

        client_socket.send(response.encode("utf-8"))
        server_socket.close()


if __name__ == "__main__":
    main()
