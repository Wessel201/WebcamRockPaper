import socket
import time
import sys
import random
import steen_schaar


class Client():
    def __init__(self, start_function, receive_func, command, option):
        self.start_function = start_function
        self.command = command
        self.option = option
        self.get_host()
        self.receive_func = receive_func
        self.last_move = ''


    def get_host(self):
        try:
            with open("client_config.txt", "r") as f:
                self.host = f.readline().strip()
                self.port = int(f.readline().strip())
        except FileNotFoundError:
            print("Please run client_install.py first")
            sys.exit(1)

    def run_startup(self):
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        msg = s.recv(1024)
        print('Received:' + msg.decode())
        msg = self.command + '.' + self.option
        s.send(msg.encode())
        msg = s.recv(1024).decode()
        s.close()
        if self.command == "open":
            print(msg)
            return msg
        if msg.isdigit() is False:
            print(msg)
            return msg
        port = self.port + int(msg)
        self.start_game(port)

    def start_game(self, port):
        self.s = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM)
        self.s.connect((self.host, port))
        msg = self.s.recv(1024)

        while msg:
            bericht = msg.decode()
            for command in bericht.split('.'):
                if command == "":
                    continue
                self.run_command(command)
            msg = self.s.recv(1024)
        print("game over")

        # disconnect the client
        self.s.close()

    def run_command(self, command):
        print('Received:' + command)
        if command == 'start':
            choice = self.start_function()
            self.last_move = choice
            time.sleep(1)
            self.receive_func('send' + ' ' + choice, self.last_move)
            print("sending result", choice)
            self.s.send(choice.encode())
            
        else:
            self.receive_func(command, self.last_move)


def demonstration():
    print("Pick 1 for rock, 2 for paper, 3 for scissors")
    a = int(input("Your choice: "))
    if a == 1:
        return "rock"
    elif a == 2:
        return "paper"
    elif a == 3:
        return "scissor"
    else:
        print("wrong input default = rock")
        return "rock"


def random_pick():
    return random.choice(picks)


def test_receive(command, move):
    print(command)
    print(move)



picks = ['rock', 'paper', 'scissor']


if __name__ == "__main__":
    speler = Client(random_pick, test_receive,  sys.argv[1], sys.argv[2]).run_startup()
    # Client(random_pick, test_receive, sys.argv[1], sys.argv[2]).run_startup()
