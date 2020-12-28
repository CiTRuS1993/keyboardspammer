
import _thread
import time
import random
import socket
import parse
from scapy.arch import get_if_addr
import select

num_of_threads = []
tcp_port = 2118
server_name = 'HackerzServer\n'
wait_time = 10
udp_port = 13117
buffer_size = 4096
# global game_status 
game_status = {'stat':False}
score = {}
groups = {'Group 1': [], 'Group 2':[]}
myHostName = socket.gethostname()
# server_ip = socket.gethostbyname(myHostName)
server_ip = get_if_addr('eth0')
# server_ip = 'localhost'
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# udp_socket.bind((server_ip, udp_port))
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((server_ip, tcp_port))
tcp_socket.listen(1)

def start():
    while True:
        # game_status['stat'] = False
        groups['Group 1'] = []
        groups['Group 2'] = []
        score = {}
        try:
            num_of_threads.append(1)
            _thread.start_new_thread(tcp_master,())
        except Exception as err:
            print(err)
        try:
            num_of_threads.append(1)
            _thread.start_new_thread(udp_broadcast,())
        except Exception as err:
            print(err)
        time.sleep(10)
        while len(num_of_threads) > 0:
            pass
        user_input = input("To quit enter 'quit' text")
        if (user_input == 'quit'):
            break

def udp_broadcast():
    start_time = time.time()
    while(time.time() - start_time <= 10):
        msg = bytes.fromhex('feedbeef02') + \
                            (tcp_port).to_bytes(2, byteorder='big')
        udp_socket.sendto(msg, ('<broadcast>', udp_port))
    num_of_threads.pop()


def tcp_master():
    print(f"Server started, listening on IP address {server_ip}")
    name_list = list()
    start_time = time.time()
    while(time.time() - start_time <= 10):
        readable, writable, errored = select.select([tcp_socket], [], [],0)
        if len(readable)>0:
            client_socket, addr = tcp_socket.accept()
            name = client_socket.recv(buffer_size).decode()
            print(name)
            name_counter = 1
            while name in name_list:
                name_counter += 1
                name += str(name_counter)
            groups['Group 1'].append((name, client_socket, addr)) if len(groups['Group 1']) >= len(
                groups['Group 2']) else groups['Group 2'].append((name, client_socket, addr))
        # client_socket.settimeout(time.time() - start_time)

    start_game_message = 'Welcome to Keyboard Spamming Battle Royale.\n'
    # group_1_names = [name for name in groups['Group 1']]
    # group_2_names = [name for name in groups['Group 2']]

    # group_1_names_str = '\n'.join(group_1_names)
    # start_game_message += 'Group 1:\n==\n'
    # start_game_message += group_1_names_str

    # group_2_names_str = '\n'.join(group_2_names)
    # start_game_message += 'Group 2:\n==\n'
    # start_game_message += group_2_names_str

    for key, value in groups.items():
        for (name, socket, addr) in value:
            num_of_threads.append(1)
            _thread.start_new_thread(
                client_run, (name, socket, addr, start_game_message))

    game_status['stat'] = True
    time.sleep(10)
    game_status['stat'] = False
    print(get_scores())
    num_of_threads.pop()


def client_run(name, socket, addr, msg):
    socket.send(msg.encode())
    score[name] = 0
    while not game_status['stat']:
        pass
    while game_status['stat']:
        readable, writable, errored = select.select([socket], [], [],0)
        if len(readable)>0:
            char = socket.recv(1)
            score[name] += 1
    socket.send("finished".encode())
    num_of_threads.pop()



def get_scores():
    group1_score = sum([score[team] for (team, _, _) in groups['Group 1']])
    group2_score = sum([score[team] for (team, _, _) in groups['Group 2']])
    return group1_score, group2_score

start()
