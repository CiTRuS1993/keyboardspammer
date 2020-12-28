import time
import socket
import scapy
import parse
import sys
import select

group_name = 'Team TCP/IP\n'
wait_time = 10
udp_port = 13117
buffer_size = 4096
tcp_port = 0
myHostName = socket.gethostname()
# server_ip = socket.gethostbyname(myHostName)
server_ip = 'localhost'


def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', udp_port))
    print("Client started, listening for offer requests...")
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            tcp_port = int(parse.parse("feedbeef02{}", data.hex())[0], 16)
            if tcp_port == 2118:
                return addr[0], tcp_port  # The server address
        except:
            print("let's try again")


def connect(addr, name, port):
    print(f"Received offer from {addr}, attempting to connect...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    # sock.setblocking(0)
    sock.send(name.encode())
    return sock


def game(sock):
    while True:
        msg = sock.recv(buffer_size)
        if msg:
            print(msg)
            break
    while True:
        readable, writable, exceptional = select.select([sock], [], [], 0)
        if len(readable) > 0:
            msg = sock.recv(buffer_size)
            if msg:
                print(msg)
                break
        sock.send(sys.stdin.read(1).encode())


while True:
    addr, port = start()
    sock = connect(addr, group_name, port)
    game(sock)
    user_input = input("type exit to end game otherwise type anything")
    if (user_input == 'exit'):
        break
