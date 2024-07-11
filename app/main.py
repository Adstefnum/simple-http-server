# Uncomment this to pass the first stage
import socket
import re
import threading
import os
import argparse
import gzip

def handle_connection(client_socket, addr):
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('--directory',  help='Directory where files are stored')

    args = parser.parse_args()
    directory = args.directory

    print(f"connection received from {addr}")
    response = "HTTP/1.1 404 Not Found\r\n\r\n"
    data = client_socket.recv(1024)
    data_breakdown  = data.decode("utf-8").split("\r\n")
    request_data = data_breakdown[0].split(" ")

    if request_data[1] == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"

    elif re.match(r"/[a-z]+", request_data[1]):
        path_data = request_data[1].split("/")
        path = path_data[1].strip()
        encoding_string = next((s for s in data_breakdown if re.match(r"Accept-Encoding: (.*)", s)), None)

        if path == "user-agent":
            user_agent_string = next((s for s in data_breakdown if re.match(r"User-Agent: (.*)", s)), None)
            user_agent = user_agent_string.split(" ")[1].strip()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"

        elif path == "files" and request_data[0] == "GET":
            filename = path_data[2].strip()
            file_path = os.path.join(directory, filename)

            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    file_contents = f.read()
                    no_of_bytes = len(file_contents)
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {no_of_bytes}\r\n\r\n" + file_contents.decode("utf-8")
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"

        elif path == "files" and request_data[0] == "POST":
            filename = path_data[2].strip()
            file_path = os.path.join(directory, filename)

            file_contents = data_breakdown[-1].encode("utf-8")
            with open(file_path, "wb") as f:
                f.write(file_contents)

            response = "HTTP/1.1 201 Created\r\n\r\n"

        if path != "files" and len(path_data) > 2:
            param = path_data[2].strip()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(param)}\r\n\r\n{param}"

        if encoding_string:
            encoding = encoding_string.split(" ")[1].strip()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: {encoding}\r\n\r\n"

        if encoding_string and encoding == "invalid-encoding":
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"

    client_socket.send(response.encode("utf-8"))
    print(f"connection closed from {addr}")
    client_socket.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), backlog=5)
    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_connection, args=(client_socket,addr))
            client_thread.start()

    except KeyboardInterrupt:
        print("Shutting down server")
    
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
