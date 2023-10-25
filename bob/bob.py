import socket
import ssl

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establish a TLS connection to the server
ssl_socket = ssl.wrap_socket(client_socket, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLSv1)
ssl_socket.connect(('localhost', 4433))  # Replace 'server_address' with the actual address of your server

# Send data securely
data_to_send = "Hello from the client!"
ssl_socket.send(data_to_send.encode('utf-8'))

# Receive and print data from the server
data_received = ssl_socket.recv(1024)
print(data_received.decode('utf-8'))

# Close the connection
ssl_socket.close()
