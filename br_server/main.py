import socket,threading

def recv_msg(client):
    try:
        while True:
            response = client.recv(1024)
            if len(response) > 0:
                print(response)
            if response.lower() == 'server closed':
                break
    except Exception as e:
        print(f'Error when handling user:{e}')
    finally:
        print('Connection to server is closed')

def run_client():
    try:
        client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        
        server_ip = '127.0.0.1'
        server_port = 8000
        
        client.connect((server_ip,server_port))
        print('Connected to sever')
        
        thread = threading.Thread(target=recv_msg,args=(client,))
        thread.start()
        
        while True:
            message = input('Enter message: ')
            if not message:
                continue
            client.send(message.encode('utf-8')[:1024])
            if message.lower() == 'close':
                break
    except Exception as e:
        print(f'Error:{e}')
    finally:
        client.close()
        print('Connetion to client closed!')


clients = []

def handle_client(socket,addr):
    pass