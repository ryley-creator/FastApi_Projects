import socket
import threading

clients = []  # List to store client sockets and addresses


def handle_client(client_socket, addr):
    try:
        while True:
            # Receive client message
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break  # Exit loop if client disconnects
            
            print(f"Client {addr[1]} sent: {request}")

            # Broadcast message to other clients
            broadcast_message = f"Client {addr[1]} sent message: {request}"
            for c in clients:
                if c != client_socket:  # Avoid sending the message back to the sender
                    c.send(broadcast_message.encode("utf-8"))

            # If the client sends "close", notify and close connection
            if request.lower() == "close":
                client_socket.send("server closed".encode("utf-8"))
                break
            
            # Send acknowledgment back to the sender
            response = "Message received and broadcasted"
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error when handling client {addr[1]}: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)  # Remove client from the list
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    server_ip = "127.0.0.1"  # Server hostname or IP address
    port = 8000  # Server port number
    try:
        # Create a socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))  # Bind the socket to the host and port
        server.listen()  # Listen for incoming connections
        print(f"Listening on {server_ip}:{port}")

        while True:
            # Accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            clients.append(client_socket)  # Add the client to the list
            
            # Start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()

