from re import L
import socket
import sys
import os
import game_server
import time


HOST = '81.24.11.79'
PORT = 5000

active_rooms = 0
connections = []
code_map = {}
active_map = [0] * 20


def read_status(name):
    try:
        with open(name, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return '0'


def get_all_status():
    names = os.listdir("ports")
    res = []
    res2 = []
    for name in names:
        ds = read_status("ports/"+name)
        if ds == "1":
            res.append(int(name.split(".")[0]))
        elif ds == "2":
            res2.append(int(name.split(".")[0]))
    return res, res2


def main():
    global active_rooms
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    while True:
        try:
            c, addr = s.accept()
            msg = "connected"
            c.send(msg.encode())
            choice = c.recv(1024).decode()
            command, option = choice.split('.')
            time.sleep(0.1)
            if command == "create":
                active_rooms += 1
                if active_rooms == 20:
                    active_rooms = 1
                code_map[option] = active_rooms
                c.send(str(active_rooms).encode())
                id = os.fork()
                if id == 0:
                    game_server.main(PORT + active_rooms, 5)
                    exit(0)
            elif command == "join":
                if option[0] == "x":
                    room = option[1:]
                    status = read_status("ports/"+option[1:] + ".txt")
                elif option in code_map:
                    room = code_map[option]
                    status = read_status("ports/"+str(code_map[option])+".txt")
                if status == "1":
                    c.send(str(room).encode())
                elif status == "2":
                    c.send(b"Room full")
                elif status == '0':
                    c.send(b"Room closed")
            elif command == "open":
                op, active = get_all_status()
                print(op, active)
                message1 = str(op)
                message2 = str(active)
                c.send(message1[1:-1].encode() +
                       b'.' + message2[1:-1].encode())
            else:
                msg = "invalid"
                c.send(msg.encode())
            c.close()
        except Exception as e:
            print(e)
            continue
        except KeyboardInterrupt:
            s.close()
            print("\nServer closed")
            exit(0)


if __name__ == "__main__":
    with open("server_config.txt", "r") as f:
        HOST = f.readline().strip()
        PORT = int(f.readline().strip())
    main()