import socket
import threading
import sys

clients = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        try:
            message = conn.recv(1024).decode()
            if message:
                topic, msg = message.split(':', 1)
                if topic in clients:
                    for client in clients[topic]:
                        if client != conn: 
                            client.send(f"{addr} says: {msg}".encode())
        except:
            connected = False
            print(f"[DISCONNECT] {addr} disconnected.")
            for topic, client_list in clients.items():
                if conn in client_list:
                    client_list.remove(conn)

    conn.close()

def start_server(server_ip, server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen()
    print(f"[LISTENING] Server is listening on {server_ip}:{server_port}")

    while True:
        conn, addr = server.accept()
        topic = conn.recv(1024).decode()
        if topic not in clients:
            clients[topic] = []
        clients[topic].append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <server_port>")
        sys.exit()

    server_ip = "0.0.0.0"
    server_port = int(sys.argv[1])

    start_server(server_ip, server_port)
