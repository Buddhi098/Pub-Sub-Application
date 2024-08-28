import socket
import sys
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def start_client(server_ip, server_port, role, topic):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    client.send(topic.encode())

    if role == "PUBLISHER":
        while True:
            message = input(f"{topic} (You): ")
            client.send(f"{topic}:{message}".encode())
            if message.lower() == "terminate":
                client.close()
                break
    elif role == "SUBSCRIBER":
        thread = threading.Thread(target=receive_messages, args=(client,))
        thread.start()
        while True:
            message = input()
            if message.lower() == "terminate":
                client.close()
                break

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: my_client_app <server_ip> <server_port> <role> <topic>")
        sys.exit()

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    role = sys.argv[3].upper()
    topic = sys.argv[4].upper()

    start_client(server_ip, server_port, role, topic)
