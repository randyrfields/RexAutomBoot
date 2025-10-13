import socket

HOST = '192.168.1.248'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)  # Receive up to 1024 bytes
            if not data:
                break  # Exit loop if no data received (client disconnected)
            # conn.sendall(data) # Echo the received data back to the client
            print(data)