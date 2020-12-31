import _thread
from art import *
import time
import random
import socket
import parse
from scapy.arch import get_if_addr
import select
import ipaddress

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

middle_finger =  r"""
        
           __
          / |\
          |   |
          |   |
          |   |
          |   |
        __|   |__
     __/  \  _/__\___
    /  \   |/        \
    |   |  |______    |
    |\  |  |  |  |    |
    | '-\__'  '--'   |
    \         (     /
     \             /
      |            |
    """

tcp_love = r"""
____________36936936936936936
____________36936936936936936
____________369369369369369369
___________36936936936936933693
__________3693693693693693693693
_________369369369369369369369369
_________3693693693693693693693699
________3693693693693693693693699369
_______36936939693693693693693693693693
_____3693693693693693693693693693693636936
___36936936936936936936936936936___369369369
__36936___369336936369369369369________36936
_36936___36936_369369336936936__¶¶__¶¶
36933___36936__36936___3693636_¶¶¶¶¶¶¶¶
693____36936__36936_____369363_¶¶¶¶¶¶¶¶
______36936__36936______369369__¶¶¶¶¶¶
_____36936___36936_______36936___¶¶¶¶
_____36936___36936________36936___¶¶
_____36936___36936_________36936___11,
______369____36936__________369___11,
______________369________________11,
TCP____________________________11,
___TCP_______________________11,
______TCP__________________11,
_________TCP____________¶¶¶_¶¶¶
____________TCP________¶¶¶¶¶¶¶¶¶
_______________TCP_____¶¶¶¶¶¶¶¶¶
__________________TCP___¶¶¶¶¶¶¶
_____________________TCP_¶¶¶¶¶
TCP_______________________¶¶¶
___TCP_____________________¶
______TCP_____________________11,
_________TCP____________________11,
____________TCP___________________11,
_______________TCP_________________11,
__________________TCP______________11,
_____________________TCP__________11,
________________________TCP______11,
___________________________TCP_11,
TCP________________________¶¶__¶¶
___TCP____________________¶¶¶¶¶¶¶¶
______TCP_________________¶¶¶¶¶¶¶¶
_________TCP_______________¶¶¶¶¶¶
____________TCP_____________ ¶¶¶
_______________TCP___________ ¶
__________________TCP_______11,
_____________________TCP__11,
__________________________11,
____________________________11,
TCP___TCP___TCP___TCP___TCP___11,
___TCP___TCP___TCP___TCP___TCP__11,
__________________________________11,
______________369___________________11,
______369____36936__________369_____11,
_____36936___36936_________36936___11,
_____36936___36936________36936___11,
_____36936___36936_______36936___11,
______36936__36936______369369 _¶¶_¶¶
693____36936__36936_____369363 ¶¶¶¶¶¶¶
36933___36936__36936___3693636 ¶¶¶¶¶¶¶
_36936___36936_369369336936936 _¶¶¶¶¶
__36936___369336936369369369369 _¶¶¶__3696
___36936936936936936936936936936 _¶_336939
_____36936936936936936936936936936936936
_______369369396936936936936936693693
________36936936936936936936999369
_________36936936936936936933699
_________3693693693693693369369
__________36936936936936993693
___________369369369369333693
____________3693693693699369
____________369369369366936
____________36936936936693
"""

tcp_port = 2118
wait_time = 10
udp_port = 13117
buffer_size = 4096
server_ip = get_if_addr('eth2')
broadcast_ip = str(ipaddress.ip_network(server_ip + '/16', False).broadcast_address)

num_of_threads = []
score = {}
game_status = {'stat': False}
groups = {'Group 1': [], 'Group 2': []}
stats = {'group_name:': 'none', 'score': 0, "num_of_games": 0}

def udp_broadcast():
    start_time = time.time()
    while (time.time() - start_time <= 10):
        msg = bytes.fromhex('feedbeef02') + \
            (tcp_port).to_bytes(2, byteorder='big')
        try:
            udp_socket.sendto(msg, (broadcast_ip, udp_port))
        except Exception as err:
            print(f"{bcolors.FAIL}Server UDP send error {err}{bcolors.ENDC}")
            pass
        time.sleep(1)

    num_of_threads.pop()
    return

