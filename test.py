import socket

HOST = '0.0.0.0' 
PORT = 8565

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f"Listening on port {PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            print(data)
            if not data:
                break
            conn.sendall(b"Hello from the server!")
