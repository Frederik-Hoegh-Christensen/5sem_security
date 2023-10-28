import socket
import ssl
import threading
import help


received_val = []


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8083))
    server_socket.listen(3)

    print("Hospital Server is listening on port 8083")
    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()

        # Wrap the client socket in an SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # Use your own certificate and key
        ssl_context.load_cert_chain(
            certfile="server_cert.pem", keyfile="server_key.pem")

        ssl_client_socket = ssl_context.wrap_socket(
            client_socket, server_side=True)

        # Receive data from the client
        data = ssl_client_socket.recv(1024)
        print(f"Received from client: {data.decode('utf-8')}")
        received_val.append(data.decode('utf-8'))

        # Send a response
        response = "The hospital has received your data"
        ssl_client_socket.send(response.encode('utf-8'))

        # Close the connection
        ssl_client_socket.close()


def main():
    server_thread = threading.Thread(target=server)
    server_thread.start()

    while len(received_val) < 3:
        pass

    received_val1 = received_val[0]
    received_val2 = received_val[1]
    received_val3 = received_val[2]

    AggregateSum = help.CalculateShares(
        received_val1, received_val2, received_val3)
    print("The AggregateSum", AggregateSum)


if __name__ == "__main__":
    main()
