import ssl
import socket
import threading
import time
import help

# Global variable to store the received message
received_msg = []
charlie_value = 300
shares = help.split_num_to_shares(charlie_value)
message_to_alice = str(shares[1])
message_to_bob = str(shares[2])
received_msg.append(str(shares[0]))

# Function to start the server
def start_charlie_server():
    global received_msg  # Declare the variable as global to modify it within the function

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

    # Create a server socket that listens for incoming connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(('0.0.0.0', 8445))
        server_sock.listen(5)

        print("Charlie server is listening on port 8445...")

        try:
            while True:
                if len(received_msg) == 3:
                    sum = 0
                    for elem in received_msg:
                        sum += int(elem)
                    hospital_received_msg = False
                    while (not hospital_received_msg):
                        msg_to_hospital = str(sum)
                        try:
                            client_hospital_thread = threading.Thread(target=send_message_to_server, args=(8446, msg_to_hospital,))
                            client_hospital_thread.start()
                            hospital_received_msg = True
                        except:
                            time.sleep(1)

                
                # Accept an incoming connection
                
                conn, addr = server_sock.accept()

                with conn:
                    print(f"Connected by {addr}")

                    with context.wrap_socket(conn, server_side=True) as ssock:
                        data = ssock.recv(1024)
                        if not data:
                            break
                        received_msg.append(data.decode())
                        print(f"Received data: {received_msg}")

                        response_msg = "approved"
                        ssock.sendall(response_msg.encode())

        except KeyboardInterrupt:
            print("Server stopped by Ctrl + C")

def send_message_to_server(port, message):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    
    # Disable certificate verification for self-signed certificates
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Replace 'alice_hostname' with the actual hostname or IP address of Alice's server.
    try:
        with socket.create_connection(('localhost', port)) as sock:
            with context.wrap_socket(sock, server_hostname='localhost') as ssock:
                ssock.sendall(message.encode())
                response = ssock.recv(1024)
        print(response.decode())
        return response.decode()
    except:
        print("Server not responding, waiting 5 seconds untill new msg")
        time.sleep(5)
        send_message_to_server(port=port, message=message)


# Function to get the received message
def get_received_message():
    global received_msg
    return received_msg

if __name__ == '__main__':
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_charlie_server)
    server_thread.start()
    client_thread = threading.Thread(target=send_message_to_server, args=(8443, message_to_bob,))
    client_thread.start()
    client_thread = threading.Thread(target=send_message_to_server, args=(8444, message_to_alice,))
    client_thread.start()

    # The main thread can continue running and provide access to the received message
    
