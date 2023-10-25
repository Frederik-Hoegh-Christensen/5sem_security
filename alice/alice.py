import socket
import ssl

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 4433))
server_socket.listen(5)

# Load SSL/TLS certificate and key files
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='server_cert.pem', keyfile='server_key.pem')

# Accept incoming connections with TLS
while True:
    client_socket, addr = server_socket.accept()
    ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)

    # Now, you can use ssl_socket to send and receive data securely
    data = ssl_socket.recv(1024)
    print(data)
    print(data.decode('utf-8'))

    # Close the connection
    ssl_socket.close()
