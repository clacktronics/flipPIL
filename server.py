from socket import *
from time import sleep

s=socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

i = 0

cmd = ["step",
"forw",
"back",
"clea",
"bonw",
"wonb",
"ints",
"exts"]

while True:
	if i < len(cmd)-1 : i += 1
	else: i = 0

	message = cmd[i]
	s.sendto(message,('',1515))
	print message
	sleep(0.5)
