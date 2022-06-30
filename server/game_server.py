"""
    Main module for running a rock paper scissor room
    Accepts arguments port, number of rounds
"""

import socket
import time
import sys


HOST = '81.24.11.79'
PORT = 5000
ROUNDS = 5


def set_room_status(port, status):
    with open("ports/"+str(port-5000)+'.txt', 'w+') as f:
        print(status)
        f.write(status)

def send_to_all(connections, msg):
    for c in connections:
        try:
            c.send(msg.encode())
        except socket.error:
            connections.remove(c)
            for c in connections:
                c.send(b'player disconnected.')
                c.close()
            set_room_status(PORT, '0')
            sys.exit("Connection closed.")
            
def send_results(connections, flag):
    for num, c in enumerate(connections):
        if num == flag:
            msg = "won"
        else:
            msg = "lost"
        try:
            c.send(msg.encode())
        except socket.error:
            connections.remove(c)
            for c in connections:
                c.send(b'player disconnected.')
                c.close()
            set_room_status(PORT, '0')
            sys.exit("Connection closed.")
    
    


def player0_wins(results):
    if results[0] == 'rock' and results[1] == 'scissor':
        return True
    elif results[0] == 'paper' and results[1] == 'rock':
        return True
    elif results[0] == 'scissor' and results[1] == 'paper':
        return True
    else:
        return False



def main(port=PORT, rounds=ROUNDS):
    global PORT
    PORT = port
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen(10)
    connections = []
    # display client address
    for i in range(2):
        c, addr = s.accept()
        print("CONNECTION FROM:.", str(addr))

    # send message to the client after
    # encoding into binary string
        msg = "connected, you are player {}.".format(i+1)
        c.send(msg.encode())
        if i == 0:
            set_room_status(port, '1')
            time.sleep(0.1)
            msg = "wait."
            c.send(msg.encode())
        connections.append(c)
        time.sleep(0.1)

    send_to_all(connections, "ready.")
    set_room_status(port, '2')
    round_wins = []

    for i in range(rounds):
        results = []
        time.sleep(0.2)
        send_to_all(connections, "start.")
        for c in connections:
            results.append(c.recv(1024).decode())
        if results[0] != results[1]:
            if player0_wins(results):
                round_wins.append(0)
                send_results(connections, 0)
            else:
                round_wins.append(1)
                send_results(connections, 1)
        else:
            send_to_all(connections, "draw.")

        print(results)

    if round_wins.count(0) > round_wins.count(1):
        final_msg = "player 1 wins the game."
    else:
        final_msg = 'player 2 wins the game.'
    send_to_all(connections, final_msg)
    for c in connections:
        time.sleep(1)
        c.close()

    s.close()
    set_room_status(port, '0')


if __name__ == "_main_":
    if len(sys.argv) > 3:
        main(int(sys.argv[1]). int(sys.argv[2]))
    else:
        main()