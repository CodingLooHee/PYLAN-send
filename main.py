import socket
import os

PORT = 5005

def mode_receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = socket.gethostbyname(socket.gethostname())
    try:
        server.bind((ADDR, PORT))
    except:
        print('Can\'t bind server')
        return
    server.listen(1)
    print('-' * 20)
    print(f'Address:\t{ADDR}')
    print(f'Port:\t\t{PORT}')
    print('-' * 20)
    while True:
        cmd_mode_name = False
        cmd_mode_name_tempname = ''
        conn, client_addr = server.accept()
        print(f'Connected by {client_addr}')
        while True:
            data = conn.recv(1024)

            if not data:
                conn.close()
                try:
                    file.close()
                    print('File received')
                except:
                    pass
                break


            try:
                if data == 'SET_NAME'.encode():
                    cmd_mode_name = True
                elif cmd_mode_name:
                    cmd_mode_name_tempname = data
                    cmd_mode_name = False
                    file = open(cmd_mode_name_tempname, 'wb')
                else:
                    file.write(data)
            except Exception as err:
                print('Something went wrong')
                print(err)
                try:
                    conn.close()
                    file.close()
                except:
                    pass
                break

                
            

def mode_send():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Enter server address')
    ADDR = input('Address: ')
    try:
        client.connect((ADDR, PORT))
    except:
        print('Invalid')
        return
    
    try:
        filename = input('File: ').replace('"', '')
        file = open(filename, 'rb')
    except:
        print('Unable to open file')
        return
    
    client.sendall('SET_NAME'.encode())
    client.sendall(os.path.basename(filename).encode())
    for chunk in iter(file.read, b''):
        client.send(chunk)
    
    client.close()


while True:
    print('Select mode')
    print('1. Receive mode')
    print('2. Send mode')
    print()
    while True:
        select = input('Mode: ')
        if select == '1':
            mode_receive()
            break
        if select == '2':
            mode_send()
            break
        print('Invalid')