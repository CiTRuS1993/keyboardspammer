import time
import socket
import scapy
import parse
import sys
import select
import getch
from scapy.arch import get_if_addr

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

group_name = 'Team TCP/IP\n'
wait_time = 10
udp_port = 13117
buffer_size = 4096
tcp_port = 0
myHostName = socket.gethostname()
server_ip = socket.gethostbyname(myHostName)
my_ip = get_if_addr('eth1')
# print(server_ip)
#print(my_ip)


def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', udp_port))
    print(f"{bcolors.HEADER}Client started, listening for offer requests...{bcolors.ENDC}")
    while True:
        #time.sleep(0.5)
        data, addr = sock.recvfrom(1024)
        # if (addr[1] == udp_port):
        #     print(f"got adress: {addr}")        
        # print(f"got adress: {addr}")
        try:
            tcp_port = int(parse.parse("feedbeef02{}", data.hex())[0], 16)
            if tcp_port == 2118:
                print(f"connectin adress: {addr}")
                sock.close()
                return addr[0], tcp_port  # The server address
        except:
            if (addr[1] == udp_port):
                print("something wrong")


def connect(addr, name, port):
    print(f"Received offer from {addr}, attempting to connect...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print(f"trying to connect to: {addr, port}")
    sock.connect((addr, port))
    # sock.setblocking(0)
    sock.send(name.encode())
    return sock


def game(sock):
    while True: # receive welcome message
        msg = sock.recv(buffer_size).decode()
        if msg:
            print(msg)
            break

    while True: # read and then write to socket
        readable, writable, exceptional = select.select([sock], [], [], 0)
        if len(readable) > 0:
            msg = sock.recv(buffer_size).decode()
            if msg:
                print(msg)
                break
        sock.send(getch.getche().encode())
        print()


while True:
    addr, port = start()
    sock = connect(addr, group_name, port)
    game(sock)
    user_input = input("type 'q' to end client otherwise type anything: ")
    if (user_input == 'q'):
        break

sock.close()