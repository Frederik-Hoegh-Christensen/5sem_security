import threading
import time
import ssl
import socket
import help

bob_input = 300
message = []
received_val = []


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8081))
    server_socket.listen(3)

    print("Bobs Server is listening on port 8081")
    while True:

        client_socket, addr = server_socket.accept()
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(
            certfile="server_cert.pem", keyfile="server_key.pem")
        ssl_client_socket = ssl_context.wrap_socket(
            client_socket, server_side=True)

        data = ssl_client_socket.recv(1024)
        print(f"Received from client: {data.decode('utf-8')}")
        received_val.append(data.decode('utf-8'))

        response = "Success"
        ssl_client_socket.send(response.encode('utf-8'))

        ssl_client_socket.close()


def client(msg, num_port):
    try:
        # Create a client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        # Replace 'server_ip_address' with your server's IP address
        client_socket.connect(("localhost", num_port))

        # Wrap the client socket in an SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # Use your server's certificate
        ssl_context.load_verify_locations("server_cert.pem")

        ssl_client_socket = ssl_context.wrap_socket(
            client_socket, server_hostname='localhost')

        # Send a request to the server
        request = msg
        ssl_client_socket.send(request.encode('utf-8'))

        # Receive the server's response
        response = ssl_client_socket.recv(1024)
        print(f"Received from server: {response.decode('utf-8')}")

        # Close the connection
        ssl_client_socket.close()
    except:
        time.sleep(5)
        print('Waiting for server...')
        client(msg, num_port)


def main():

    # Split input into three shares
    result = help.SplitToShare(message, bob_input)

    # Converting shares in order to send them
    str_convert = [str(i) for i in result]

    # Starting server
    server_thread = threading.Thread(target=server)
    server_thread.start()

    # Launching client with alices server as port, in a thread
    client_thread = threading.Thread(
        target=client(str_convert[1], 8080))
    client_thread.start()

    # Launching client with charlies server as port, in another thread
    client_thread = threading.Thread(
        target=client(str_convert[2], 8082))
    client_thread.start()

    # Calculating sum to send to hospital
    while len(received_val) < 2:
        pass
    received_val1 = received_val[0]
    received_val2 = received_val[1]
    ShareSumToSend = help.CalculateShares(
        str_convert[0], received_val1, received_val2)

    # converting sum to be able to send it
    bob_sum = str(ShareSumToSend)
    print("Bobs sum to be send to hospital:", bob_sum)

    # Launching client with hospitals server as port, in a final thread
    client_thread = threading.Thread(
        target=client(bob_sum, 8083))
    client_thread.start()


if __name__ == "__main__":
    main()
