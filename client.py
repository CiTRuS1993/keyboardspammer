import time
import socket
import scapy
import parse

group_name = 'Team TCP/IP\n'
wait_time = 10
udp_port = 13117
buffer_size = 4096
tcp_port = 0
sock = None
def start():
	sock = socket(socket.AF_INET, socket.SOCK_DGRAM)
	# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('', udp_port))
	while True:
		data, addr = sock.recvfrom(1024)
		try:
			tcp_port = int(parse.parse("feedbeef02{:d}",data.hex())[0]),16)

			return addr  # The server address
		except:
			print("let's try again")

def connect(addr,name):
	print(f"Received offer from {addr}, attempting to connect...")
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((addr, tcp_port))
	sock.setblocking(0)
	sock.send(name)

def game():
	while True:
			msg,_ = sock.recv(buffer_size)
			if msg:
				print(msg)
				break
	while True:
		msg,_ = sock.recv(buffer_size)
		if msg:
			print(msg)
			break
		sock.send(sys.stdin.read(1))

while True:
	addr = start()
	connect(addr,group_name)
	game()
