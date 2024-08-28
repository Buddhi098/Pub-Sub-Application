import socket
import threading

publishers = []
subscribers = []

def handle_client(client_socket, client_type):
    if client_type == "PUBLISHER":
        publishers.append(client_socket)
    elif client_type == "SUBSCRIBER":
        subscribers.append(client_socket)
    
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data.lower() == 'terminate':
                print(f"{client_type} client requested termination.")
                client_socket.close()
                if client_type == "PUBLISHER":
                    publishers.remove(client_socket)
                elif client_type == "SUBSCRIBER":
                    subscribers.remove(client_socket)
                break
            elif client_type == "PUBLISHER":
                print(f"Publisher sent: {data}")
                for subscriber in subscribers:
                    subscriber.send(data.encode())
            elif client_type == "SUBSCRIBER":
                print(f"Received from Subscriber: {data}")
        except ConnectionResetError:
            break

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server started on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        client_type = client_socket.recv(1024).decode()
        print(f"Client type: {client_type}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_type))
        client_handler.start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: my_server_app <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
