import random

ready = False  # is game ready to be played
game_status = {'Stock pieces': [],
               'Computer pieces': [],
               'Player pieces': [],
               'Domino snake': [],
               'Status': ''}


class Player:

    def move(self, selection):
        invalid_input = False
        _continue = True
        snake_end = Snake().end()
        snake_start = Snake().start()

        if abs(selection) > len(game_status['Player pieces']):
            print('Invalid input. Please try again.')
            return invalid_input
        elif selection > 0:
            domino = game_status['Player pieces'][selection - 1]
            if domino[0] == snake_end:
                game_status['Player pieces'].remove(domino)
                game_status['Domino snake'].append(domino)
            elif domino[1] == snake_end:
                game_status['Player pieces'].remove(domino)
                domino.reverse()
                game_status['Domino snake'].append(domino)
            else:
                print('Illegal move. Please try again.')
                return invalid_input
        elif selection < 0:
            domino = game_status['Player pieces'][abs(selection) - 1]
            if domino[1] == snake_start:
                game_status['Player pieces'].remove(domino)
                game_status['Domino snake'].insert(0, domino)
            elif domino[0] == snake_start:
                game_status['Player pieces'].remove(domino)
                domino.reverse()
                game_status['Domino snake'].insert(0, domino)
            else:
                print('Illegal move. Please try again.')
                return invalid_input
        else:  # selection == 0
            if len(game_status['Stock pieces']) > 0:
                piece = game_status['Stock pieces'].pop(0)
                game_status['Player pieces'].append(piece)

        return _continue


class Computer:

    def __init__(self):
        self.scores = []

    def calc_score(self):
        counts = {x: 0 for x in range(7)}

        for [x, y] in game_status['Computer pieces']:
            counts[x] += 1
            counts[y] += 1
        for [x, y] in game_status['Domino snake']:
            counts[x] += 1
            counts[y] += 1
        for [a, b] in game_status['Computer pieces']:
            score = counts[a] + counts[b]
            self.scores.append(([a, b], score))

        self.scores.sort(key=lambda pair: pair[1], reverse=True)

    def move(self):
        self.calc_score()
        end = Snake().end()
        start = Snake().start()

        for piece, _ in self.scores:
            # check snake end
            if end in piece:
                if piece[0] == end:
                    game_status['Computer pieces'].remove(piece)
                    game_status['Domino snake'].append(piece)
                    break
                else:
                    game_status['Computer pieces'].remove(piece)
                    piece.reverse()
                    game_status['Domino snake'].append(piece)
                    break

            # check snake start
            if start in piece:
                if piece[1] == start:
                    game_status['Computer pieces'].remove(piece)
                    game_status['Domino snake'].insert(0, piece)
                    break
                else:
                    game_status['Computer pieces'].remove(piece)
                    piece.reverse()
                    game_status['Domino snake'].insert(0, piece)
                    break
        else:
            if len(game_status['Stock pieces']) > 0:
                piece = game_status['Stock pieces'].pop(0)
                game_status['Computer pieces'].append(piece)
            else:
                pass


class Snake:
    def end(self):
        snake = game_status['Domino snake']
        return snake[-1][1]

    def start(self):
        snake = game_status['Domino snake']
        return snake[0][0]

    def dead(self):
        snake = game_status['Domino snake']
        start = self.end()
        end = self.start()
        value_count = 0

        if start == end:
            for [a, b] in snake:
                if a == start:
                    value_count += 1
                if b == start:
                    value_count += 1

            if value_count == 8:
                return True

        return False


def main():
    domino_set = initialize()

    while not ready:
        reshuffle(domino_set)
        check_first()

    while in_play():
        display()
        while not play():
            pass
        switch_turn()

    display()


def initialize():
    domino_set = []
    for a in range(7):
        for b in range(7):
            domino = [a, b]
            if [b, a] not in domino_set:
                domino_set.append(domino)
    return domino_set


def reshuffle(domino_set):
    random.shuffle(domino_set)
    game_status['Player pieces'] = domino_set[0:7]
    game_status['Computer pieces'] = domino_set[7:14]
    game_status['Stock pieces'] = domino_set[14:28]


def check_first():
    max_double_computer = [0, 0]
    max_double_player = [0, 0]
    global ready

    for [x, y] in game_status['Computer pieces']:
        if x == y and x >= max_double_computer[0]:
            max_double_computer = [x, y]

    for [x, y] in game_status['Player pieces']:
        if x == y and x >= max_double_player[0]:
            max_double_player = [x, y]

    if max_double_computer[0] > max_double_player[0]:
        game_status['Computer pieces'].remove(max_double_computer)
        game_status['Domino snake'].append(max_double_computer)
        game_status['Status'] = 'player'
        ready = True
    elif max_double_player[0] > max_double_computer[0]:
        game_status['Player pieces'].remove(max_double_player)
        game_status['Domino snake'].append(max_double_player)
        game_status['Status'] = 'computer'
        ready = True


def in_play():
    computer = len(game_status['Computer pieces'])
    player = len(game_status['Player pieces'])
    snake_dead = Snake().dead()
    if computer > 0 and player > 0 and not snake_dead:
        return True
    elif computer == 0:
        game_status['Status'] = 'computer won'
    elif player == 0:
        game_status['Status'] = 'player won'
    elif snake_dead:
        game_status['Status'] = 'draw'

    return False


def display():
    print('=' * 70)

    print('Stock size:', len(game_status['Stock pieces']))

    print('Computer pieces:', len(game_status['Computer pieces']))
    print()

    snake = game_status['Domino snake']
    if len(snake) <= 6:
        for piece in snake:
            print(piece, end='')
    else:
        for i in range(3):
            print(snake[i], end='')
        print('...', end='')
        for i in range(-3, 0):
            print(snake[i], end='')
    print('\n')

    print('Your pieces:')

    for i, piece in enumerate(game_status['Player pieces']):
        print(i + 1, ':', piece, sep='')
    print()

    print('Status: ', end='')
    if game_status['Status'] == 'player':
        print("It's your turn to make a move. Enter your command.")
    elif game_status['Status'] == 'computer':
        print("Computer is about to make a move. Press Enter to continue...")
    elif game_status['Status'] == 'computer won':
        print("The game is over. The computer won!")
    elif game_status['Status'] == 'player won':
        print("The game is over. You won!")
    else:
        print("The game is over. It's a draw!")


def play():
    """ Return True if valid play else False. """
    invalid_input = False
    user_input = input()
    computer = Computer()
    player = Player()

    if game_status['Status'] == 'player':
        try:
            selection = int(user_input)
        except ValueError:
            print('Invalid input. Please try again.')
            return invalid_input
        return player.move(selection)
    elif game_status['Status'] == 'computer':
        computer.move()
        return True


def switch_turn():
    if game_status['Status'] == 'player':
        game_status['Status'] = 'computer'
    elif game_status['Status'] == 'computer':
        game_status['Status'] = 'player'


if __name__ == "__main__":
    main()
