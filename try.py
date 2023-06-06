import numpy as np
import math


class TicTacToe:
    def __init__(self):
        self.row_count = 3
        self.column_count = 3
        self.action_size = self.row_count * self.column_count

    def get_initial_state(self):
        return np.zeros((self.row_count, self.column_count))

    def get_next_state(self, state, action, player):
        row = action//self.column_count
        column = action % self.column_count
        state[row, column] = player
        return state

    def get_valid_moves(self, state):
        return (state.reshape(-1) == 0).astype(np.uint8)

    def check_win(self, state, action):
        if action == None:
            return False
        row = action//self.column_count
        column = action % self.column_count
        player = state[row, column]
        return (
            np.sum(state[row, :]) == player*self.column_count
            or np.sum(state[:, column]) == player*self.column_count
            or np.sum(np.diag(state)) == player*self.row_count
            or np.sum(np.diag(np.flip(state, axis=0))) == player*self.row_count
        )

    def get_value_and_terminated(self, state, action):
        if self.check_win(state, action):
            return 1, True
        if np.sum(self.get_valid_moves(state)) == 0:
            return 0, True
        return 0, False

    def get_opponent(self, player):
        return -player

    def get_opponent_value(self, value):
        return -value

    def change_perspective(self, state, player):
        return state*player


tictactoe = TicTacToe()
player = 1
state = tictactoe.get_initial_state()

while True:
    print(state)
    valid_moves = tictactoe.get_valid_moves(state)
    print("valid_moves", [i for i in range(
        tictactoe.action_size) if valid_moves[i] == 1])
    action = int(input(f"{player}:"))

    if valid_moves[action] == 0:
        print("action not valid")
        continue

    state = tictactoe.get_next_state(state, action, player)

    value, is_terminal = tictactoe.get_value_and_terminated(state, action)

    if is_terminal:
        print(state)
        if value == 1:
            print(player, "won")
        else:
            print("draw")
        break

    player = tictactoe.get_opponent(player)


class Node:
    def __init__(self, game, args, state, parent=None, action_taken=None):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken

        self.children = []
        self.expandable_moves = game.get_valid_moves(state)

        self.visit_count = 0
        self.value_sum = 0

    def is_fully_expanded(self):
        return np.sum(self.expandable_moves) == 0 and len(self.children) > 0

    def select(self):
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_child:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        q_value = 1 - ((child.value_sum/child.visit_count)+1)/2
        return q_value + self.args['c']*math.sqrt(math.log(self.visit_count)/child.visit_count)

    def expand(self):
        action = np.random.choice(np.where(self.expandable_moves == 1)[0])
        self.expandable_moves[action] = 0

        child_state = self.state.copy()
        child_state = self.game.get_next_state(child_state, action, 1)
        child_state = self.game.change_perspective(child_state, player=-1)


class MCTS:
    def __init__(self, game, args):
        self.game = game
        self.args = args

    def search(self, state):
        root = Node(self.game, self.args, state)

        for search in range(self.args['num_search']):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            value, is_terminal = self.game.get_value_and_terminated(
                node.state, node.action_taken)
            value = self.game.get_opponent_value(value)

            if not is_terminal:
                node = node.expand()
