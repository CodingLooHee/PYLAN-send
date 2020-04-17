import socket
import multiprocessing

def isIpConectable(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    result = sock.sendto(b'check', (ip, 5005))
    sock.close()
    return ip if result == 0 else False
def ipLocator():
    pool = multiprocessing.Pool(processes=4)
    return [i for i in pool.map(isIpConectable, ['192.168.1.' + str(i) for i in range(0,255)]) if i != False]

def serverBackground():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 5005))
    while True:
        data, addr = server.recvfrom(1024)
        print(addr, data)
        if data == b'check':
            server.sendall(b'ready')
            print('yay')

if __name__ == '__main__':
    multiprocessing.Process(target=serverBackground, args=()).start()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        server_addr_list = ipLocator()
        print('Who do you want to send message to?')
        print('0. Refresh')
        for index, server_addr in enumerate(server_addr_list):
            print(f'{index}:\t{server_addr}')
        print()
        while True:
            select = input('Select: ')
            if select == '0':
                break
        print()