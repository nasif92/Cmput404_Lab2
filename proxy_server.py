import socket, time, sys

# define global addresses and buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get ip
def get_remote_ip(host):
	print("Getting IP for",  host)
	try:
		remote_ip = socket.gethostbyname(host)
	except:
		print("Hostname could not be resolved. Exiting")
		sys.exit()

	print("IP address of", host, "is", remote_ip)
	return remote_ip

def main():
	# Question 6 addresss
	host = 'www.google.com'
	port = 80

	# create socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		print("Starting proxy server")

		#QUESTION 3
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)
		
		#continuously listen for connections
		while True:
			conn, addr = s.accept()
			print("Connected by", addr)
			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
				print("Connecting to Google")	
				remote_ip = get_remote_ip(host)
				proxy_end.connect((remote_ip,port))

				# send data
				send_full_data = conn.recv(BUFFER_SIZE)
				print("Sending received data", send_full_data, "to google")
				proxy_end.sendall(send_full_data)

				# shut down
				proxy_end.shutdown(socket.SHUT_WR)

				data = proxy_end.recv(BUFFER_SIZE)
				print("Sending received data", data,"to client")
				conn.send(data)

			conn.close()

if __name__ == "__main__":
    main()