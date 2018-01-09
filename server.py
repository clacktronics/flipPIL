from socket import *
from time import sleep
from threading import Timer
import SimpleHTTPServer
import SocketServer
from config import timeline

s=socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

class perpetualTimer():

   def __init__(self,t,hFunction):
	  self.t=t
	  self.hFunction = hFunction
	  self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
	  self.hFunction()
	  self.thread = Timer(self.t,self.handle_function)
	  self.thread.start()

   def start(self):
	  self.thread.start()

   def cancel(self):
	  self.thread.cancel()


PORT = 1515

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		try:
			query = [self.path.index('?')+1,self.path.index('=')]
			cmd =  self.path[query[0]:query[1]]
		except:
			cmd = ''

		print cmd

		if cmd == "stop":
			st.cancel()
			print cmd
		elif cmd == "start":
			st.start()
			print cmd
		elif cmd == "step":
			sendStep()
			print cmd

		self.path = '/control_panel.html'
		return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

httpd = SocketServer.TCPServer(("", PORT), MyRequestHandler)


i = 0

cmd = ["step",
"forw",
"back",
"clea",
"bonw",
"wonb",
"ints",
"exts"]

def sendStep():
	message = cmd[0]
	s.sendto(message,('',1515))
	print "sent" + message

st = perpetualTimer(1,sendStep)
# st.start()

def main():

	events = []
	for timeEvent in timeline:
		for event in timeline[timeEvent]:
			if event[:4] in ['.mp3','.mp4','.wav']:
				print "playing audio"
			else:
				pass
				#e = lambda event: s.sendto(event,('',1515))
				#events.append(Timer(timeEvent,e))

	for event in events:
		event.start()

	print "Serving at port", PORT
	httpd.serve_forever()

try:
	main()
except (KeyboardInterrupt, SystemExit):
	st.cancel()
	httpd.shutdown()
except Exception as e:
	print e
