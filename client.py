import time
import socket
import scapy
import parse
import sys
import select
import getch
from scapy.arch import get_if_addr
import ipaddress
import termios
import tty

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
my_ip = get_if_addr('eth1')
broadcast_ip = str(ipaddress.ip_network(my_ip + '/16', False).broadcast_address)


def start():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((broadcast_ip, udp_port))
    except Exception as err:
        print(f"{bcolors.FAIL}UDP create or bind error: {err}{bcolors.ENDC}")
        if(sock != None):
            sock.close()
        return None, None

    print(f"{bcolors.HEADER}Client started, listening for offer requests...{bcolors.ENDC}")
    
    start_time = time.time()
    while (time.time() - start_time <= 10): # receive TCP port over UDP loop
        readable, writable, errored = select.select([sock], [], [], 0)
        if len(readable) > 0:
            try:
                data, addr = sock.recvfrom(1024)
            except Exception as err:
                print(f"{bcolors.FAIL}UDP receive port error: {err}{bcolors.ENDC}")
                sock.close()
                return None, None

            try:
                tcp_port = int(parse.parse("feedbeef02{}", data.hex())[0], 16)
                # if tcp_port == 2118:
                sock.close()
                return addr[0], tcp_port
            except Exception as err:
                # print(f"{bcolors.FAIL}Wrong parse error: {err}{bcolors.ENDC}")
                pass
        time.sleep(1)    
    return None, None


def connect(addr, name, port):
    print(f"Received offer from {addr}, attempting to connect...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((addr, port))
        # sock.setblocking(0)
        sock.send(name.encode())
    except Exception as err:
        print(f"{bcolors.FAIL}TCP connect or send name error: {err}{bcolors.ENDC}")
        sock.close()
        return None
    return sock


def game(sock):
    sock.settimeout(20)
    while True: # receive welcome message
        try:
            msg = sock.recv(buffer_size).decode()
        except Exception as err:
            print(f"{bcolors.FAIL}TCP game receive start message error: {err}{bcolors.ENDC}")
            return
        if msg and len(msg)>0:
            print(msg)
            break
        time.sleep(0.5)

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True: # read and then write to socket
            readable, writable, exceptional = select.select([sock, sys.stdin], [], [], 0)
            if sock in readable:
                try:
                    msg = sock.recv(buffer_size).decode()
                except ConnectionResetError:
                    break
                if msg:
                    print(msg)
                    break
            time.sleep(0.01)

            if sys.stdin in readable:
                try:
                    char = getch.getche()
                except OverflowError:
                    print("change your key")
                try:
                    sock.send(char.encode())
                except (BrokenPipeError, ConnectionResetError):
                    print('server closed, try  again')
                    return
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


while True:
    addr, port = start()
    if(addr and port != None):
        try:
            sock = connect(addr, group_name, port)
            if(sock != None):
                game(sock)
        except ConnectionError:
            print("connection refused")
            continue
        finally:
            if sock is not None:
                sock.close()

    
    user_input = input("type 'q' to end client otherwise type anything: ")
    if (user_input == 'q'):
        break


# hackathon