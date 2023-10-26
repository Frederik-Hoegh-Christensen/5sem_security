import ssl
import socket
import threading


received_msg = []

def start_hospital_server():
    global received_msg  # Declare the variable as global to modify it within the function

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

    # Create a server socket that listens for incoming connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(('0.0.0.0', 8446))
        server_sock.listen(5)

        print("Hospital server is listening on port 8446...")

        try:
            while True:
                if len(received_msg) == 3:
                    sum = 0
                    for elem in received_msg:
                        sum += int(elem)
                    print("Final aggregated value: ", sum)
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

if __name__ == '__main__':
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_hospital_server)
    server_thread.start()