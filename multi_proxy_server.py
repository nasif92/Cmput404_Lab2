import socket,  sys
from multiprocessing import Process

HOST = "localhost"
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

# send data to google and send response to client
def handle_request(conn, proxy_end):
	send_full_data = conn.recv(BUFFER_SIZE)
	print("Sending received data to google")
	proxy_end.sendall(send_full_data)
	proxy_end.shutdown(socket.SHUT_WR)

	data = proxy_end.recv(BUFFER_SIZE)
	print("Sending received data to to client")
	conn.send(data)

def main():
	extern_host = "www.google.com"
	extern_port = 80
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as proxy_start:
		print("Starting multi proxy server")
		proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		proxy_start.bind((HOST, PORT))
		proxy_start.listen(1)

		while True:
			conn, addr = proxy_start.accept()
			print("Connected by", addr)
			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
				print("Connecting to Google")
				remote_ip = get_remote_ip(extern_host)
				proxy_end.connect((remote_ip, extern_port))
				p = Process(target = handle_request, args=(conn,  proxy_end))
				p.daemon = True
				p.start()
				print("Start process:", p)
			conn.close()
            
if __name__ == "__main__":
    main()