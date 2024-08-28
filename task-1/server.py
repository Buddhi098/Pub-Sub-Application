import socket
import sys

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server started in port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        while True:
            data = client_socket.recv(1024).decode()
            if data.lower() == 'terminate':
                print("Terminated!!!.")
                client_socket.close()
                break
            print(f"Received from client: {data}")
        if data.lower() == 'terminate':
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    start_server(port)