# hackathon
def tcp_master():
    print(f"{bcolors.WARNING}Server started, listening on IP address {server_ip}{bcolors.ENDC}")
    name_list = list()
    start_time = time.time()
    while (time.time() - start_time <= 10):
        readable, writable, errored = select.select([tcp_socket], [], [], 0)
        if len(readable) > 0:
            try:
                client_socket, addr = tcp_socket.accept()
                name = client_socket.recv(buffer_size).decode()
                print(name)
            except Exception as err:
                print(f"{bcolors.FAIL}Server accept or receive error {err}{bcolors.ENDC}")
                continue

            name_counter = 1
            while name in name_list:
                name_counter += 1
                name = name[:-1] + str(name_counter)+"\n"
            name_list.append(name)
            groups['Group 1'].append((name, client_socket, addr)) if len(groups['Group 1']) <= len(
                groups['Group 2']) else groups['Group 2'].append((name, client_socket, addr))
        # client_socket.settimeout(time.time() - start_time)
        time.sleep(0.5)

    stats['num_of_games'] += 1
    start_game_message = "Welcome to Keyboard Spamming Battle Royale.\n\n"
    group_1_names = [name for (name, client_socket, addr) in groups['Group 1']]
    group_2_names = [name for (name, client_socket, addr) in groups['Group 2']]

    group_1_names_str = '\n'.join(group_1_names)
    start_game_message += bcolors.OKBLUE + "Group 1:\n==\n"
    start_game_message += group_1_names_str + bcolors.ENDC

    group_2_names_str = '\n'.join(group_2_names)
    start_game_message += bcolors.OKGREEN + '\nGroup 2:\n==\n'
    start_game_message += group_2_names_str + bcolors.ENDC
    start_game_message += bcolors.OKCYAN + "\nStart Typing!!\n\n" + bcolors.ENDC

    print(start_game_message)

    for key, value in groups.items():
        for (name, socket, addr) in value:
            num_of_threads.append(1)
            _thread.start_new_thread(
                client_run, (name, socket, addr, start_game_message))

    print(f"{bcolors.WARNING}Game is running{bcolors.ENDC}")
    game_status['stat'] = True
    time.sleep(10)
    game_status['stat'] = False
    #print(get_scores())
    print(f"{bcolors.WARNING}Game is finished{bcolors.ENDC}")
    num_of_threads.pop()
    return

# hackathon
def client_run(name, socket, addr, msg):
    socket.send(msg.encode())
    score[name] = 0
    while not game_status['stat']:
        time.sleep(1)
        pass
    while game_status['stat']:
        readable, writable, errored = select.select([socket], [], [], 0)
        if len(readable) > 0:
            char = socket.recv(1).decode()
            score[name] += 1
        time.sleep(0.1)
    try:
        socket.send(get_end_message().encode())
        socket.close()
    except Exception as err:
        print(f"{bcolors.FAIL}Server-Client thread send end msg error: {err}{bcolors.ENDC}")

    num_of_threads.pop()
    return
# hackathon
def get_end_message():
    end_message= "Game over!\n"
    scores = get_scores()
    for i in range(len(scores)):
        end_message += "Group "+str(i+1)+" typed "+str(scores[i])+" chars!\n"
    end_message+= "Group "+str(scores.index(max(scores))+1) + " wins!\n"
    if  scores[0] > scores[1]:
        end_message+="The winners are: ".join([name for (name,_,_) in groups['Group 1']])
    else:
        end_message+="The winners are: ".join([name for (name,_,_) in groups['Group 2']])

    end_message+="************\n"
    end_message+= "Server record is: " + str(stats['score']) + " by team " + stats['name']
    end_message += tcp_love#middle_finger

    return end_message
# hackathon
def get_scores():
    group1_score = sum([score[team] for (team, _, _) in groups['Group 1']])
    group2_score = sum([score[team] for (team, _, _) in groups['Group 2']])
    for team in score.keys():
        if score[team]> stats['score']:
            stats['score'] = score[team]
            stats['name'] = team

    return group1_score, group2_score

try:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except Exception as err:
    print(f"{bcolors.FAIL}Server UDP create error {err}{bcolors.ENDC}")
    exit()

try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((server_ip, tcp_port))
    tcp_socket.listen()
except Exception as err:
    print(f"{bcolors.FAIL}Server TCP create error {err}{bcolors.ENDC}")
    exit()

while True:

    groups['Group 1'] = []
    groups['Group 2'] = []
    score = {}

    try:
        num_of_threads.append(1)
        _thread.start_new_thread(tcp_master, ())
    except Exception as err:
        print(err)

    try:
        num_of_threads.append(1)
        _thread.start_new_thread(udp_broadcast, ())
    except Exception as err:
        print(err)

    while len(num_of_threads) > 0:
        time.sleep(5)
        pass

    user_input = input("type 'q' to end server otherwise type anything: ")
    if (user_input == 'q'):
        break

udp_socket.close()
tcp_socket.close()

#start()

# hackathon