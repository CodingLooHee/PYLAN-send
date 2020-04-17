import socket
import multiprocessing

def serverRecv():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 5005))
    while True:
        data, addr = server.recvfrom(1024)
        if data == b'check_test':
            server.sendto(b'check_ok', addr)
        else:
            print(data)

if __name__ == '__main__':
    server_worker = multiprocessing.Process(target=serverRecv, args=())
    server_worker.start()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            client.sendto(b'check_test', ('127.0.0.1', 5005))
            print(client.recvfrom(1024))
        except ConnectionResetError:
            pass
        except Exception as err:
            server_worker.terminate()
            raise(err)