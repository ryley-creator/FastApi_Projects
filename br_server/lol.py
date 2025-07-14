# import socket
# import threading


# def for_thread(client):
#     while True:
#         response = client.recv(1024)
#         response = response.decode('utf-8')
#         if len(response) > 0:
#             if response.lower() == "closed":
#                 break
#             print(f"Received: {response}")
#     print("Connection to server closed")  
    

# def run_client():
#     # create a socket object
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     server_ip = "127.0.0.1"  # replace with the server's IP address
#     server_port = 8000  # replace with the server's port number
#     # establish connection with server
#     client.connect((server_ip, server_port))
#     thread = threading.Thread(target=for_thread,args=(client,))
#     thread.start()
#     try:
#         while True:
#             msg = input("Enter message: ")
#             client.send(msg.encode("utf-8")[:1024])
         
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         client.close()
# run_client()



# import socket
# import threading

# clients = []

# def handle_client(client_socket, addr):
#     try:
#         while True:
#             # receive and print client messages
#             request = client_socket.recv(1024).decode("utf-8")
#             print(clients)
#             for c in clients:
#                 c.send(request.encode('utf-8'))
#             if request.lower() == "close":
#                 client_socket.send("closed".encode("utf-8"))
#                 break
#             print(f"Received: {request}")
#             # convert and send accept response to the client
#             response = "accepted"
#             client_socket.send(response.encode("utf-8"))
#     except Exception as e:
#         print(f"Error when hanlding client: {e}")
#     finally:
#         client_socket.close()
#         print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


# def run_server():
#     server_ip = "127.0.0.1"  # server hostname or IP address
#     port = 8000  # server port number
#     # create a socket object
#     try:
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         # bind the socket to the host and port
#         server.bind((server_ip, port))
#         # listen for incoming connections
#         server.listen()
#         print(f"Listening on {server_ip}:{port}")

#         while True:
#             # accept a client connection
#             client_socket, addr = server.accept()
#             print(f"Accepted connection from {addr[0]}:{addr[1]}")
#             clients.append(client_socket)
            
#             # start a new thread to handle the client
#             thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
#             thread.start()
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         server.close()

# run_server()