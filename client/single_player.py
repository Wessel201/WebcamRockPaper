import steen_schaar
import random


def com_win(move):
    if move == 'scissor':
        return ('rock', 1)
    elif move == 'rock':
        return ('paper', 1)
    elif move == 'paper':
        return ('scissor', 1)


def com_lose(move):
    if move == 'scissor':
        return ('paper', 0)
    elif move == 'rock':
        return ('scissor', 0)
    elif move == 'paper':
        return ('rock', 0)


def com_draw(move):
    if move == 'scissor':
        return ('scissor', 2)
    elif move == 'rock':
        return ('rock', 2)
    elif move == 'paper':
        return ('paper', 2)


def random_com_move(player_move):
    num = random.randint(0, 100)

    com_move = ''
    if num < 55:
        com_move, result = com_win(player_move)
    elif num >= 55 and num < 85:
        com_move, result = com_lose(player_move)
    else:
        com_move, result = com_draw(player_move)
    return (com_move, result)


def show_winner(results):
    winner = max(set(results), key=results.count)
    if winner == 0:
        print('----------------------------')
        print('Goed gedaan je hebt gewonnen')
        print('----------------------------')
    elif winner == 1:
        print('----------------------------')
        print('helaas je hebt verloren')
        print('----------------------------')
    else:
        print('----------------------------')
        print('Jammer het is gelijk spel niemand wint')
        print('----------------------------')


def basic_com():
    results = []
    for i in range(5):
        com_move, result = random_com_move()
        print('computer koos', com_move)
        if result == 0:
            print('je hebt deze ronde gewonnen')
            results.append(0)
        elif result == 1:
            print('je hebt deze ronde verloren')
            results.append(1)
        else:
            print('het is gelijk spel deze ronde')
            results.append(2)
    show_winner(results)


def get_winner(player, com):
    if player == 'scissor' and com == 'rock':
        return 1
    elif player == 'scissor' and com == 'paper':
        return 0
    elif player == 'scissor' and com == 'scissor':
        return 2
    elif player == 'paper' and com == 'rock':
        return 0
    elif player == 'paper' and com == 'paper':
        return 2
    elif player == 'paper' and com == 'scissor':
        return 1
    elif player == 'rock' and com == 'rock':
        return 2
    elif player == 'rock' and com == 'paper':
        return 1
    elif player == 'rock' and com == 'scissor':
        return 0


def add_win(result, moves, wins, com_move):
    if result == 0:
        print('je hebt deze ronde gewonnen')
        wins.append(0)
        return random.choice(moves)
    elif result == 1:
        print('je hebt deze ronde verloren')
        wins.append(1)
        com_move, _ = com_win(com_move)
        return com_move
    elif result == 2:
        print('het is gelijk spel deze ronde')
        wins.append(2)
        return random.choice(moves)


def advanced_AI():
    wins = []
    moves = ['rock', 'paper', 'scissor']
    player_move = steen_schaar.main()
    com_move = random.choice(moves)
    print(com_move)
    result = get_winner(player_move, com_move)
    com_move = add_win(result, moves, wins, com_move)

    for i in range(1, 5):
        player_move = steen_schaar.main()
        print(com_move)
        result = get_winner(player_move, com_move)
        com_move = add_win(result, moves, wins, com_move)

    show_winner(wins)


if __name__ == '__main__':
    basic_com()
    # advanced_AI()
