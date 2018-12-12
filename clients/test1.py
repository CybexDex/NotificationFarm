
import sys
import zmq


#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")

if len(sys.argv) < 3:
    print('run <port> <topic>')
    exit(1)
socket.connect("tcp://localhost:"+ sys.argv[1])

# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[2] 

# Python 2 - ascii bytes to unicode str
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

# Process 5 updates
total_temp = 0
for update_nbr in range(50):
    string = socket.recv_string()
    print string

