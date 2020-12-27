import time
from socket import *
from scapy import *

port = 2018
group_name = 'Team TCP/IP\n'
wait_time = 10
udp_port = 13117
buffer_size = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)