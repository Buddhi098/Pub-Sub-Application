import socket
import sys
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Message from Publisher: {message}")
            else:
                break
        except ConnectionAbortedError:
            print("Connection closed by the server.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def start_client(server_ip, server_port, client_type):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    client_socket.send(client_type.encode())

    if client_type == "SUBSCRIBER":
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

    try:
        while True:
            message = input("Enter message: ")
            client_socket.send(message.encode())
            if message.lower() == "terminate":
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: my_client_app <SERVER_IP> <SERVER_PORT> <PUBLISHER|SUBSCRIBER>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    client_type = sys.argv[3].upper()
    start_client(server_ip, server_port, client_type)
