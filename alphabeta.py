import random
from utils import *

class Game:
    def moves_possible(self, state):
        """
        function needs to be implemented in subclass else NotImplemented exception raised
        """
        abstract

    def play_move(self, move, state):
        """
        function needs to be implemented in subclass else NotImplemented exception raised
        """
        abstract

    def current_state(self, state, player):
        """
        function needs to be implemented in subclass else NotImplemented exception raised
        """
        abstract

    def terminate(self, state):
        return not self.moves_possible(state)

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        print state

    def possible_successors(self, state):
        return [(move, self.play_move(move, state))
                for move in self.moves_possible(state)]

class TicTacToe(Game):
    """
    Player entries : X and O
    Default board size 3x3
    """
    def __init__(self, h=3, v=3, k=3):
        update(self, h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)

    def moves_possible(self, state):
        return state.moves

    def play_move(self, move, state):
        if move not in state.moves:
            return state
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return Struct(to_move=if_(state.to_move == 'X', 'O', 'X'), utility=self.check_state(board, move, state.to_move), board=board, moves=moves)

    def current_state(self, state):
        """
        1 for win, -1 for loss, 0 for illegal
        """
        return state.utility

    def terminate(self, state):
        """
        if game won or no empty squares
        """
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print board.get((x, y), '.'),
            print

    def check_state(self, board, move, player):
        """
        If X wins with this move, return 1; if O wins, return -1; else return 0.
        """
        if (self.line_through_move(board, move, player, (0, 1)) or self.line_through_move(board, move, player, (1, 0)) or self.line_through_move(board, move, player, (1, -1)) or self.line_through_move(board, move, player, (1, 1))):
            return if_(player == 'X', +1, -1)
        else:
            return 0

    def line_through_move(self, board, move, player, (dx, dy)):
        """
        Line through board move available
        """
        x, y = move
        n = 0
        while board.get((x, y)) == player:
            n += 1
            x, y = x + dx, y + dy
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - dx, y - dy
        n -= 1
        return n >= self.k

def max_full_value(state, alpha, beta, game):
        if game.terminate(state):
            return game.current_state(state, player)
        v = -infinity
        for (a, s) in game.possible_successors(state):
            v = max(v, min_full_value(s, alpha, beta, game))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

def min_full_value(state, alpha, beta, game):
        if game.terminate(state):
            return game.current_state(state, player)
        v = infinity
        for (a, s) in game.possible_successors(state):
            v = min(v, max_full_value(s, alpha, beta, game))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

"""
search all the way to the leaves
"""
def alphabeta_full_search(state, game):
    player = game.to_move(state)
    action, state = argmax(game.possible_successors(state), lambda ((a, s)): min_full_value(s, -infinity, infinity, game))
    return action

def cutoff_test(state, depth, game):
    cutoff_test = None
    cutoff_test = (cutoff_test or (lambda state, depth: depth>d or game.terminate(state)))
    return cutoff_test

def eval_function(state, game):
    eval_fn = None
    eval_fn = eval_fn or (lambda state: game.current_state(state, player))
    return eval_fn

def max_prune_value(state, alpha, beta, depth, game):
        if cutoff_test(state, depth, game):
            return eval_function(state, game)
        v = -infinity
        for (a, s) in game.possible_successors(state):
            v = max(v, min_prune_value(s, alpha, beta, depth+1, game))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

def min_prune_value(state, alpha, beta, depth, game):
    if cutoff_test(state, depth, game):
        return eval_function(state, game)
    v = infinity
    for (a, s) in game.possible_successors(state):
        v = min(v, max_prune_value(s, alpha, beta, depth+1, game))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

"""
search upto cutoff depth
"""
def alphabeta_pruning_search(state, game, d=4, cutoff_test=cutoff_test, eval_function=eval_function):
    player = game.to_move(state)
    action, state = argmax(game.possible_successors(state), lambda ((a, s)): min_prune_value(s, -infinity, infinity, 0, game))
    return action
