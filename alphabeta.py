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
