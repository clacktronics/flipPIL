import socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost',1515))

while True:
	m=s.recvfrom(4)
	print m[0]
	print "nop"
