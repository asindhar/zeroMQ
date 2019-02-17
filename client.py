import zmq, subprocess
from datetime import datetime

#Constants
HOST = '127.0.0.1'
PORT = '8080'

def zmq_sub():
	context = zmq.Context()						#Create zmq context
	sock = context.socket(zmq.SUB)				#Create a socket in zmq context for subscriber
	publisher = "tcp://" + HOST + ":" + PORT	#Adress of server for publisher
	sock.connect(publisher)


	#subscribe for 'Server Time' messages on the socket
	sock.setsockopt(zmq.SUBSCRIBE, b"Server Time")

	print("Client subsrcibed for messages on "+ publisher)

	#Start timer for RTT
	t1 = datetime.now()

	#Recieve one message and stop 
	server_time = sock.recv()
	#deconde from bytes to string and strip away Server Time from message
	server_time = server_time.decode("utf-8")[12:]

	#Stop timer for RTT
	t2 = datetime.now()
	RTT = (t2 - t1) / 2

	print("Date-Time received from server: ", server_time )
	print("RTT: ", RTT)

	#Add RTT to server time
	dt = datetime.strptime(server_time, '%m%d%H%M%y.%S') + RTT
	print("Date-Time with RTT: ", dt)

	#format the date object to a string - month:day:hour:min:year.sec 
	#ex 0206180219.59
	# Unix date command only change time upto seconds level
	dt_str = dt.strftime('%m%d%H%M%y.%S')

	return dt_str
	


if __name__ == '__main__':
	server_time = zmq_sub()
	#Run sudo command date for changing client time
	subprocess.run(["sudo","date", server_time])