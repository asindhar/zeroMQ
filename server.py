import zmq, sys, os
from datetime import datetime

#Constants
HOST = '127.0.0.1'
PORT = '8080'
	
context = zmq.Context()						#Create zmq context
sock = context.socket(zmq.PUB)				#Create a socket in zmq context for publisher
publisher = "tcp://" + HOST + ":" + PORT	#Adress of server for publisher
sock.bind(publisher)						#Bind the publisher address to zmq socket

print("Server is ready to publish on - ", publisher)

publish_time = True

def server_time():
	#get server time
	dt = datetime.now()
	#return datetime string and encode to bytes for zmq
	return datetime.strftime(dt ,'%m%d%H%M%y.%S').encode('utf-8')

print("Press Ctrl+c to interrupt sending messages from server otherwise server will keep publishing every 2 sec...")
#Keeping sending server time until KeyboardInterrupt
while publish_time:
	try:
		#Send server time every 2 seconds
		time.sleep(2)
		sock.send(b"Server Time " + server_time())
	except KeyboardInterrupt:
		print('\n Session closed...')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)